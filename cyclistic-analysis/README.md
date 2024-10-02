# Studi Kasus Analitik Data Google: Analisis Perjalanan Cyclistic

## Deskripsi Proyek
Proyek ini merupakan bagian dari studi kasus pada kursus **Google Data Analytics Specialization** di Coursera. Analisis ini bertujuan untuk memahami pola perjalanan pengguna sepeda di kota Chicago berdasarkan data yang disediakan oleh Cyclistic, sebuah layanan penyewaan sepeda, untuk membuat strategi pemasaran yang dapat mengubah pengendara biasa menjadi anggota tahunan.

## Cara Menjalankan Proyek
1. Clone repositori ini ke komputer lokal Anda:
   ```bash
   git clone https://github.com/naurahhanaf/portofolio-project.git
   cd cyclistic-analysis
   
2. Unduh dataset di [Cyclistic Trip Data](https://divvy-tripdata.s3.amazonaws.com/index.html)
   ```
   mkdir -p data

   curl -o data/202401-divvy-tripdata.csv https://divvy-tripdata.s3.amazonaws.com/202401-divvy-tripdata.csv
   curl -o data/202402-divvy-tripdata.csv https://divvy-tripdata.s3.amazonaws.com/202402-divvy-tripdata.csv
   curl -o data/202403-divvy-tripdata.csv https://divvy-tripdata.s3.amazonaws.com/202403-divvy-tripdata.csv
   curl -o data/202404-divvy-tripdata.csv https://divvy-tripdata.s3.amazonaws.com/202404-divvy-tripdata.csv
   curl -o data/202405-divvy-tripdata.csv https://divvy-tripdata.s3.amazonaws.com/202405-divvy-tripdata.csv
   curl -o data/202406-divvy-tripdata.csv https://divvy-tripdata.s3.amazonaws.com/202406-divvy-tripdata.csv
   curl -o data/202407-divvy-tripdata.csv https://divvy-tripdata.s3.amazonaws.com/202407-divvy-tripdata.csv
   curl -o data/202408-divvy-tripdata.csv https://divvy-tripdata.s3.amazonaws.com/202408-divvy-tripdata.csv

3. Install package yang dibutuhkan di R console:
   ```
   install.packages("tidyverse")
   install.packages("rmarkdown")

4. Buka file 'analysis.r' dan jalankan kode R untuk melakukan analisis. 
