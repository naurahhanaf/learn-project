import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

# Muat model yang telah dilatih
model = joblib.load('water-potability-prediction/model/model_knn.jlb')

# Fungsi untuk membuat prediksi
def predict_potability(input_data):
    # Melakukan Fitur scalling standardisasi input data
    scaler = StandardScaler()
    input_data_scaled = scaler.fit_transform(input_data)
    # Membuat prediksi menggunakan model yang telah dimuat
    prediction = model.predict(input_data_scaled)
    return prediction

# Tab menu
tab1, tab2, tab3 = st.tabs(['Beranda', 'Prediksi', 'Tentang Dataset'])

# Tab Beranda
with tab1 :
    # Judul
    st.title('Selamat Datang di Website Prediksi Kelayakan Air Minum')
    st.write('''
    Website ini dirancang untuk membantu peniliti untuk menilai potabilitas air berdasarkan berbagai parameter kualitas air. Dengan menggunakan model K-Nearest Neighbors (KNN) yang telah dilatih, website ini memungkinkan pengguna untuk memasukkan data tentang kualitas air dan mendapatkan prediksi apakah air tersebut layak untuk dikonsumsi.
    ''')

    with st.expander('Apa itu model K-Nearest Neighbors (KNN)'):
        st.write('K-NN merupakan algoritma yang digunakan untuk melakukan klasifikasi dengan mencari tetangga terdekat dari data baru berdasarkan jarak.')
	
    st.write('Lihat representasi grafis dari performa model dalam mengklasifikasikan kelayakan air.')
    st.image('water-potability-prediction/app/confusion_matrix.png')

    st.write('''
    *Prediksi yang diberikan oleh website ini hanya berdasarkan model yang telah dilatih dan harus digunakan sebagai referensi tambahan. Untuk penilaian kelayakan air yang akurat, disarankan untuk melakukan uji laboratorium yang lengkap.*
    ''')    

# Tab Prediksi
with tab2:
    # Judul
    st.title('Prediksi Kelayakan Air Minum')

    # Masukkan fitur yang dibutuhkan untuk prediksi
    ph = st.number_input('pH air (0 to 14)', min_value=0.0, max_value=14.0, step=0.01)
    hardness = st.number_input('Hardness (mg/L) : Kapasitas air untuk mengendapkan sabun', step=0.01)
    solids = st.number_input('Solids (ppm) : Total padatan terlarut', step=0.01)
    chloramines = st.number_input('Chloramines (ppm) : Jumlah kloramin', step=0.01)
    sulfate = st.number_input('Sulfate (mg/L) : Jumlah sulfat yang dilarutkan', step=0.01)
    conductivity = st.number_input('Conductivity (μS/cm) : Konduktivitas listrik air', step=0.01)
    organic_carbon = st.number_input('Organic Carbon (ppm) : Jumlah karbon organik', step=0.01)
    trihalomethanes = st.number_input('Trihalomethanes (μg/L) : Jumlah Trihalometana', step=0.01)
    turbidity = st.number_input('Turbidity (NTU) : Kekeruhan air', step=0.01)

    # Membuat DataFrame pandas untuk menyimpan input data dalam format yang sesuai untuk prediksi
    input_data = pd.DataFrame([[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]],
                            columns=['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity'])

    # Tombol untuk membuat prediksi
    if st.button('Prediksi'):
        prediction = predict_potability(input_data)
        if prediction[0] == 1:
            st.success('Air layak minum')
        else:
            st.error('Air tidak layak minum.')

# Tab Tentang Dataset
with tab3:
    st.write('''
             ##### Dataset yang digunakan untuk website ini tersedia di [Kaggle](https://www.kaggle.com/adityakadiwal/water-potability) dengan lisensi [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/). Dataset ini berisi 10 metrik kualitas air dengan 3.276 jenis air yang berbeda.
             
             1. pH air
             
             WHO merekomendasikan batas maksimum pH yang diizinkan untuk kelayakan air adalah 6,5 hingga 8,5.
             
             2. Hardness

             Hardness pada awalnya didefinisikan sebagai kapasitas air untuk mengendapkan sabun yang disebabkan oleh Kalsium dan Magnesium.

             3. Solids (Total dissolved solids - TDS)

             Air memiliki kemampuan untuk melarutkan berbagai macam mineral anorganik dan beberapa mineral atau garam organik seperti kalium, kalsium, natrium, bikarbonat, klorida, magnesium, sulfat dan lain-lain. Air dengan nilai TDS yang tinggi mengindikasikan bahwa air tersebut mengandung mineral yang tinggi. Batas yang diinginkan untuk TDS adalah 500 mg/l dan batas maksimumnya adalah 1000 mg/l yang ditetapkan untuk tujuan minum.

             4. Chloramines

             Klorin dan kloramin adalah disinfektan utama yang digunakan dalam sistem air publik. Kadar klorin hingga 4 miligram per liter (mg/L atau 4 bagian per juta (ppm)) dianggap aman dalam air minum.

             5. Sulfate

             Sulfat adalah zat alami yang ditemukan dalam mineral, tanah, dan batuan. Kadarnya berkisar antara 3 hingga 30 mg/L pada sebagian besar pasokan air tawar, meskipun konsentrasi yang jauh lebih tinggi (1000 mg/L) ditemukan di beberapa lokasi geografis.

             6. Conductivity

             Electrical conductivity (EC) atau konduktivitas listrik sebenarnya mengukur proses ionik suatu larutan yang memungkinkannya mengalirkan arus. Pada umumnya, jumlah padatan terlarut dalam air menentukan konduktivitas listrik. Menurut standar WHO, nilai EC tidak boleh melebihi 400 μS/cm.

             7. Organic_carbon

             Total organic Carbon (TOC) dalah ukuran jumlah total karbon dalam senyawa organik dalam air murni. Menurut US EPA < 2 mg/L sebagai TOC dalam air yang diolah / air minum, dan < 4 mg/Lit dalam air sumber yang digunakan untuk pengolahan.

             8. Trihalomethanes

             THM adalah bahan kimia yang dapat ditemukan dalam air yang diolah dengan klorin. Kadar THM hingga 80 ppm dianggap aman dalam air minum.

             9. Turbidity (Kekeruhan air)

             Kekeruhan merupakan ukuran dari sifat-sifat air yang memancarkan cahaya dan tes ini digunakan untuk menunjukkan kualitas pembuangan limbah sehubungan dengan materi koloid. Nilai yang direkomendasikan WHO yaitu 5,00 NTU.

             10. Potability
             
             Menunjukkan apakah air aman untuk dikonsumsi manusia dimana 1 berarti layak diminum dan 0 berarti tidak layak minum.
             ''')
    
    st.write('### Pratinjau Dataset')
    data = pd.read_csv('water_potability.csv')  # Sesuaikan path dengan lokasi dataset
    st.dataframe(data.head(51))

# Untuk menjalankan Streamlit, jalankan di terminal
# streamlit run app.py
