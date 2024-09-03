# import fitz
# import pandas as pd
# import concurrent.futures
# from langchain_community.vectorstores import FAISS
# from langchain_openai.embeddings import OpenAIEmbeddings
# from langchain.docstore.document import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain import hub
# from langchain.agents import AgentExecutor, create_react_agent
# from langchain_openai.chat_models import ChatOpenAI
# from langchain.tools import Tool
# import logging

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def process_question_with_pdf(question, pdf_path):
#     try:
#         doc = fitz.open(pdf_path)
#         text = "".join([page.get_text() for page in doc])
        
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#         texts = text_splitter.split_text(text)
#         documents = [Document(page_content=t) for t in texts]

#         embeddings = OpenAIEmbeddings()
#         vectorstore = FAISS.from_documents(documents, embeddings)

#         def vectorstore_tool(query: str) -> str:
#             results = vectorstore.similarity_search(query, k=1)
#             return results[0].page_content if results else "No relevant documents found."

#         vectorstore_tool = Tool(
#             name="Vectorstore Retriever",
#             func=vectorstore_tool,
#             description="Search documents using a vectorstore."
#         )
#         prompt = hub.pull("hwchase17/react")
#         llm = ChatOpenAI(model_name="gpt-4o")  # Use gpt-4o model
#         agent = create_react_agent(llm, [vectorstore_tool], prompt)
        
#         agent_executor = AgentExecutor(agent=agent, tools=[vectorstore_tool], verbose=True, handle_parsing_errors=True)

#         response = agent_executor.invoke({"input": question})
#         return response['output']

#     except Exception as e:
#         logging.error(f"Error processing {pdf_path} for question: {question}: {e}")
#         return str(e)

# def process_row(row):
#     try:
#         question = row['question']
#         pdf_name = row['doc_name']
#         pdf_path = f"./docs/{pdf_name}.pdf"
    
#         logging.info(f"Processing {pdf_name} for question: {question}")
#         answer = process_question_with_pdf(question, pdf_path)
    
#         return answer
    
#     except Exception as e:
#         logging.error(f"Failed to process row: {e}")
#         return str(e)

# if __name__ == "__main__":
#     data = pd.read_csv('data.csv')

#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         try:
#             results = list(executor.map(process_row, [row for _, row in data.iterrows()]))
#         except Exception as e:
#             logging.error(f"Parallel processing failed: {e}")
#             raise

#     data['langchain_react'] = results

#     data.to_csv('data_with_answers.csv', index=False)
#     logging.info("Results saved to data_with_answers.csv")



import fitz
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI
from langchain.tools import Tool

def process_question_with_pdf(question, pdf_path):
    # Extract text from the PDF
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

    def vectorstore_tool(query: str) -> str:
        results = vectorstore.similarity_search(query, k=1)
        return results[0].page_content if results else "No relevant documents found."

    vectorstore_tool = Tool(
        name="Vectorstore Retriever",
        func=vectorstore_tool,
        description="Search documents using a vectorstore."
    )
    prompt = hub.pull("hwchase17/react")
    llm = OpenAI()
    agent = create_react_agent(llm, [vectorstore_tool], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[vectorstore_tool], verbose=True)

    response = agent_executor.invoke({"input": question})
    return response['output']

if __name__ == "__main__":
    question = "What is Adobe's year-over-year change in unadjusted operating income from FY2015 to FY2016 (in units of percents and round to one decimal place)? Give a solution to the question by using the income statement."
    pdf_path = "./docs/ADOBE_2016_10K.pdf"

    answer = process_question_with_pdf(question, pdf_path)
    print("Answer:", answer)
