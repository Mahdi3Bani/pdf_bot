from fastapi import APIRouter, HTTPException
from app.models.question import Question
from server.app.services.embeddings import PDFProcessor
from server.app.services.llm import query_openai

router = APIRouter()
pdf_processor = PDFProcessor()

@router.post("/")
async def ask_question(question: Question):
    try:
        context = pdf_processor.query_chunks(question.text)
        answer = query_openai(question.text, context)
        return {
            "answer": answer,
            "relevant_chunks": context.split("\n"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")