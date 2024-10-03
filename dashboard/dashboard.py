import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Judul Aplikasi
st.title("Proyek Analisis Data - Bike Sharing")

# Memuat Dataset
st.header("Data Wrangling")
st.write("Memuat dataset dan menampilkan beberapa data.")

# Membaca file dataset
day_df = pd.read_csv('dashboard/day.csv')
hour_df = pd.read_csv('dashboard/hour.csv')

# Menampilkan data pertama
st.subheader("Data 'Day'")
st.dataframe(day_df.head())

st.subheader("Data 'Hour'")
st.dataframe(hour_df.head())

# Data Assessing
st.header("Data Assessing")
st.write("Informasi dataset 'day'")
st.text(day_df.info())

st.write("Informasi dataset 'hour'")
st.text(hour_df.info())

# Memeriksa apakah ada data yang kosong
st.write("Memeriksa missing data pada dataset 'day'")
st.text(day_df.isnull().sum())

st.write("Memeriksa missing data pada dataset 'hour'")
st.text(hour_df.isnull().sum())

# Memeriksa apakah ada data yang terduplikasi
st.write("Jumlah duplikasi pada dataset 'day':", day_df.duplicated().sum())
st.write("Jumlah duplikasi pada dataset 'hour':", hour_df.duplicated().sum())

# Data Wrangling
st.header("Data Wrangling")
st.write("Membersihkan dan mempersiapkan data untuk analisis.")

# Mengubah tipe data dan mengganti value sesuai dengan deskripsi
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

columns = ['season', 'mnth', 'weekday', 'weathersit']
for column in columns:
    day_df[column] = day_df[column].astype('category')
    hour_df[column] = hour_df[column].astype('category')

# Mengubah value pada beberapa kolom
season_value = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Snow'}
day_df['season'] = day_df['season'].map(season_value)
hour_df['season'] = hour_df['season'].map(season_value)

mnth_value = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}
day_df['mnth'] = day_df['mnth'].map(mnth_value)
hour_df['mnth'] = hour_df['mnth'].map(mnth_value)

