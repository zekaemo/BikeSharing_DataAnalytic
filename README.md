# Bike Sharing Data Analysis

**Nama**: Zeka Emo

**Email**: zeka.emo30@gmail.com 

# Project Description

Proyek ini bertujuan untuk menganalisis dataset penyewaan sepeda guna memperoleh wawasan tentang perilaku pengguna, seperti waktu penyewaan terbanyak, pengaruh cuaca, serta perbedaan antara pengguna kasual dan terdaftar. Analisis dilakukan dengan menggunakan Python dan Pandas, sementara visualisasinya dibuat menggunakan Streamlit.

## Outline Program

### Program ini bertujuan untuk menjawab beberapa pertanyaan analisis data berikut:
1. Bagaimana pengaruh cuaca terhadap jumlah penyewaan sepeda?
2. Apakah terdapat perbedaan kebiasaan penyewaan sepeda pada hari libur dibandingkan dengan hari biasa?
3. Pada pukul berapa sepeda paling banyak disewa dalam sehari?
4. Pada hari apa dalam seminggu sepeda paling banyak disewa?
5. Bagaimana pengaruh suhu udara yang panas atau dingin terhadap jumlah sepeda yang disewa?


### Data Wrangling: 
   - Mengubah tipe data, membersihkan data, dan melakukan pemrosesan awal dataset.
   
### Exploratory Data Analysis (EDA)
   - Analisis pola penyewaan sepeda berdasarkan cuaca, waktu, hari libur, dan suhu udara.

### Visualizing Data
   - Menampilkan grafik bar dan garis untuk menunjukkan hubungan antara variabel-variabel yang dianalisis.

### Drawing Conclusions
   - Menyajikan kesimpulan dari hasil analisis data.

### Dataset yang Digunakan
- `day.csv`: Berisi data penyewaan sepeda harian.
- `hour.csv`: Berisi data penyewaan sepeda per jam.

## Cara Menjalankan Program

### Prasyarat
- Python 3.x sudah terinstal di komputer Anda.
- Pastikan Anda sudah menginstal beberapa pustaka Python yang diperlukan:
  ```bash
  pip install streamlit pandas seaborn matplotlib
  ```

### Langkah Menjalankan Program
#### Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

#### Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

#### Run steamlit app
```
streamlit run dashboard.py
```

### Struktur Direktori
```
├───dashboard
| ├───main_data.csv
| └───dashboard.py
├───data
| ├───data_1.csv
| └───data_2.csv
├───bike_sharing.ipynb
├───README.md
└───requirements.txt
└───url.txt
```

## Visualisasi dan Analisis
Setiap analisis dilengkapi dengan visualisasi, seperti grafik batang dan garis, untuk mempermudah pemahaman pola penyewaan sepeda berdasarkan faktor-faktor seperti:
- **Kondisi cuaca**: Pengaruh cuaca terhadap jumlah penyewaan sepeda.
- **Waktu**: Waktu paling sibuk untuk penyewaan sepeda.
- **Hari libur vs hari biasa**: Perbedaan perilaku pengguna selama liburan.

