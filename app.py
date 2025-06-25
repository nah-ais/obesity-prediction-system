import streamlit as st
import requests
import json

# Set page config
st.set_page_config(
    page_title="Obesity Prediction App",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-result {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .normal-weight {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .overweight {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    .obesity {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .insufficient-weight {
        background-color: #cce5ff;
        color: #004085;
        border: 1px solid #99d6ff;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🏥 Obesity Prediction System</h1>', unsafe_allow_html=True)

# API endpoint
API_URL = "http://localhost:8000"

# Sidebar for input
st.sidebar.header("📝 Input Data Pasien")

# Input fields
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
age = st.sidebar.number_input("Age (tahun)", min_value=1, max_value=120, value=25)
height = st.sidebar.number_input("Height (meter)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
weight = st.sidebar.number_input("Weight (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1)

family_history = st.sidebar.selectbox("Family History with Overweight", ["yes", "no"])
favc = st.sidebar.selectbox("Frequent Consumption of High Caloric Food", ["yes", "no"])
fcvc = st.sidebar.slider("Frequency of Consumption of Vegetables (1-3)", 1.0, 3.0, 2.0, 0.1)
ncp = st.sidebar.slider("Number of Main Meals (1-4)", 1.0, 4.0, 3.0, 0.1)

caec = st.sidebar.selectbox("Consumption of Food Between Meals", ["no", "Sometimes", "Frequently", "Always"])
smoke = st.sidebar.selectbox("Smoke", ["yes", "no"])
ch2o = st.sidebar.slider("Consumption of Water Daily (1-3)", 1.0, 3.0, 2.0, 0.1)
scc = st.sidebar.selectbox("Calories Consumption Monitoring", ["yes", "no"])

faf = st.sidebar.slider("Physical Activity Frequency (0-3)", 0.0, 3.0, 1.0, 0.1)
tue = st.sidebar.slider("Time Using Technology Devices (0-2)", 0.0, 2.0, 1.0, 0.1)
calc = st.sidebar.selectbox("Consumption of Alcohol", ["no", "Sometimes", "Frequently", "Always"])
mtrans = st.sidebar.selectbox("Transportation Used", 
                             ["Walking", "Public_Transportation", "Automobile", "Bike", "Motorbike"])

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Input Summary")
    
    # Display input summary
    input_data = {
        "Gender": gender,
        "Age": age,
        "Height": height,
        "Weight": weight,
        "family_history_with_overweight": family_history,
        "FAVC": favc,
        "FCVC": fcvc,
        "NCP": ncp,
        "CAEC": caec,
        "SMOKE": smoke,
        "CH2O": ch2o,
        "SCC": scc,
        "FAF": faf,
        "TUE": tue,
        "CALC": calc,
        "MTRANS": mtrans
    }
    
    # Calculate BMI
    bmi = weight / (height ** 2)
    st.metric("BMI", f"{bmi:.2f}")
    
    # Display input data in a nice format
    st.subheader("Data Input:")
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write(f"**Gender:** {gender}")
        st.write(f"**Age:** {age} tahun")
        st.write(f"**Height:** {height} m")
        st.write(f"**Weight:** {weight} kg")
        st.write(f"**Family History:** {family_history}")
        st.write(f"**High Caloric Food:** {favc}")
        st.write(f"**Vegetables Frequency:** {fcvc}")
        st.write(f"**Main Meals:** {ncp}")
    
    with col_b:
        st.write(f"**Food Between Meals:** {caec}")
        st.write(f"**Smoke:** {smoke}")
        st.write(f"**Water Consumption:** {ch2o}")
        st.write(f"**Calorie Monitoring:** {scc}")
        st.write(f"**Physical Activity:** {faf}")
        st.write(f"**Technology Use:** {tue}")
        st.write(f"**Alcohol:** {calc}")
        st.write(f"**Transportation:** {mtrans}")

with col2:
    st.header("🔮 Prediction")
    
    # Predict button
    if st.button("🚀 Predict Obesity Level", type="primary", use_container_width=True):
        try:
            # Make API request
            response = requests.post(f"{API_URL}/predict", json=input_data)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result["prediction"]
                confidence = result["confidence"]
                
                # Display result with appropriate styling
                if "Normal_Weight" in prediction:
                    st.markdown(f'<div class="prediction-result normal-weight">✅ {prediction}<br>Confidence: {confidence:.2%}</div>', 
                               unsafe_allow_html=True)
                elif "Insufficient_Weight" in prediction:
                    st.markdown(f'<div class="prediction-result insufficient-weight">⚠️ {prediction}<br>Confidence: {confidence:.2%}</div>', 
                               unsafe_allow_html=True)
                elif "Overweight" in prediction:
                    st.markdown(f'<div class="prediction-result overweight">⚠️ {prediction}<br>Confidence: {confidence:.2%}</div>', 
                               unsafe_allow_html=True)
                else:  # Obesity levels
                    st.markdown(f'<div class="prediction-result obesity">🚨 {prediction}<br>Confidence: {confidence:.2%}</div>', 
                               unsafe_allow_html=True)
                
                # Additional information
                st.subheader("📋 Recommendation")
                if "Normal_Weight" in prediction:
                    st.success("Pertahankan pola hidup sehat Anda!")
                elif "Insufficient_Weight" in prediction:
                    st.warning("Konsultasikan dengan dokter untuk program penambahan berat badan yang sehat.")
                elif "Overweight" in prediction:
                    st.warning("Pertimbangkan untuk mengurangi berat badan dengan diet seimbang dan olahraga teratur.")
                else:
                    st.error("Sangat disarankan untuk berkonsultasi dengan dokter untuk program penurunan berat badan.")
                
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Tidak dapat terhubung ke API. Pastikan server FastAPI berjalan di http://localhost:8000")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("### 📚 About")
st.info("""
**Obesity Prediction System** menggunakan machine learning untuk memprediksi tingkat obesitas berdasarkan berbagai faktor gaya hidup dan karakteristik fisik.

**Kategori Prediksi:**
- Insufficient Weight
- Normal Weight  
- Overweight Level I
- Overweight Level II
- Obesity Type I
- Obesity Type II
- Obesity Type III

**Disclaimer:** Hasil prediksi ini hanya untuk referensi dan tidak menggantikan konsultasi medis profesional.
""")

# API Status check
try:
    health_response = requests.get(f"{API_URL}/health", timeout=5)
    if health_response.status_code == 200:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Error")
except:
    st.sidebar.error("❌ API Disconnected")

