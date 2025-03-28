from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

def create_rag_chain():
    # Load documents (update the path or use multiple files as needed)
    loader = TextLoader("path/to/your/document.txt")
    documents = loader.load()

    # Create a vector store index from the documents (using FAISS, Chroma, etc.)
    index_creator = VectorstoreIndexCreator()
    vectorstore = index_creator.from_documents(documents)
    
    # Initialize the LLM
    llm = OpenAI(temperature=0)
    
    # Create a RetrievalQA chain that uses the vector store as a retriever
    qa_chain = RetrievalQA(llm=llm, retriever=vectorstore.as_retriever())
    return qa_chain

if __name__ == '__main__':
    qa_chain = create_rag_chain()
    query = "What is LangChain?"
    result = qa_chain.run(query)
    print("RAG Result:", result)
