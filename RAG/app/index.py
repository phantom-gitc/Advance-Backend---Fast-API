from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

load_dotenv()


# Load PDF file from data folder

pdf_path = (Path(__file__).parent / "data" / "sample.pdf")


#Pdf Loader 
loader = PyPDFLoader(str(pdf_path))
documents = loader.load()


# Split documents into chunks 
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400,
    length_function=len,
)


chunks = text_splitter.split_documents(documents=documents)
print(f"Total chunks: {len(chunks)}")


#Embeddings using Gemini API
gemini_api_key = os.getenv("GEMINI_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=gemini_api_key
) 





# Create a vector store 
vector_store = QdrantVectorStore.from_documents(
    chunks,
    embeddings,
    url="http://localhost:6333",
    collection_name="rag_collection",
    force_recreate=True
)



print("Vector store created successfully!")
