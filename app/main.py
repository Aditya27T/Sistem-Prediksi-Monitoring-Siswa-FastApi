import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import predict, students, auth
from app.db import models
from app.db.session import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistem Prediksi Siswa API",
    version="1.0.0",
    description="Backend cerdas menggunakan Random Forest & FastAPI"
)

# 3. Setup CORS (PENTING BUAT REACT)
# Agar React (port 3000/5173) boleh akses API ini (port 8000)
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(predict.router, prefix="/api/v1/predict", tags=["Prediksi"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Manajemen Data"])

@app.get("/")
def root():
    return {"message": "Server Prediksi Siswa Online! 🚀"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)