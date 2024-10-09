import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Judul aplikasi
st.title('Proyek Analisis Data: Bike Sharing Datasheet')

st.markdown('''
*   Nama: Zeka Emo
*   Email: zeka.emo30@gmail.com
''')

# Membaca dataset
df_day = pd.read_csv('dashboard/day.csv')
df_hour = pd.read_csv('dashboard/hour.csv')

st.header('Di hari apa pengguna paling sering meminjam sepeda, dan pada hari apa permintaan paling sedikit terjadi?')

# Membuat kamus untuk mengubah label weekday
weekday_mapping = {
    0: 'Minggu',
    1: 'Senin',
    2: 'Selasa',
    3: 'Rabu',
    4: 'Kamis',
    5: 'Jumat',
    6: 'Sabtu'
}

# Mengelompokkan data berdasarkan 'weekday' untuk mendapatkan total penyewaan
weekday_rentals = df_day.groupby('weekday', observed=True)['cnt'].sum().reset_index()

# Mengonversi nilai weekday ke nama hari
weekday_rentals['weekday'] = weekday_rentals['weekday'].map(weekday_mapping)

# Menemukan hari dengan penyewaan sepeda tertinggi
most_rentals_day = weekday_rentals.loc[weekday_rentals['cnt'].idxmax()]

# Menemukan hari dengan penyewaan sepeda terendah
least_rentals_day = weekday_rentals.loc[weekday_rentals['cnt'].idxmin()]

# Menampilkan hasil
st.write(f"Hari dengan penyewaan sepeda tertinggi: {most_rentals_day['weekday']} ({most_rentals_day['cnt']} penyewaan)")
st.write(f"Hari dengan penyewaan sepeda terendah: {least_rentals_day['weekday']} ({least_rentals_day['cnt']} penyewaan)")

# Visualisasi total penyewaan per hari
st.subheader('Total Penyewaan Sepeda Berdasarkan Hari')
fig, ax = plt.subplots()
sns.barplot(data=weekday_rentals, x='weekday', y='cnt', ax=ax)
ax.set_xlabel('Hari dalam Seminggu')
ax.set_ylabel('Total Penyewaan')
st.pyplot(fig)

# Visualisasi penyewaan sepeda berdasarkan jam
hourly_rentals = df_hour.groupby('hr')['cnt'].sum().reset_index()

# Line plot untuk total penyewaan berdasarkan jam
st.subheader('Total Penyewaan Sepeda Berdasarkan Jam')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_rentals, marker="o", ax=ax)
plt.title('Total Penyewaan Sepeda Berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Total Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)

# Histogram untuk distribusi penyewaan berdasarkan jam
st.subheader('Distribusi Penyewaan Sepeda Berdasarkan Jam')
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(hourly_rentals['cnt'], bins=10, kde=True, ax=ax)
plt.title('Histogram Distribusi Penyewaan Sepeda')
plt.xlabel('Total Penyewaan Sepeda')
plt.ylabel('Frekuensi')
st.pyplot(fig)

# Box plot untuk penyewaan berdasarkan jam
st.subheader('Box Plot Penyewaan Sepeda Berdasarkan Jam')
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='hr', y='cnt', data=df_hour, ax=ax)
plt.title('Box Plot Penyewaan Sepeda Berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Total Penyewaan Sepeda')
st.pyplot(fig)

# Visualisasi rata-rata penyewaan sepeda berdasarkan kondisi cuaca
# Menghitung korelasi antara suhu dan total penyewaan sepeda
correlation_temp = df_day[['temp', 'cnt']].corr().iloc[0, 1]
print(f"Korelasi antara suhu dan penyewaan sepeda: {correlation_temp}")

st.header('Apakah ada hubungan antara penyewa sepeda dengan suhu dan cuaca?')

weather_mapping = {
    1: 'Cerah',
    2: 'Berkabut',
    3: 'Hujan Salju Ringan',
    4: 'Hujan Salju Lebat'
}

# Mengelompokkan berdasarkan 'weather_situation' untuk melihat rata-rata penyewaan sepeda per kondisi cuaca
weather_rentals = df_day.groupby('weathersit')['cnt'].mean().reset_index()
weather_rentals.columns = ['weathersit', 'cnt']  # Ganti nama kolom untuk kejelasan

# Mapping kondisi cuaca
weather_rentals['weathersit'] = weather_rentals['weathersit'].map(weather_mapping)

# Visualisasi rata-rata penyewaan sepeda berdasarkan kondisi cuaca
st.subheader('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_rentals, ax=ax)
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)

st.header('Musim mana yang cenderung paling populer untuk penyewaan sepeda berdasarkan volume penggunaan?')
# Mapping untuk musim
season_mapping = {
    1: 'Semi',
    2: 'Panas',
    3: 'Gugur',
    4: 'Salju'
}

# Mengelompokkan data berdasarkan 'season' untuk mendapatkan total penyewaan per musim
season_rentals = df_day.groupby('season', observed=True)['cnt'].sum().reset_index()
season_rentals['season'] = season_rentals['season'].map(season_mapping)

# Menemukan musim dengan penyewaan sepeda tertinggi
popular_season = season_rentals.loc[season_rentals['cnt'].idxmax()]

# Menampilkan hasil
st.write(f"Musim dengan penyewaan sepeda tertinggi: {popular_season['season']} ({popular_season['cnt']} penyewaan)")

# Visualisasi penyewaan sepeda berdasarkan musim
st.subheader('Total Penyewaan Sepeda Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=season_rentals, ax=ax)
plt.title('Total Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Total Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)

st.header('Lebih banyak mana user yang berlangganan atau tidak berlangganan?')

# Mengelompokkan data berdasarkan status berlangganan dan menjumlahkan total penyewaan
subscription_rentals = df_day[['registered', 'casual']].sum().reset_index()

# Menyusun ulang data untuk memudahkan perbandingan
subscription_rentals.columns = ['user_type', 'total_rentals']

# Menampilkan hasil
st.subheader("Jumlah Total Penyewaan Sepeda untuk Pengguna Terdaftar dan Kasual:")
st.write(subscription_rentals)

# Membandingkan jumlah penyewaan
if subscription_rentals.loc[subscription_rentals['user_type'] == 'registered', 'total_rentals'].values[0] > \
   subscription_rentals.loc[subscription_rentals['user_type'] == 'casual', 'total_rentals'].values[0]:
    st.write("Pengguna yang berlangganan lebih banyak dibandingkan dengan pengguna kasual.")
else:
    st.write("Pengguna kasual lebih banyak dibandingkan dengan pengguna yang berlangganan.")

# Visualisasi perbandingan pengguna terdaftar dan kasual
st.subheader('Perbandingan Total Penyewaan: Pengguna Terdaftar vs Pengguna Kasual')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='user_type', y='total_rentals', data=subscription_rentals, ax=ax)
plt.title('Perbandingan Total Penyewaan: Pengguna Terdaftar vs Pengguna Kasual')
plt.xlabel('Tipe Pengguna')
plt.ylabel('Total Penyewaan')
plt.xticks(rotation=45)
st.pyplot(fig)
