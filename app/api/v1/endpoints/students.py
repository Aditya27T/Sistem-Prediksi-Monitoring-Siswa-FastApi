from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import User
from app.api.deps import get_current_user 
from app.services.student_service import (
    get_all_students, delete_student, get_dashboard_stats, 
    get_student_detail, update_student
)
from app.services.ml_service import ml_service 
from app.schemas.student import StudentListSchema, DashboardStats, StudentInputSchema

router = APIRouter()

@router.get("/", response_model=List[StudentListSchema])
def read_students(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return get_all_students(db)

@router.get("/dashboard", response_model=DashboardStats)
def read_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_stats(db)

@router.get("/{id_siswa}")
def read_student_detail(
    id_siswa: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = get_student_detail(db, id_siswa)
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")
    flat_data = {
        "nama_siswa": student.nama_siswa,
        "school": student.school,
        "sex": student.sex,
        "age": student.age,
        "address": student.address,
        "famsize": student.famsize,
        "Pstatus": student.Pstatus,
        "guardian": student.guardian,
        "reason": student.reason,
        "Medu": student.latar_belakang.Medu,
        "Fedu": student.latar_belakang.Fedu,
        "Mjob": student.latar_belakang.Mjob,
        "Fjob": student.latar_belakang.Fjob,
        "traveltime": student.latar_belakang.traveltime,
        "internet": student.latar_belakang.internet,
        "romantic": student.latar_belakang.romantic,
        "famrel": student.latar_belakang.famrel,
        "freetime": student.latar_belakang.freetime,
        "goout": student.latar_belakang.goout,
        "Dalc": student.latar_belakang.Dalc,
        "Walc": student.latar_belakang.Walc,
        "health": student.latar_belakang.health,
        "activities": student.latar_belakang.activities,
        "nursery": student.latar_belakang.nursery,
        "studytime": student.akademik.studytime,
        "failures": student.akademik.failures,
        "schoolsup": student.akademik.schoolsup,
        "famsup": student.akademik.famsup,
        "paid": student.akademik.paid,
        "higher": student.akademik.higher,
        "absences": student.akademik.absences,
        "G1": student.akademik.G1,
        "G2": student.akademik.G2
    }
    return flat_data

@router.delete("/{id_siswa}")
def remove_student(
    id_siswa: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = delete_student(db, id_siswa)
    if not success:
        raise HTTPException(status_code=404, detail="Gagal hapus, ID tidak ditemukan")
    return {"status": "success"}

@router.put("/{id_siswa}")
def edit_student(
    id_siswa: int, 
    data: StudentInputSchema, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    input_data = data.dict()
    
    try:
        new_prediction = ml_service.predict(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses AI: {e}")
    success = update_student(db, id_siswa, input_data, prediction_result=new_prediction)
    if not success:
        raise HTTPException(status_code=404, detail="Gagal update")
    
    return {"status": "success", "message": "Data & Analisis berhasil diperbarui"}