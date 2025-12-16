# 🧠 Backend - Sistem Prediksi & Monitoring Siswa (EduFocus AI)

Backend ini adalah pusat logika untuk aplikasi **Sistem Prediksi & Monitoring Siswa**. Dibangun menggunakan **FastAPI** (Python), backend ini menangani manajemen data siswa, autentikasi pengguna, serta integrasi model Machine Learning (**Random Forest**) untuk memprediksi potensi kelulusan siswa.

## 🚀 Fitur Utama

* **RESTful API:** Arsitektur API yang cepat dan standar.
* **Machine Learning Integration:** Memuat model `.pkl` (Random Forest) untuk prediksi *real-time*.
* **Data Preprocessing:** Menangani konversi data mentah (kategorikal) menjadi numerik (Encoding & Scaling) sebelum diproses AI.
* **Secure Authentication:** Sistem login aman menggunakan **JWT (JSON Web Token)** dan Hashing Password.
* **Role Protection:** Middleware untuk membatasi akses endpoint hanya bagi pengguna terdaftar.
* **Database Management:** CRUD (Create, Read, Update, Delete) data siswa terintegrasi dengan MySQL.

## 🛠️ Teknologi yang Digunakan

* **Language:** Python 3.9+
* **Framework:** FastAPI
* **Database ORM:** SQLAlchemy
* **Database Driver:** MySQL Connector
* **ML Libraries:** Scikit-learn, Pandas, Numpy
* **Authentication:** Python-Jose (JWT), Passlib (Bcrypt/PBKDF2)
* **Server:** Uvicorn

⚙️ Cara Instalasi & Menjalankan
Ikuti langkah berikut untuk menjalankan backend di komputer lokal.

1. Persiapan Database
Pastikan Anda memiliki XAMPP atau MySQL Server yang berjalan. Buat database baru di phpMyAdmin atau SQL Client:

SQL

CREATE DATABASE db_prediksi_siswa;
2. Setup Environment Python
Buka terminal di dalam folder backend_prediction.

Buat Virtual Environment:

python -m venv env
Aktifkan Virtual Environment:
Windows: env\Scripts\activate
Mac/Linux: source env/bin/activate

3. Install Dependencies
Install semua library yang dibutuhkan:

pip install fastapi uvicorn sqlalchemy mysql-connector-python scikit-learn pandas python-jose[cryptography] passlib[bcrypt] python-multipart
4. Konfigurasi .env
Buat file baru bernama .env di root folder, lalu isi konfigurasi berikut (sesuaikan dengan setting MySQL Anda):
Cuplikan kode
# Format: mysql+mysqlconnector://user:password@host:port/nama_database
DATABASE_URL=mysql+mysqlconnector://root:@localhost:3306/db_prediksi_siswa
# Kunci rahasia untuk generate Token (Bisa isi string acak apa saja)
SECRET_KEY=rahasia_super_aman_12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MODEL_PATH=ml_models/model_student_performance.pkl
5. Menjalankan Server
Jalankan perintah berikut untuk menyalakan server:
python -m app.main
Jika berhasil, akan muncul pesan: INFO: Application startup complete. INFO: Uvicorn running on http://0.0.0.0:8000

📚 Dokumentasi API (Swagger UI)
FastAPI menyediakan dokumentasi interaktif secara otomatis. Setelah server berjalan, buka browser dan akses:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Endpoint Penting:
POST /api/v1/auth/token : Login Admin (Get Token)

POST /api/v1/predict/ : Input Data & Prediksi AI

GET /api/v1/students/ : Ambil semua data siswa

GET /api/v1/students/dashboard : Statistik Metadata Dashboard

👤 Akun Default
Saat pertama kali dijalankan, Anda perlu mendaftarkan user admin pertama melalui endpoint /api/v1/auth/register di Swagger UI, atau secara manual insert ke database.

Developed by [Nama Anda]


### Tips Tambahan:
Jangan lupa jalankan perintah ini di terminal Backend agar file `requirements.txt` ter-generate otomatis (berguna kalau mau di-upload ke GitHub atau dikasih ke Dosen):

```bash
pip freeze > requirements.txt
