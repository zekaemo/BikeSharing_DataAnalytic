import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Judul dan Pengantar
st.title('Proyek Analisis Data: Bike Sharing')
st.subheader('Dibuat oleh Zeka Emo')

st.markdown("""
### Analisis data pada Bike Sharing Dataset dilakukan guna melihat interaksi antar variabel yang terdapat di dalamnya. Dan juga menarik kesimpulan dari pertanyaan- pertanyaan yang ada  
""")

# Data Loading
st.markdown('## Data Loading & Wrangling')
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

st.write('Tabel day_df:')
st.dataframe(day_df.head())

st.write('Tabel hour_df:')
st.dataframe(hour_df.head())

# Data Wrangling
st.markdown('## Data Wrangling')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Mengubah tipe data menjadi kategori
columns = ['season', 'mnth', 'weekday', 'weathersit']
for column in columns:
    day_df[column] = day_df[column].astype("category")
    hour_df[column] = hour_df[column].astype("category")

# Mengubah nilai season, month, dll
season_value = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Snow'}
day_df['season'] = day_df['season'].map(season_value)

mnth_value = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}
day_df['mnth'] = day_df['mnth'].map(mnth_value)

# Data Assessing
st.markdown('## Data Assessing')
st.write('Informasi dataset day_df:')
st.write(day_df.info())

# Exploratory Data Analysis
st.markdown('## Exploratory Data Analysis')

# Analisis 1: Cuaca dan Peminjaman Sepeda
st.markdown('### Bagaimana cuaca mempengaruhi jumlah peminjaman sepeda?')
weather_rents = hour_df.groupby('weathersit')['cnt'].sum().reset_index().sort_values(by='cnt', ascending=False)
st.write(weather_rents)

# Visualisasi
st.markdown('Visualisasi Rata-rata Penyewaan Berdasarkan Kondisi Cuaca:')
plt.figure(figsize=(10,6))
sns.barplot(x='weathersit', y='cnt', data=weather_rents, palette="coolwarm")
plt.title('Penyewaan Berdasarkan Kondisi Cuaca')
st.pyplot()

# Analisis 2: Pengguna Liburan vs Hari Biasa
st.markdown('### Apakah ada perbedaan kategori peminjam saat liburan?')
holiday_data = hour_df[hour_df['holiday'] == 1]
no_holiday_data = hour_df[hour_df['holiday'] == 0]

registered_holiday = holiday_data['registered'].mean()
casual_holiday = holiday_data['casual'].mean()
registered_no_holiday = no_holiday_data['registered'].mean()
casual_no_holiday = no_holiday_data['casual'].mean()

st.write(f'Rata-rata pengguna terdaftar saat liburan: {registered_holiday:.2f}')
st.write(f'Rata-rata pengguna casual saat liburan: {casual_holiday:.2f}')

# Visualisasi
st.markdown('Visualisasi Perbandingan Pengguna Terdaftar vs Casual saat Liburan:')
categories = ['Liburan', 'Hari Biasa']
registered_values = [registered_holiday, registered_no_holiday]
casual_values = [casual_holiday, casual_no_holiday]
x = np.arange(len(categories))
width = 0.35
fig, ax = plt.subplots(figsize=(10,6))
ax.bar(x - width/2, registered_values, width, label='Terdaftar')
ax.bar(x + width/2, casual_values, width, label='Casual')
ax.set_xlabel('Kondisi')
ax.set_ylabel('Jumlah Pengguna')
ax.set_title('Pengguna Terdaftar dan Casual saat Liburan vs Hari Biasa')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
st.pyplot(fig)

# Kesimpulan
st.markdown('## Kesimpulan')
st.markdown("""
1. **Cuaca Cloudy** paling banyak menarik peminjam sepeda.
2. **Pengguna baru** lebih banyak pada hari liburan dibandingkan dengan hari biasa.
3. **Peminjaman sepeda paling banyak** terjadi pada jam 17.00 dan pada hari Kamis.
4. **Temperatur** mempengaruhi jumlah peminjaman sepeda, di mana penyewaan tertinggi terjadi pada suhu 31-40°C.
5. Pada proses **binning**, pengguna cenderung lebih banyak menyewa sepeda pada rentang suhu 31 sampai 40 derajat celcius.
""")
