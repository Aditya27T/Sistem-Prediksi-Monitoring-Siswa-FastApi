from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.student import StudentInputSchema, PredictionResponse
from app.services.ml_service import ml_service
from app.services.student_service import create_student 
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
def predict_student(
    data: StudentInputSchema, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    input_data = data.dict()

    try:
        hasil_ai = ml_service.predict(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")

    try:
        create_student(db, input_data, hasil_ai) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    return {
        "status": "success",
        "nama": data.nama_siswa,
        "prediksi_label": hasil_ai['label'],
        "probabilitas": hasil_ai['score'],
        "pesan": hasil_ai['pesan'],
        "raw_data": hasil_ai.get('raw_data'),
        "processed_data": hasil_ai.get('processed_data')
    }