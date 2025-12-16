import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Sistem Prediksi Siswa"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost/db_prediksi_siswa")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "ml_models/model_student_performance.pkl")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "defaultsecretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()