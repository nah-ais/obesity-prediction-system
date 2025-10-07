# Sistem Prediksi Obesitas

## Deskripsi Proyek

Sistem Prediksi Obesitas adalah aplikasi machine learning yang dapat memprediksi tingkat obesitas seseorang berdasarkan berbagai faktor gaya hidup dan karakteristik fisik. Sistem ini terdiri dari tiga komponen utama:

1. **Machine Learning Model** - Model yang dilatih menggunakan Random Forest dan Gradient Boosting
2. **FastAPI Backend** - API REST untuk melakukan prediksi
3. **Streamlit Frontend** - Interface web yang user-friendly

## Dataset

Dataset yang digunakan adalah `ObesityDataSet2.csv` yang berisi 2111 sampel dengan 17 fitur:

### Fitur Input:
- **Gender**: Jenis kelamin (Male/Female)
- **Age**: Usia dalam tahun
- **Height**: Tinggi badan dalam meter
- **Weight**: Berat badan dalam kilogram
- **family_history_with_overweight**: Riwayat keluarga dengan kelebihan berat badan (yes/no)
- **FAVC**: Konsumsi makanan berkalori tinggi secara sering (yes/no)
- **FCVC**: Frekuensi konsumsi sayuran (1-3)
- **NCP**: Jumlah makanan utama (1-4)
- **CAEC**: Konsumsi makanan di antara waktu makan (no/Sometimes/Frequently/Always)
- **SMOKE**: Merokok (yes/no)
- **CH2O**: Konsumsi air harian (1-3)
- **SCC**: Monitoring konsumsi kalori (yes/no)
- **FAF**: Frekuensi aktivitas fisik (0-3)
- **TUE**: Waktu menggunakan perangkat teknologi (0-2)
- **CALC**: Konsumsi alkohol (no/Sometimes/Frequently/Always)
- **MTRANS**: Transportasi yang digunakan (Walking/Public_Transportation/Automobile/Bike/Motorbike)

### Target Output:
- **NObeyesdad**: Tingkat obesitas dengan 7 kategori:
  - Insufficient_Weight
  - Normal_Weight
  - Overweight_Level_I
  - Overweight_Level_II
  - Obesity_Type_I
  - Obesity_Type_II
  - Obesity_Type_III

## Arsitektur Sistem

```
┌─────────────────┐    HTTP Request    ┌─────────────────┐    Model Prediction    ┌─────────────────┐
│                 │ ──────────────────> │                 │ ─────────────────────> │                 │
│ Streamlit       │                     │ FastAPI         │                        │ Machine Learning│
│ Frontend        │ <────────────────── │ Backend         │ <───────────────────── │ Model           │
│ (Port 8501)     │    JSON Response    │ (Port 8000)     │    Prediction Result   │ (Pickle Files)  │
└─────────────────┘                     └─────────────────┘                        └─────────────────┘
```

## Komponen Sistem

### 1. Machine Learning Model (`obesity_prediction_model.ipynb`)

Model machine learning yang dilatih menggunakan dua algoritma:
- **Random Forest Classifier**
- **Gradient Boosting Classifier**

#### Preprocessing:
- Label encoding untuk variabel kategorikal
- Standard scaling untuk fitur numerik
- Penanganan missing values

#### Model Performance:
- Akurasi: ~96.9%
- Model terbaik dipilih berdasarkan akurasi pada test set
- Model disimpan dalam format pickle untuk deployment

#### File Output:
- `best_obesity_model.pkl`: Model terbaik
- `scaler.pkl`: Standard scaler untuk preprocessing
- `target_label_encoder.pkl`: Label encoder untuk target variable

### 2. FastAPI Backend (`main.py`)

API REST yang menyediakan endpoint untuk prediksi obesitas.

#### Endpoints:
- `GET /`: Root endpoint dengan informasi API
- `GET /health`: Health check untuk status model
- `POST /predict`: Endpoint utama untuk prediksi
- `GET /model-info`: Informasi tentang model yang dimuat

#### Features:
- CORS enabled untuk akses dari frontend
- Input validation menggunakan Pydantic models
- Error handling yang komprehensif
- Automatic model loading saat startup

#### Input Format:
```json
{
  "Gender": "Male",
  "Age": 25,
  "Height": 1.75,
  "Weight": 70,
  "family_history_with_overweight": "no",
  "FAVC": "no",
  "FCVC": 2.0,
  "NCP": 3.0,
  "CAEC": "Sometimes",
  "SMOKE": "no",
  "CH2O": 2.0,
  "SCC": "no",
  "FAF": 1.0,
  "TUE": 1.0,
  "CALC": "no",
  "MTRANS": "Public_Transportation"
}
```

