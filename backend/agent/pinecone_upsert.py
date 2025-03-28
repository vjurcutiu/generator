import os
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

# Initialize Pinecone with your API key and environment variables
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_env = os.environ.get("PINECONE_ENV")
if not pinecone_api_key or not pinecone_env:
    raise ValueError("PINECONE_API_KEY and PINECONE_ENV must be set in the environment")

pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

# Define your Pinecone index name and dimension (for example, using OpenAI's embeddings, dimension=1536)
INDEX_NAME = "your-index-name"
EMBEDDING_DIM = 1536

# Create the index if it doesn't exist
if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(INDEX_NAME, dimension=EMBEDDING_DIM)

def upsert_document(file_path: str):
    """
    Reads a file from disk, splits it into chunks, computes embeddings using LangChain,
    and upserts the embeddings into the specified Pinecone index.
    """
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split text into manageable chunks (tweak chunk_size and overlap as needed)
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text(content)

    # Wrap each chunk in a Document
    documents = [Document(page_content=t) for t in texts]

    # Initialize embeddings (this example uses OpenAI embeddings; set your parameters if needed)
    embeddings = OpenAIEmbeddings()

    # Prepare data for upsertion
    vectors = []
    file_identifier = os.path.basename(file_path)
    for i, doc in enumerate(documents):
        # Use the embedding model to convert the document text to a vector
        vector = embeddings.embed_query(doc.page_content)
        # Create a unique id for each vector; include file name and chunk index
        vector_id = f"{file_identifier}-{i}"
        # Include metadata if needed (e.g., original text)
        metadata = {"text": doc.page_content}
        vectors.append((vector_id, vector, metadata))

    # Connect to the Pinecone index and upsert the vectors
    index = pinecone.Index(INDEX_NAME)
    upsert_response = index.upsert(vectors=vectors)
    return upsert_response
