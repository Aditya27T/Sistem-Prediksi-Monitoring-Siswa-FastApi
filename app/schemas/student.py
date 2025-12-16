from pydantic import BaseModel
from typing import Optional, Dict, Any

class StudentInputSchema(BaseModel):
    nama_siswa: str
    school: str
    sex: str
    age: int
    address: str
    famsize: str
    Pstatus: str
    guardian: str
    reason: str

    Medu: int
    Fedu: int
    Mjob: str
    Fjob: str
    traveltime: int
    internet: str
    romantic: str
    famrel: int
    freetime: int
    goout: int
    Dalc: int
    Walc: int
    health: int
    activities: str
    nursery: str

    studytime: int
    failures: int
    schoolsup: str
    famsup: str
    paid: str
    higher: str
    absences: int
    G1: int
    G2: int

    class Config:
        from_attributes = True

class PredictionResponse(BaseModel):
    status: str
    nama: str
    prediksi_label: str
    probabilitas: float
    pesan: str
    raw_data: Optional[Dict[str, Any]] = None 
    processed_data: Optional[Dict[str, Any]] = None 
class StudentListSchema(BaseModel):
    id_siswa: int
    nama_siswa: str
    school: str
    sex: str
    age: int
    hasil_prediksi: Optional[str] = None
    probabilitas: Optional[float] = None
    created_at: Optional[object] = None

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_siswa: int
    total_lulus: int
    total_berisiko: int
    rata_rata_g1: float
    rata_rata_g2: float
    persentase_kelulusan: float
    gender_m: int
    gender_f: int
    school_gp: int
    school_ms: int
    avg_studytime: float
    avg_absences: float
    