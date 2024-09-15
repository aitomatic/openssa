import fitz
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI
from langchain_openai.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain_community.tools.vectorstore.tool import VectorStoreQATool
import sys

def capture_agent_output_to_file(agent_executor, question, file_path):
    # Open a file to write output
    with open(file_path, 'w') as f:
        # Redirect stdout to the file
        sys.stdout = f
        
        # Invoke the agent with the input question
        answer = agent_executor.invoke({"input": question})
        
        # Restore stdout to its original state
        sys.stdout = sys.__stdout__
        return answer


def process_question_with_pdf(question, pdf_path, output_path):
    try:
        doc = fitz.open(pdf_path)
        text = "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"Error extracting text from {pdf_path}: {e}"

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text(text)
    documents = [Document(page_content=t) for t in texts]

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)

    prompt = hub.pull("hwchase17/react")
    llm = ChatOpenAI(model_name="gpt-4o")

    vectorstore_tool = VectorStoreQATool(
        name="Financial Analysis",
        description="Tool to answer questions based on financial data",
        vectorstore=vectorstore,
        llm=llm
    )

    agent = create_react_agent(llm, [vectorstore_tool], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[vectorstore_tool], verbose=True)

    response = capture_agent_output_to_file(agent_executor, question, output_path)

    return response['output']

if __name__ == "__main__":
    question = "What is Adobe's year-over-year change in unadjusted operating income from FY2015 to FY2016 (in units of percents and round to one decimal place)? Give a solution to the question by using the income statement."
    pdf_path = "./docs/ADOBE_2016_10K.pdf"
    reasoning_output_path = "output.txt"

    answer = process_question_with_pdf(question, pdf_path, reasoning_output_path)
    print("Reasoning output saved to:", reasoning_output_path)
    print("Answer:", answer)