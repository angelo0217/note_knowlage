import json
import sys

import redis
from langchain_ollama import OllamaEmbeddings
from langchain.docstore.document import Document
from langchain_community.vectorstores import Redis as RedisVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- Configuration ---
REDIS_HOST = 'n8n_redis'  # n8n_redis
REDIS_PORT = 6379
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
RAG_INDEX_NAME = "ticket_rag_index" # Unified index name for RAG

ollama_host = "n8n_ollama"  # n8n_ollama
ollama_port = 11434                  # Ollama 服務的端口
ollama_url = f"http://{ollama_host}:{ollama_port}"

# Initialize embeddings globally, as it's used for vector store operations
try:
    EMBEDDINGS_MODEL = "nomic-embed-text"
    embeddings = OllamaEmbeddings(
        model=EMBEDDINGS_MODEL, base_url=ollama_url
    )
    print(f"Successfully initialized Ollama embeddings with model: {EMBEDDINGS_MODEL}")
except Exception as e:
    # If Ollama is not running or model not available, this will fail early
    error_output = {"error": f"Failed to initialize Ollama embeddings: {e}. Please ensure Ollama is running and '{EMBEDDINGS_MODEL}' model is pulled."}
    print(json.dumps({"json": error_output}, ensure_ascii=False))
    sys.exit(1)


# --- Helper Functions ---

def _clear_redis_index(redis_conn: redis.Redis, index_name: str):
    """
    Clears an existing Redis index if it exists by deleting associated keys.
    This is an internal helper function.
    """
    try:
        # Check if the index exists. Note: FTS.INFO is for RediSearch indexes.
        # For Langchain's Redis vectorstore, keys are prefixed with 'doc:{index_name}:'
        print(f"Attempting to clear existing Redis index '{index_name}'...")
        keys_to_delete = redis_conn.keys(f"doc:{index_name}:*")
        if keys_to_delete:
            deleted_count = redis_conn.delete(*keys_to_delete)
            print(f"Successfully deleted {deleted_count} keys associated with index '{index_name}'.")
        else:
            print(f"No keys found for index '{index_name}'. Nothing to clear.")
    except Exception as e:
        print(f"Warning: Could not clear Redis index '{index_name}': {e}")
        # Do not re-raise, as existing index might not be critical for subsequent ops if data is overwritten

def _split_documents(documents: list[Document], index_name: str) -> list[Document]:
    """
    Internal helper to split Langchain Document objects into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""],
        length_function=len,
        is_separator_regex=False,
    )
    docs = text_splitter.split_documents(documents)
    print(f"Split {len(docs)} documents into chunks for RAG index '{index_name}'.")
    return docs

def train_rag_vector_store(context_text: str, index_name: str, metadata: dict = None):
    """
    Trains the Redis vector database directly from a given text context.
    This function handles document splitting, embedding generation,
    and storage in the Redis vector store.
    """
    print(f"Starting RAG vector store training from context into index: {index_name}")

    # Create a Langchain Document object from the context text
    if metadata is None:
        metadata = {"source": f"context_train_{index_name}"}

    documents = [Document(page_content=context_text, metadata=metadata)]

    # Split text
    docs = _split_documents(documents, index_name)

    # Generate embeddings and store in Redis vector database
    # _clear_redis_index is called inside train_rag_vector_store to ensure a clean state
    # for the vector store specifically.
    try:
        # RedisVectorStore.from_documents automatically handles creation/clearing
        # but it's good practice to ensure direct key cleanup if separate keys are managed.
        vectorstore = RedisVectorStore.from_documents(
            docs, embeddings, redis_url=REDIS_URL, index_name=index_name
        )
        print(f"Context loaded and indexed into Redis RAG index: {index_name}")
    except Exception as e:
        # Re-raise to be caught by the main script's try-except block
        raise ConnectionError(f"Failed to create Redis vector store: {e}")


# --- Main Execution Flow ---
if __name__ == "__main__":
    # 1. Read input from stdin
    input_data = sys.stdin.read()
    infos = input_data.split(":!!!!:")
    print("====", infos)
    if len(infos) < 3:
        error_output = {"error": "Invalid input format. Expected: ticket:!!!!:component:!!!!:context"}
        print(json.dumps({"json": error_output}, ensure_ascii=False))
        sys.exit(1)

    ticket = infos[0]
    component = infos[1]
    context = infos[2]

    redis_conn = None # Initialize to None

    try:
        # 2. Attempt Redis connection and store context directly
        print(f"Attempting to connect to Redis at {REDIS_HOST}:{REDIS_PORT}...")
        redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_connect_timeout=5)
        redis_conn.ping() # Test connection
        print("Successfully connected to Redis.")

        train_context = f"[模組]{component}[票號]{ticket}[訊息]{context}"
        # 3. Train RAG vector store with the context
        train_rag_vector_store(context, RAG_INDEX_NAME, metadata={"ticket_id": ticket, "component": component})

        # 4. Prepare and print the final output for n8n
        n8n_final_output = {
            "ticket_id": ticket,
            "context": context,
            "redis_status": "OK",
            "rag_index_status": "OK",
            "rag_index_name": RAG_INDEX_NAME
        }
        print(json.dumps({"json": n8n_final_output}, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        raise e
