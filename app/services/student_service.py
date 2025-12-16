from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import Optional
from app.db.models import SiswaProfil, LatarBelakang, RekamAkademik

def create_student(db: Session, data: dict, prediction_result: dict):
    try:
        profil = SiswaProfil(
            nama_siswa=data['nama_siswa'], school=data['school'], sex=data['sex'],
            age=data['age'], address=data['address'], famsize=data['famsize'],
            Pstatus=data['Pstatus'], guardian=data['guardian'], reason=data['reason']
        )
        db.add(profil)
        db.commit()      
        db.refresh(profil)
        
        new_id = profil.id_siswa 
        latar = LatarBelakang(
            id_siswa=new_id,
            Medu=data['Medu'], Fedu=data['Fedu'], Mjob=data['Mjob'], Fjob=data['Fjob'],
            traveltime=data['traveltime'], internet=data['internet'], romantic=data['romantic'],
            famrel=data['famrel'], freetime=data['freetime'], goout=data['goout'],
            Dalc=data['Dalc'], Walc=data['Walc'], health=data['health'],
            activities=data['activities'], nursery=data['nursery']
        )
        db.add(latar)
        akademik = RekamAkademik(
            id_siswa=new_id,
            studytime=data['studytime'], failures=data['failures'], schoolsup=data['schoolsup'],
            famsup=data['famsup'], paid=data['paid'], higher=data['higher'],
            absences=data['absences'], G1=data['G1'], G2=data['G2'],
 
            hasil_prediksi=prediction_result['label'],
            probabilitas=prediction_result['score']
        )
        db.add(akademik)

        db.commit() 
        return new_id

    except Exception as e:
        db.rollback()
        raise e

def get_all_students(db: Session):
    results = db.query(
        SiswaProfil.id_siswa, SiswaProfil.nama_siswa, SiswaProfil.school,
        SiswaProfil.sex, SiswaProfil.age, SiswaProfil.created_at,
        RekamAkademik.hasil_prediksi, RekamAkademik.probabilitas
    ).join(RekamAkademik, SiswaProfil.id_siswa == RekamAkademik.id_siswa).all()
    return results

def get_student_detail(db: Session, id_siswa: int):
    student = db.query(SiswaProfil).filter(SiswaProfil.id_siswa == id_siswa).first()
    return student

def update_student(db: Session, id_siswa: int, data: dict, prediction_result: Optional[dict] = None):
    profil = db.query(SiswaProfil).filter(SiswaProfil.id_siswa == id_siswa).first()
    latar = db.query(LatarBelakang).filter(LatarBelakang.id_siswa == id_siswa).first()
    akademik = db.query(RekamAkademik).filter(RekamAkademik.id_siswa == id_siswa).first()

    if not profil:
        return False

    try:
        profil.nama_siswa = data['nama_siswa']
        profil.age = data['age']
        profil.address = data['address']
        profil.school = data['school']
        profil.sex = data['sex']
        profil.famsize = data['famsize']
        profil.Pstatus = data['Pstatus']
        profil.guardian = data['guardian']
        profil.reason = data['reason']

        if latar:
            latar.Medu = data['Medu']
            latar.Fedu = data['Fedu']
            latar.Mjob = data['Mjob']
            latar.Fjob = data['Fjob']
            latar.traveltime = data['traveltime']
            latar.internet = data['internet']
            latar.romantic = data['romantic']
            latar.famrel = data['famrel']
            latar.freetime = data['freetime']
            latar.goout = data['goout']
            latar.Dalc = data['Dalc']
            latar.Walc = data['Walc']
            latar.health = data['health']
            latar.activities = data['activities']
            latar.nursery = data['nursery']

        if akademik:
            akademik.G1 = data['G1']
            akademik.G2 = data['G2']
            akademik.absences = data['absences']
            akademik.studytime = data['studytime']
            akademik.failures = data['failures']
            akademik.schoolsup = data['schoolsup']
            akademik.famsup = data['famsup']
            akademik.paid = data['paid']
            akademik.higher = data['higher']
            
            if prediction_result:
                akademik.hasil_prediksi = prediction_result['label']
                akademik.probabilitas = prediction_result['score']

        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e


def delete_student(db: Session, id_siswa: int):
    try:
        db.query(LatarBelakang).filter(LatarBelakang.id_siswa == id_siswa).delete()
        db.query(RekamAkademik).filter(RekamAkademik.id_siswa == id_siswa).delete()
        rows_deleted = db.query(SiswaProfil).filter(SiswaProfil.id_siswa == id_siswa).delete()
        
        db.commit()
        
        if rows_deleted > 0:
            return True
        return False

    except Exception as e:
        db.rollback()
        raise e

def get_dashboard_stats(db: Session):
    total = db.query(SiswaProfil).count()
    
    if total == 0:
        return {
            "total_siswa": 0, "total_lulus": 0, "total_berisiko": 0,
            "rata_rata_g1": 0, "rata_rata_g2": 0, "persentase_kelulusan": 0,
            "gender_m": 0, "gender_f": 0,
            "school_gp": 0, "school_ms": 0,
            "avg_studytime": 0, "avg_absences": 0
        }

    lulus = db.query(RekamAkademik).filter(RekamAkademik.hasil_prediksi == 'Lulus').count()
    berisiko = db.query(RekamAkademik).filter(RekamAkademik.hasil_prediksi == 'Berisiko').count()
    avg_g1 = db.query(func.avg(RekamAkademik.G1)).scalar() or 0
    avg_g2 = db.query(func.avg(RekamAkademik.G2)).scalar() or 0
    
    gender_m = db.query(SiswaProfil).filter(SiswaProfil.sex == 'M').count()
    gender_f = db.query(SiswaProfil).filter(SiswaProfil.sex == 'F').count()
    
    school_gp = db.query(SiswaProfil).filter(SiswaProfil.school == 'GP').count()
    school_ms = db.query(SiswaProfil).filter(SiswaProfil.school == 'MS').count()

    avg_studytime = db.query(func.avg(RekamAkademik.studytime)).scalar() or 0
    avg_absences = db.query(func.avg(RekamAkademik.absences)).scalar() or 0

    return {
        "total_siswa": total,
        "total_lulus": lulus,
        "total_berisiko": berisiko,
        "rata_rata_g1": round(avg_g1, 2),
        "rata_rata_g2": round(avg_g2, 2),
        "persentase_kelulusan": round((lulus / total) * 100, 1) if total > 0 else 0,
        
        "gender_m": gender_m,
        "gender_f": gender_f,
        "school_gp": school_gp,
        "school_ms": school_ms,
        "avg_studytime": round(avg_studytime, 2),
        "avg_absences": round(avg_absences, 1)
    }