import pickle
import pandas as pd
from app.core.config import settings

class MLService:
    def __init__(self):
        self.model = None
        self.encoders = None
        self.scaler = None
        self.feature_names = None
        self.cols_num = None
        self.cols_text = None
        self.load_model()

    def load_model(self):
        try:
            print(f"Loading model from: {settings.MODEL_PATH}")
            with open(settings.MODEL_PATH, 'rb') as f:
                packet = pickle.load(f)
                self.model = packet['model']
                self.encoders = packet['encoders']
                self.scaler = packet['scaler']
                self.feature_names = packet['feature_names']
                self.cols_num = packet['cols_num']
                self.cols_text = packet['cols_text']
            print("ML Model Berhasil Dimuat!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Pastikan file .pkl ada di folder ml_models/")

    def predict(self, input_data: dict):
        if not self.model:
            raise Exception("Model belum dimuat (Cek log error)")

        df = pd.DataFrame([input_data])
        df_processed = df.copy()

        # 2. Preprocessing: Encoding (Huruf -> Angka)
        for col in self.cols_text:
            if col in df.columns:
                try:
                    # Transformasi data, simpan hasilnya ke df_processed
                    transformed_val = self.encoders[col].transform(df[col])
                    df_processed[col] = transformed_val # Simpan angka
                    df[col] = transformed_val           # Pakai untuk prediksi
                except:
                    df[col] = 0
                    df_processed[col] = 0

        # 3. Preprocessing: Scaling (Normalisasi Angka)
        # Pastikan kolom angka ada semua
        for col in self.cols_num:
            if col not in df.columns:
                df[col] = 0
                df_processed[col] = 0
        
        # Transform angka pakai rumus scaler yang sudah disimpan
        scaled_values = self.scaler.transform(df[self.cols_num])
        
        # Simpan hasil scaling ke DataFrame
        df[self.cols_num] = scaled_values
        df_processed[self.cols_num] = scaled_values

        # 4. Urutkan Kolom (Wajib sama dengan saat training)
        df = df[self.feature_names]

        # 5. Prediksi
        pred_label = self.model.predict(df)[0]       # Hasil: 1 atau 0
        pred_proba = self.model.predict_proba(df)[0][1] * 100 # Hasil: % Lulus

        return {
            "label": "Lulus" if pred_label == 1 else "Berisiko",
            "score": round(pred_proba, 2),
            "pesan": "Pertahankan prestasi!" if pred_label == 1 else "Perlu bimbingan intensif segera.",
            "raw_data": input_data,
            "processed_data": df_processed.to_dict(orient='records')[0]
        }

# Singleton Instance
ml_service = MLService()