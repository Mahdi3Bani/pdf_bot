from fastapi import APIRouter, UploadFile, File, HTTPException
from server.app.services.embeddings import PDFProcessor

router = APIRouter()
pdf_processor = PDFProcessor()

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        chunks_count = pdf_processor.process_pdf(file)
        return {"message": "PDF processed successfully", "chunks": chunks_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
