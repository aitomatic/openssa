import concurrent.futures
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import time
import pandas as pd

def extract_text_from_pdf(pdf_path):
    try:
        print(pdf_path)
        return extract_text(pdf_path)
    except PDFSyntaxError:
        print(f"Error extracting text from {pdf_path}: Not a valid PDF.")
        return None

def create_vectorstore(documents):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

def create_react_agent(vectorstore):
    llm = ChatOpenAI(model_name="gpt-4o")
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
    return qa_chain

def load_and_prepare_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text(text)
    documents = [Document(page_content=t) for t in texts]
    return documents

def ask_question(react_agent, query):
    response = react_agent.invoke({"query": query}) 
    return response['result']

def process_single_question(question, pdf_path):
    documents = load_and_prepare_pdf(pdf_path)

    vectorstore = create_vectorstore(documents)

    react_agent = create_react_agent(vectorstore)

    answer = ask_question(react_agent, question)
    
    return answer

def process_questions_parallel(questions, pdf_paths):
    results = [None] * len(questions)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_single_question, question, pdf_path): index for index, (question, pdf_path) in enumerate(zip(questions, pdf_paths))}
        
        for future in concurrent.futures.as_completed(futures):
            index = futures[future]
            results[index] = future.result()

    return results

if __name__ == "__main__":
    # Example usage

    data = pd.read_csv('data.csv')
    questions = data['question'].tolist()
    pdf_paths = [f"./docs/{doc_name}.pdf" for doc_name in data['doc_name']]

    all_answers = []

    # Run the loop 4 times
    for i in range(4):
        print(f"Starting iteration {i+1}")
        start = time.time()
        answers = process_questions_parallel(questions, pdf_paths)
        print(f"Iteration {i+1} processing time: {time.time() - start}")
        all_answers.append(answers)

    # Prepare data for CSV
    data = {"question": questions}
    for i in range(4):
        data[f"answer {i+1}"] = [all_answers[i][j] for j in range(len(questions))]

    df = pd.DataFrame(data)
    df.to_csv("langchain_output.csv", index=False)

    print("Results saved to langchain_output.csv")
