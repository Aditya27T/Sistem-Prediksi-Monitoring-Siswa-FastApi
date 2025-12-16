from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Tabel PROFIL
class SiswaProfil(Base):
    __tablename__ = "siswa_profil"

    id_siswa = Column(Integer, primary_key=True, index=True)
    nama_siswa = Column(String(100))
    school = Column(String(10))  # GP/MS
    sex = Column(String(5))      # F/M
    age = Column(Integer)
    address = Column(String(5))
    famsize = Column(String(5))
    Pstatus = Column(String(5))
    guardian = Column(String(20))
    reason = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

    latar_belakang = relationship("LatarBelakang", back_populates="siswa", uselist=False)
    akademik = relationship("RekamAkademik", back_populates="siswa", uselist=False)


# Tabel LATAR BELAKANG
class LatarBelakang(Base):
    __tablename__ = "latar_belakang"

    id_lb = Column(Integer, primary_key=True, index=True)
    id_siswa = Column(Integer, ForeignKey("siswa_profil.id_siswa"))
    
    Medu = Column(Integer)
    Fedu = Column(Integer)
    Mjob = Column(String(50))
    Fjob = Column(String(50))
    traveltime = Column(Integer)
    internet = Column(String(5))
    romantic = Column(String(5))
    famrel = Column(Integer)
    freetime = Column(Integer)
    goout = Column(Integer)
    Dalc = Column(Integer)
    Walc = Column(Integer)
    health = Column(Integer)
    activities = Column(String(5))
    nursery = Column(String(5))

    siswa = relationship("SiswaProfil", back_populates="latar_belakang")


# Tabel REKAM AKADEMIK
class RekamAkademik(Base):
    __tablename__ = "rekam_akademik"

    id_ra = Column(Integer, primary_key=True, index=True)
    id_siswa = Column(Integer, ForeignKey("siswa_profil.id_siswa"))
    
    studytime = Column(Integer)
    failures = Column(Integer)
    schoolsup = Column(String(5))
    famsup = Column(String(5))
    paid = Column(String(5))
    higher = Column(String(5))
    absences = Column(Integer)
    G1 = Column(Integer)
    G2 = Column(Integer)
    
    # Hasil AI
    hasil_prediksi = Column(String(20))
    probabilitas = Column(Float)
    tanggal_prediksi = Column(TIMESTAMP, server_default=func.now())

    siswa = relationship("SiswaProfil", back_populates="akademik")

# Tabel USER (Admin/Guru)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(100), nullable=True)
    role = Column(String(20), default="admin") # admin / guru
    created_at = Column(TIMESTAMP, server_default=func.now())