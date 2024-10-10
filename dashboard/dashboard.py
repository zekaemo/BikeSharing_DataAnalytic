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

# Filtering data berdasarkan musim dan cuaca
filtered_data_day = df_day.copy()
if season:
    filtered_data_day = filtered_data_day[filtered_data_day['season'].isin(season)]

if weather:
    filtered_data_day = filtered_data_day[filtered_data_day['weathersit'].isin(weather)]

# Analisis Berdasarkan Hari
st.header('Analisis Berdasarkan Hari')
weekday_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
filtered_data_day['weekday'] = filtered_data_day['weekday'].map(weekday_mapping)
weekday_rentals = filtered_data_day.groupby('weekday', observed=True)['cnt'].sum().reset_index()

# Visualisasi total penyewaan per hari
st.subheader('Total Penyewaan Sepeda Berdasarkan Hari')
fig, ax = plt.subplots()
sns.barplot(data=weekday_rentals, x='weekday', y='cnt', ax=ax)
ax.set_xlabel('Hari dalam Seminggu')
ax.set_ylabel('Total Penyewaan')
st.pyplot(fig)

# Filtering berdasarkan jam
st.header('Analisis Berdasarkan Jam')
hourly_rentals = df_hour.groupby('hr')['cnt'].sum().reset_index()

# Visualisasi penyewaan sepeda berdasarkan jam
st.subheader('Total Penyewaan Sepeda Berdasarkan Jam')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_rentals, marker="o", ax=ax)
plt.title('Total Penyewaan Sepeda Berdasarkan Jam')
plt.xlabel('Jam')
plt.ylabel('Total Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualisasi berdasarkan musim
st.header('Analisis Berdasarkan Musim')
season_rentals = filtered_data_day.groupby('season', observed=True)['cnt'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=season_rentals, ax=ax)
plt.title('Total Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Total Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)

st.header('Analisis Berdasarkan Kondisi Cuaca')
weather_rentals = filtered_data_day.groupby('weathersit')['cnt'].mean().reset_index()

# Visualisasi rata-rata penyewaan sepeda berdasarkan kondisi cuaca
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_rentals, ax=ax)
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)
