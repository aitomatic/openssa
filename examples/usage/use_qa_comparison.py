import pandas as pd
from openssa.core.rag_ooda.rag_ooda import RagOODA
from openssa.core.rag_ooda.resources.standard_vi.standard_vi import load_standard_vi
from openssa.core.rag_ooda.resources.dense_x.dense_x import load_dense_x


class RagStrategy:
    dense = "dense"
    standard_vi = "standard_vi"


class RagUseCase:
    m290 = "m290"
    l316 = "l316"


DATA_FOLDER_PATH = "examples/data"


def get_dirs(use_case: str, strategy: str) -> tuple:
    cache_dir = f"{DATA_FOLDER_PATH}/cache/{strategy}/{use_case}/indexes"
    data_dir = f"{DATA_FOLDER_PATH}/docs/{use_case}"
    nodes_cache_path = f"{DATA_FOLDER_PATH}/cache/{strategy}/{use_case}/nodes_dict.json"
    return cache_dir, data_dir, nodes_cache_path


def load_standard_vector_index():
    use_case = RagUseCase.m290
    strategy = RagStrategy.standard_vi
    cache_dir, data_dir, _ = get_dirs(use_case, strategy)
    print(f"Loading resources... {use_case} with strategy {strategy} ")
    return load_standard_vi(data_dir, cache_dir)


def load_dense_x_index():
    strategy = RagStrategy.dense
    use_case = RagUseCase.m290
    cache_dir, data_dir, nodes_cache_path = get_dirs(use_case, strategy)
    print(f"Loading resources... {use_case} with strategy {strategy} ")
    return load_dense_x(data_dir, cache_dir, nodes_cache_path)


def main():
    rag_standard_vi = load_standard_vector_index()
    print("standard vector index loaded.")

    # rag_dense_x = load_dense_x_index()
    # print("dense_x indexes loaded.")

    resources = [rag_standard_vi]
    rag_ooda = RagOODA(resources=resources)

    questions = [
        "do I need heat treatment for the 316L with M 290?",
        # "Which steel can I print?",
        # "can I print a part 50 cm long in the M 290?",
        # "Is it preferable to use nitrogen when printing with titanium?",
        # "List all the materials I can print with?",
        # "What are the calibration steps for a new build?",
        # "what are the size limits?",
        # "what are the parts size limits for the M 290?",
    ]

    svi_answers = []
    ro_answers = []
    # dense_x_answers = []

    for q in questions:
        print(f"\nQuestion: {q}\n")
        stand_vi_answer = rag_standard_vi.query_engine.query(q).response
        svi_answers.append(stand_vi_answer)
        # dense_x_answer = rag_dense_x.query_engine.query(q)
        # dense_x_answers.append(dense_x_answer)
        rag_ooda_answer = rag_ooda.chat(q)
        ro_answers.append(rag_ooda_answer)

    df = pd.DataFrame(  # noqa: PD901
        {
            "question": questions,
            "stand vector index": svi_answers,
            # "dense x": dense_x_answers,
            "rag ooda": ro_answers,
        }
    )
    df.to_csv(f"{DATA_FOLDER_PATH}/qa_comparion.csv", index=False)


if __name__ == "__main__":
    main()
