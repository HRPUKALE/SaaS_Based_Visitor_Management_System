import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# === Config ===
CHROMA_DIR = "./employee_db"
COLLECTION_NAME = "employee_collection"

# === Load ChromaDB client ===
client = chromadb.PersistentClient(path=CHROMA_DIR)

# === Load embedding function (same as before) ===
embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# === Load the same collection ===
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)

# === Take user input ===
user_input = input("👤 Enter employee name or query: ")

# === Query ChromaDB ===
results = collection.query(
    query_texts=[user_input],
    n_results=3  # You can change to 5 or more
)

# === Print Results ===
print("\n🔍 Top Matches:")
for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
    print(f"- {doc} (Employee: {meta['employee_name']}, Dept: {meta['department']})")