weathers_value = {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain Snow', 4: 'Heavy Rain Snow'}
day_df['weathersit'] = day_df['weathersit'].map(weathers_value)
hour_df['weathersit'] = hour_df['weathersit'].map(weathers_value)

# Mengubah nilai lainnya
year_values = {0: '2011', 1: '2012'}
day_df['yr'] = day_df['yr'].map(year_values)
hour_df['yr'] = hour_df['yr'].map(year_values)

# Mengubah nilai 'holiday'
holiday_values = {0: 'Off Season', 1: 'Holiday'}
day_df['holiday'] = day_df['holiday'].map(holiday_values)
hour_df['holiday'] = hour_df['holiday'].map(holiday_values)

# Menghapus 'atemp'
day_df = day_df.drop(columns = "atemp")
hour_df = hour_df.drop(columns = "atemp")

# Menampilkan hasil transformasi
st.subheader("Data setelah proses wrangling")
st.dataframe(day_df.head())
st.dataframe(hour_df.head())

# Exploratory Data Analysis
st.header("Exploratory Data Analysis")
st.write("Menganalisis data untuk mendapatkan wawasan dari dataset.")

# Bagaimana cuaca mempengaruhi jumlah peminjaman sepeda
weather_rents = hour_df.groupby('weather_situation')['count_total'].sum().reset_index()
weather_rents_sorted = weather_rents.sort_values(by='count_total', ascending=False)

st.subheader("Pengaruh Cuaca terhadap Peminjaman Sepeda")
st.dataframe(weather_rents_sorted)

# Visualisasi rata-rata penyewaan sepeda berdasarkan kondisi cuaca
st.subheader("Visualisasi Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
plt.figure(figsize=(10, 6))
sns.barplot(x='weather_situation', y='count_total', data=hour_df)
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Rata-rata Penyewaan Sepeda')
st.pyplot(plt)

# Rata-rata penggunaan sepeda pada liburan dan hari biasa
holiday_data = hour_df[hour_df['holiday'] == "Holiday"]
no_holiday_data = hour_df[hour_df['holiday'] == "Off Season"]

total_registered = holiday_data['registered'].mean().round().astype(int)
total_casual = holiday_data['casual'].mean().round().astype(int)
total_registered_no = no_holiday_data['registered'].mean().round().astype(int)
total_casual_no = no_holiday_data['casual'].mean().round().astype(int)

st.subheader("Pengguna Terdaftar dan Tidak Terdaftar pada Liburan vs Hari Biasa")
st.write(f"Rata-rata pengguna terdaftar pada liburan: {total_registered}")
st.write(f"Rata-rata pengguna terdaftar pada hari biasa: {total_registered_no}")
st.write(f"Rata-rata pengguna tidak terdaftar pada liburan: {total_casual}")
st.write(f"Rata-rata pengguna tidak terdaftar pada hari biasa: {total_casual_no}")

# Visualisasi pengguna registered dan casual pada liburan vs hari biasa
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

# Analisis penyewaan sepeda berdasarkan jam
st.subheader("Pada Sehari, Pada Pukul Berapa Sepeda Paling Banyak Dipinjam?")
time_rents = hour_df.groupby('hour', observed=True)['count_total'].mean().round().astype(int).reset_index()
time_rents_sorted = time_rents.sort_values(by='count_total', ascending=False)

st.dataframe(time_rents_sorted)

highest_rentals = time_rents.loc[time_rents['count_total'].idxmax()]
st.write(f"Sepeda lebih banyak dipinjam pada jam {highest_rentals['hour']}.00 dengan jumlah {highest_rentals['count_total']} unit.")

# Visualisasi penyewaan sepeda berdasarkan jam
plt.figure(figsize=(10, 6))
sns.lineplot(x='hour', y='count_total', data=time_rents, marker="o")
plt.title('Total Penyewaan Sepeda Berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(plt)

# Analisis penyewaan sepeda berdasarkan hari
st.subheader("Dalam Seminggu, Hari Apa Sepeda Paling Banyak Dipinjam?")
day_rents = hour_df.groupby('day', observed=True)['count_total'].mean().round().astype(int).reset_index()
day_rents_sorted = day_rents.sort_values(by='count_total', ascending=False)

st.dataframe(day_rents_sorted)

highest_day_rentals = day_rents.loc[day_rents['count_total'].idxmax()]
st.write(f"Pada hari {highest_day_rentals['day']} sepeda paling banyak dipinjam dengan rata-rata {highest_day_rentals['count_total']} unit.")

# Visualisasi penyewaan sepeda berdasarkan hari
plt.figure(figsize=(10, 6))
sns.barplot(x='day', y='count_total', data=day_rents)
plt.title('Total Penyewaan Sepeda Berdasarkan Hari')
plt.xlabel('Hari')
plt.ylabel('Jumlah Penyewaan Sepeda')
st.pyplot(plt)

# Korelasi antara temperatur dan jumlah penyewaan
st.subheader("Bagaimana Jumlah Sepeda yang Dipinjam Ketika Udara Sangat Panas atau Dingin?")
correlation = hour_df['temperature'].corr(hour_df['count_total'])
st.write(f"Korelasi antara temperatur dan total penyewaan: {correlation}")

# Binning untuk temperatur
bins = [0, 10, 20, 30, 40]
labels = ['0-10°C', '11-20°C', '21-30°C', '31-40°C']
hour_df['temp_category'] = pd.cut(hour_df['temperature'], bins=bins, labels=labels, include_lowest=True)

temp_rentals = hour_df.groupby('temp_category')['count_total'].mean().reset_index()
st.dataframe(temp_rentals)

# Visualisasi penyewaan sepeda berdasarkan kategori temperatur
plt.figure(figsize=(10, 6))
plt.bar(temp_rentals['temp_category'], temp_rentals['count_total'])
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kategori Temperatur')
plt.xlabel('Kategori Temperatur')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(plt)

# Kesimpulan
st.header("Kesimpulan")
st.write("""
1. Sepeda paling banyak dipinjam saat cuaca sedang cloudy.
2. Pada hari libur, pengguna baru mengalami peningkatan.
3. Rata-rata penyewaan sepeda paling banyak terdapat pada pukul 17.00.
4. Hari Kamis menjadi hari dengan penyewaan paling banyak dalam seminggu.
5. Pengguna cenderung lebih banyak menyewa sepeda pada rentang suhu 31 sampai 40 derajat celcius.
""")
