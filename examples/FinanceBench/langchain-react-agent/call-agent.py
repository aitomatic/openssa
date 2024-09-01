import concurrent.futures
import pandas as pd
import time
from pdfminer.high_level import extract_text
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def create_vectorstore(documents):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

def create_react_agent(vectorstore):
    llm = ChatOpenAI(model_name="gpt-4o")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
    return qa_chain

def load_and_prepare_pdfs(pdf_paths):
    all_documents = []
    
    for pdf_path in pdf_paths:
        text = extract_text_from_pdf(pdf_path)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(text)
        documents = [Document(page_content=t) for t in texts]
        all_documents.extend(documents)
    
    return all_documents

def ask_question(react_agent, query):
    response = react_agent.invoke({"query": query}) 
    return response['result']

def main(queries, pdf_paths):
    print("Loading and preparing PDFs...")
    documents = load_and_prepare_pdfs(pdf_paths)

    print("Creating vectorstore...")
    vectorstore = create_vectorstore(documents)

    print("Creating react agent...")
    react_agent = create_react_agent(vectorstore)

    question_answer_pairs = []
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(ask_question, react_agent, query): (i, query) for i, query in enumerate(queries)}
        for future in concurrent.futures.as_completed(futures):
            index, question = futures[future]
            answer = future.result()
            question_answer_pairs.append({"index": index, "question": question, "answer": answer})

    print("Processing time: ", time.time() - start)
    question_answer_pairs.sort(key=lambda x: x["index"])

    return question_answer_pairs

def load_questions_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df

def save_results_to_csv(df, output_file):
    df.to_csv(output_file, index=False)

def process_questions(data_file, pdf_paths, output_file):
    df = load_questions_from_csv(data_file)

    queries = df['question'].tolist()

    question_answer_pairs = main(queries, pdf_paths)
    
    drop_columns = ["answer", "OpenAI-Asst", "OpenAI-Asst---CORRECTNESS"]
    
    df.drop(columns=drop_columns, inplace=True)
    
    df['langchain_answer'] = "" 
    for pair in question_answer_pairs:
        df.loc[pair['index'], 'langchain_answer'] = pair['answer']

    save_results_to_csv(df, output_file)
    print(f"Results saved to {output_file}")

# File paths
data_file = "./data.csv" 
output_file = "./output.csv" 
pdf_paths = [f"./AMD_2022_10K.pdf"]

process_questions(data_file, pdf_paths, output_file)
