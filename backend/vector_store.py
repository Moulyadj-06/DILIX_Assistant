import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import PyPDF2  # pip install PyPDF2
import re
import pdfplumber

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "dilix-memory")

# -----------------------------
# Initialize Pinecone client
# -----------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

# -----------------------------
# Create index if not exists
# -----------------------------
existing_indexes = [idx["name"] for idx in pc.list_indexes()]
if PINECONE_INDEX_NAME not in existing_indexes:
    print(f"🆕 Creating Pinecone index: {PINECONE_INDEX_NAME}")
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,  # Must match embedding size
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
else:
    print(f"✅ Index already exists: {PINECONE_INDEX_NAME}")

# -----------------------------
# Connect to the index
# -----------------------------
index = pc.Index(PINECONE_INDEX_NAME)
print(f"✅ Connected to Pinecone index: {PINECONE_INDEX_NAME}")

# -----------------------------
# Initialize embedding model
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim embeddings

# -----------------------------
# Helper functions
# -----------------------------
def get_text_embedding(text):
    return model.encode(text).tolist()

def parse_pdf_qa(file_path):
    qa_pairs = []
    pdf_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            pdf_text += page.extract_text() + "\n"

    matches = re.findall(r"Q:\s*(.*?)\s*A:\s*(.*?)(?=(\nQ:|\Z))", pdf_text, re.DOTALL)
    for m in matches:
        question, answer = m[0].strip(), m[1].strip()
        qa_pairs.append({"question": question, "answer": answer})

    return qa_pairs


def add_to_vector_store(file_path):
    qa_pairs = parse_pdf_qa(file_path)
    print(f"📄 Found {len(qa_pairs)} Q&A pairs in {file_path}")

    for qa in qa_pairs:
        text = qa["question"] + " " + qa["answer"]
        vector_data = [{
            "id": str(abs(hash(text)))[:12],
            "values": get_text_embedding(text),
            "metadata": {
                "source": os.path.basename(file_path),
                "question": qa["question"],
                "answer": qa["answer"]  # ✅ store full answer
            }
        }]

        index.upsert(vectors=vector_data)
    print(f"✅ Added all Q&A pairs from {file_path} to Pinecone")


def query_vector_store(question, top_k=3):
    query_vector = get_text_embedding(question)
    response = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    results = []
    for match in response.matches:
        results.append({
            "question": match.metadata.get("question"),
            "answer": match.metadata.get("answer")  # optional: store full answer in metadata if needed
        })
    return results
