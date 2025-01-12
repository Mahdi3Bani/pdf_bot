from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.embeddings import EmbeddingService
from app.services.llm import LLMService
from app.utils.pdf_utils import extract_text_from_pdf

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
embedding_service = EmbeddingService()
llm_service = LLMService()

class Question(BaseModel):
    text: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Extract text from PDF
        text_content = extract_text_from_pdf(file)

        # Create chunks and build FAISS index
        embedding_service.create_chunks(text_content)
        embedding_service.build_index()

        return {"message": "PDF processed successfully", "chunks": len(embedding_service.chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    finally:
        file.file.close()

@app.post("/ask")
async def ask_question(question: Question):
    if not embedding_service.index:
        raise HTTPException(status_code=400, detail="Please upload a PDF first")

    try:
        # Retrieve relevant context from FAISS index
        relevant_chunks = embedding_service.search_index(question.text)
        relevant_context = "\n".join(relevant_chunks)

        # Query the LLM for an answer
        answer = llm_service.get_answer(question.text, relevant_context)

        return {"answer": answer, "relevant_chunks": relevant_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the PDF Question-Answering API!"}


