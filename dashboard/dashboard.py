import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import numpy as np
warnings.filterwarnings('ignore')

# Judul aplikasi
st.title('Proyek Analisis Data: Bike Sharing Dataset')

st.markdown('''
*   Nama: Zeka Emo
*   Email: zeka.emo30@gmail.com
*   Dicoding ID: zekaemo
''')

# Membaca dataset
df_day = pd.read_csv('dashboard/day.csv')
df_hour = pd.read_csv('dashboard/hour.csv')

# Mengubah kolom 'dteday' menjadi datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Sidebar untuk Filtering berdasarkan musim dan cuaca
st.sidebar.header("Filter Data")
season_mapping = {1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Salju'}
df_day['season'] = df_day['season'].map(season_mapping)

season = st.sidebar.multiselect("Pilih Musim", options=df_day['season'].unique())

weather_mapping = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan Salju Ringan', 4: 'Hujan Salju Lebat'}
df_day['weathersit'] = df_day['weathersit'].map(weather_mapping)
weather = st.sidebar.multiselect("Pilih Kondisi Cuaca", options=df_day['weathersit'].unique())

# Normalisasi data temperatur
df_day['temp'] = (df_day['temp'] * 41).round().astype(int)
df_hour['temp'] = (df_hour['temp'] * 41).round().astype(int)

# Filtering data berdasarkan musim dan cuaca
filtered_data_day = df_day.copy()
if season:
    filtered_data_day = filtered_data_day[filtered_data_day['season'].isin(season)]

if weather:
    filtered_data_day = filtered_data_day[filtered_data_day['weathersit'].isin(weather)]

# Pertanyaan 1: Bagaimana cuaca mempengaruhi jumlah peminjaman sepeda?
st.header('Rata-rata Penyewaan Berdasarkan Kondisi Cuaca')
weather_rents = df_hour.groupby('weathersit')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_rents, ax=ax)
plt.title('Rata-rata Penyewaan Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)

# Pertanyaan 2: Pada hari liburan, apakah ada kebiasaan yang berbeda dari kategori peminjam jika dibandingkan dengan hari biasa?
st.header('Pengguna Registered dan Casual Selama Liburan vs Hari Biasa')

# Menghitung nilai total_registered, total_casual, total_registered_no, total_casual_no
holiday_data = df_hour[df_hour['holiday'] == 1]
no_holiday_data = df_hour[df_hour['holiday'] == 0]

total_registered = holiday_data['registered'].mean().round().astype(int)
total_casual = holiday_data['casual'].mean().round().astype(int)
total_registered_no = no_holiday_data['registered'].mean().round().astype(int)
total_casual_no = no_holiday_data['casual'].mean().round().astype(int)

# Menampilkan hasil jumlah pengguna registered dan casual selama liburan dan hari biasa
categories = ['Liburan', 'Hari Biasa']
registered_values = [total_registered, total_registered_no]
casual_values = [total_casual, total_casual_no]

x = np.arange(len(categories))
width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width/2, registered_values, width, label='Pengguna Terdaftar')
ax.bar(x + width/2, casual_values, width, label='Pengguna Baru')
ax.set_xlabel('Kondisi (Liburan vs Hari Biasa)')
ax.set_ylabel('Rata-rata Pengguna')
ax.set_title('Rata-rata Pengguna Registered dan Casual Selama Liburan vs Hari Biasa')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
st.pyplot(fig)

# Pertanyaan 3: Pada sehari, pada pukul berapa sepeda paling banyak dipinjam?
st.header('Penyewaan Berdasarkan Jam')
time_rents = df_hour.groupby('hr')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='hr', y='cnt', data=time_rents, marker="o", ax=ax)
plt.title('Total Penyewaan Sepeda Berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Total Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)

# Pertanyaan 4: Dalam seminggu, hari apa sepeda paling banyak dipinjam?
st.header('Penyewaan Berdasarkan Hari')
weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
df_day['weekday'] = df_day['weekday'].map(weekday_mapping)
day_rents = df_day.groupby('weekday')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weekday', y='cnt', data=day_rents, ax=ax)
plt.title('Total Penyewaan Sepeda Berdasarkan Hari')
plt.xlabel('Hari')
plt.ylabel('Total Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)

# Pertanyaan 5: Bagaimana jumlah sepeda yang dipinjam ketika udara sangat panas atau sangat dingin?
st.header('Penyewaan Berdasarkan Temperatur')
bins = [0, 10, 20, 30, 40]
labels = ['0-10°C', '11-20°C', '21-30°C', '31-40°C']
df_hour['temp_category'] = pd.cut(df_hour['temp'], bins=bins, labels=labels, include_lowest=True)
temp_rentals = df_hour.groupby('temp_category')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='temp_category', y='cnt', data=temp_rentals, ax=ax)
plt.title('Rata-rata Penyewaan Berdasarkan Kategori Temperatur')
plt.xlabel('Kategori Temperatur')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)