#### Output Format:
```json
{
  "prediction": "Normal_Weight",
  "prediction_code": 1,
  "confidence": 0.996
}
```

### 3. Streamlit Frontend (`app.py`)

Interface web yang user-friendly untuk interaksi dengan sistem prediksi.

#### Features:
- Input form yang intuitif dengan berbagai widget
- Validasi input real-time
- Visualisasi hasil prediksi dengan color coding
- Kalkulasi BMI otomatis
- Rekomendasi kesehatan berdasarkan hasil prediksi
- Status koneksi API real-time
- Responsive design

#### UI Components:
- Sidebar untuk input data
- Main area untuk summary dan hasil prediksi
- Color-coded prediction results
- Health recommendations
- API status indicator

## Instalasi dan Penggunaan

### Prerequisites:
```bash
pip install pandas scikit-learn fastapi uvicorn streamlit requests
```

### Menjalankan Sistem:

1. **Start FastAPI Backend:**
```bash
python main.py
```
Server akan berjalan di `http://localhost:8000`

2. **Start Streamlit Frontend:**
```bash
streamlit run app.py
```
Aplikasi web akan tersedia di `http://localhost:8501`

### Testing API:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Gender": "Male",
    "Age": 25,
    "Height": 1.75,
    "Weight": 70,
    "family_history_with_overweight": "no",
    "FAVC": "no",
    "FCVC": 2.0,
    "NCP": 3.0,
    "CAEC": "Sometimes",
    "SMOKE": "no",
    "CH2O": 2.0,
    "SCC": "no",
    "FAF": 1.0,
    "TUE": 1.0,
    "CALC": "no",
    "MTRANS": "Public_Transportation"
  }'
```

## Hasil Testing

### API Testing:
- ✅ Health check endpoint berfungsi normal
- ✅ Prediction endpoint memberikan hasil yang akurat
- ✅ Model loading berhasil dengan confidence ~99.6%
- ✅ Error handling berfungsi dengan baik

### Frontend Testing:
- ✅ Streamlit app berhasil dijalankan
- ✅ Interface responsif dan user-friendly
- ✅ Koneksi ke API backend berhasil
- ✅ Hasil prediksi ditampilkan dengan baik

### Sample Prediction:
Input: Male, 25 tahun, 175cm, 70kg dengan gaya hidup sehat
Output: Normal_Weight dengan confidence 99.6%

## Keunggulan Sistem

1. **Akurasi Tinggi**: Model mencapai akurasi ~96.9%
2. **User-Friendly**: Interface web yang mudah digunakan
3. **Real-time Prediction**: Prediksi instan melalui API
4. **Scalable Architecture**: Pemisahan frontend dan backend
5. **Comprehensive Features**: Termasuk BMI calculator dan rekomendasi kesehatan
6. **Error Handling**: Penanganan error yang robust
7. **Documentation**: API documentation otomatis via FastAPI

## Limitasi dan Disclaimer

1. **Data Dependency**: Akurasi prediksi bergantung pada kualitas data training
2. **Medical Disclaimer**: Hasil prediksi hanya untuk referensi, bukan pengganti konsultasi medis
3. **Feature Engineering**: Bisa ditingkatkan dengan feature engineering yang lebih advanced
4. **Cross-validation**: Evaluasi model bisa diperkuat dengan cross-validation

## Pengembangan Selanjutnya

1. **Model Improvement**: 
   - Hyperparameter tuning
   - Ensemble methods
   - Deep learning approaches

2. **Feature Enhancement**:
   - Additional health metrics
   - Lifestyle tracking
   - Historical data analysis

3. **Deployment**:
   - Docker containerization
   - Cloud deployment (AWS/GCP/Azure)
   - CI/CD pipeline

4. **UI/UX Improvements**:
   - Mobile responsiveness
   - Data visualization
   - User authentication

## Kesimpulan

Sistem Prediksi Obesitas telah berhasil dikembangkan dengan arsitektur yang scalable dan user-friendly. Sistem ini menggabungkan machine learning yang akurat dengan interface yang mudah digunakan, memberikan solusi end-to-end untuk prediksi tingkat obesitas berdasarkan faktor gaya hidup.

---
