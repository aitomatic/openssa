import asyncio
import json
from pathlib import Path
import yaml
from typing import Any, Dict, List, Optional
from json import JSONDecodeError
from yaml import YAMLError
from llama_index.core import Document, ServiceContext, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.llama_pack import BaseLlamaPack
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import TextSplitter
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.schema import IndexNode, TextNode
from llama_index.core import PromptTemplate
from llama_index.core.async_utils import run_jobs
from llama_index.core.llms import LLM


PROPOSITIONS_PROMPT = PromptTemplate(
    """Decompose the "Content" into clear and simple propositions, ensuring they are interpretable out of
context.
1. Split compound sentence into simple sentences. Maintain the original phrasing from the input
whenever possible.
2. For any named entity that is accompanied by additional descriptive information, separate this
information into its own distinct proposition.
3. Decontextualize the proposition by adding necessary modifier to nouns or entire sentences
and replacing pronouns (e.g., "it", "he", "she", "they", "this", "that") with the full name of the
entities they refer to.
4. Present the results as a list of strings, formatted in JSON.

Input: Title: ¯Eostre. Section: Theories and interpretations, Connection to Easter Hares. Content:
The earliest evidence for the Easter Hare (Osterhase) was recorded in south-west Germany in
1678 by the professor of medicine Georg Franck von Franckenau, but it remained unknown in
other parts of Germany until the 18th century. Scholar Richard Sermon writes that "hares were
frequently seen in gardens in spring, and thus may have served as a convenient explanation for the
origin of the colored eggs hidden there for children. Alternatively, there is a European tradition
that hares laid eggs, since a hare’s scratch or form and a lapwing’s nest look very similar, and
both occur on grassland and are first seen in the spring. In the nineteenth century the influence
of Easter cards, toys, and books was to make the Easter Hare/Rabbit popular throughout Europe.
German immigrants then exported the custom to Britain and America where it evolved into the
Easter Bunny."
Output: [ "The earliest evidence for the Easter Hare was recorded in south-west Germany in
1678 by Georg Franck von Franckenau.", "Georg Franck von Franckenau was a professor of
medicine.", "The evidence for the Easter Hare remained unknown in other parts of Germany until
the 18th century.", "Richard Sermon was a scholar.", "Richard Sermon writes a hypothesis about
the possible explanation for the connection between hares and the tradition during Easter", "Hares
were frequently seen in gardens in spring.", "Hares may have served as a convenient explanation
for the origin of the colored eggs hidden in gardens for children.", "There is a European tradition
that hares laid eggs.", "A hare’s scratch or form and a lapwing’s nest look very similar.", "Both
hares and lapwing’s nests occur on grassland and are first seen in the spring.", "In the nineteenth
century the influence of Easter cards, toys, and books was to make the Easter Hare/Rabbit popular
throughout Europe.", "German immigrants exported the custom of the Easter Hare/Rabbit to
Britain and America.", "The custom of the Easter Hare/Rabbit evolved into the Easter Bunny in
Britain and America." ]

Input: {node_text}
Output:"""
)


def store_nodes_dict(nodes_dict: Dict[str, TextNode], nodes_cache_path) -> None:
    """Store nodes dict."""
    output_dict = {}
    for node_id, node in nodes_dict.items():
        output_dict[node_id] = node.to_json()
    nodes_cache_path = Path(nodes_cache_path)
    nodes_cache_path.parent.mkdir(parents=True, exist_ok=True)

    with open(nodes_cache_path, "w") as f:  # noqa: PLW1514
        json.dump(output_dict, f)


def load_nodes_dict(nodes_cache_path: str) -> Dict[str, TextNode]:
    """Load nodes dict."""
    with open(nodes_cache_path, "r") as f:  # noqa: PLW1514 UP015
        nodes_dict = json.load(f)

    output_dict = {}
    for node_id, node in nodes_dict.items():
        output_dict[node_id] = TextNode.from_json(node)

    return output_dict


class DenseXRetrievalPack(BaseLlamaPack):
    def __init__(
        self,
        documents: List[Document],
        proposition_llm: Optional[LLM] = None,
        query_llm: Optional[LLM] = None,
        embed_model: Optional[BaseEmbedding] = None,
        text_splitter: TextSplitter = SentenceSplitter(),
        similarity_top_k: int = 4,
    ) -> None:
        """Init params."""
        self._proposition_llm = proposition_llm or OpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=750,
        )

        embed_model = embed_model or OpenAIEmbedding(embed_batch_size=128)

        nodes = text_splitter.get_nodes_from_documents(documents)

        sub_nodes = self._gen_propositions(nodes)

        all_nodes = nodes + sub_nodes
        self.all_nodes_dict = {n.node_id: n for n in all_nodes}

        service_context = ServiceContext.from_defaults(
            llm=query_llm or OpenAI(),
            embed_model=embed_model,
            num_output=self._proposition_llm.metadata.num_output,
        )

        self.vector_index = VectorStoreIndex(
            all_nodes, service_context=service_context, show_progress=True
        )

        self.retriever = RecursiveRetriever(
            "vector",
            retriever_dict={
                "vector": self.vector_index.as_retriever(
                    similarity_top_k=similarity_top_k
                )
            },
            node_dict=self.all_nodes_dict,
        )

        self.query_engine = RetrieverQueryEngine.from_args(
            self.retriever, service_context=service_context
        )

    async def _aget_proposition(self, node: TextNode) -> List[TextNode]:
        """Get proposition."""
        inital_output = await self._proposition_llm.apredict(
            PROPOSITIONS_PROMPT, node_text=node.text
        )
        outputs = inital_output.split("\n")

        all_propositions = []

        for output in outputs:
            if not output.strip():
                continue
            if not output.strip().endswith("]"):
                if not output.strip().endswith('"') and not output.strip().endswith(
                    ","
                ):
                    output = output + '"'  # noqa: PLW2901
                output = output + " ]"  # noqa: PLW2901
            if not output.strip().startswith("["):
                if not output.strip().startswith('"'):
                    output = '"' + output  # noqa: PLW2901
                output = "[ " + output  # noqa: PLW2901

            try:
                propositions = json.loads(output)
            except JSONDecodeError:
                # fallback to yaml
                try:
                    propositions = yaml.safe_load(output)
                except YAMLError:
                    # fallback to next output
                    continue

            if not isinstance(propositions, list):
                continue

            all_propositions.extend(propositions)

        assert isinstance(all_propositions, list)
        nodes = [TextNode(text=prop) for prop in all_propositions if prop]

        sub_nodes = [IndexNode.from_text_node(n, node.node_id) for n in nodes]
        return sub_nodes

    def _gen_propositions(self, nodes: List[TextNode]) -> List[TextNode]:
        """Get propositions."""
        sub_nodes = asyncio.run(
            run_jobs(
                [self._aget_proposition(node) for node in nodes],
                show_progress=True,
                workers=8,
            )
        )

        # Flatten list
        return [node for sub_node in sub_nodes for node in sub_node]

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "query_engine": self.query_engine,
            "retriever": self.retriever,
        }

    def run(self, query_str: str, **kwargs: Any) -> Any:
        """Run the pipeline."""
        return self.query_engine.query(query_str)
