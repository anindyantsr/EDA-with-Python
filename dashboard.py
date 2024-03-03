import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

from babel.numbers import format_currency
sns.set(style='dark')

def create_renters_hour_df(hour_df):
    renters_hour_df = hour_df.groupby(by="hr").agg({
        "cnt": "sum"
    })
    return renters_hour_df

def create_renters_day_df(day_df):
    renters_day_df = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return renters_day_df

def create_sum_registered_df(day_df):
    sum_registered_df = day_df.groupby(by="dteday").agg({
        "registered": "sum"
    })
    sum_registered_df = sum_registered_df.reset_index()
    sum_registered_df.rename(columns={
        "registered": "sum_registered",
    }, inplace=True)
    return sum_registered_df

def create_sum_casual_df(day_df):
    sum_casual_df = day_df.groupby(by="dteday").agg({
        "casual": "sum"
    })
    sum_casual_df = sum_casual_df.reset_index()
    sum_casual_df.rename(columns={
        "casual": "sum_casual",
    }, inplace=True)
    return sum_casual_df

def create_sum_renters_df(hour_df):
    renters_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return renters_df

def create_renters_season_df(day_df): 
    season_df = day_df.groupby(by="season").cnt.sum().reset_index() 
    return season_df

day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)
  

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

min_day = day_df["dteday"].min()
max_day = day_df["dteday"].max()
min_hour = hour_df["dteday"].min()
max_hour = hour_df["dteday"].max()


with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/anindyantsr/EDA-with-Python/main/bike-sharing-rental-service-logo-icon-with-bicycle_116137-6024.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Span', 
        min_value=min_day,
        max_value=max_day,
        value=[min_day, max_day]
    )

main_day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]
main_hour_df = hour_df[(day_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

hour_renters_df = create_renters_hour_df(main_hour_df)
renters_day_df = create_renters_day_df(main_day_df)
sum_registered_df = create_sum_registered_df(main_day_df)
sum_casual_df = create_sum_casual_df(main_day_df)
sum_renters_df = create_sum_renters_df(main_hour_df)
seasons_df = create_renters_season_df(main_hour_df)

st.header(':bike: Bike-sharing Dashboard')
 
col1, col2, col3 = st.columns(3)

with col1:
    total_renters = renters_day_df.cnt.sum()
    st.metric("Total Bike Sharing Renters", value=total_renters)

with col2:
    total_casual_renters = sum_casual_df.sum_casual.sum()
    st.metric("Total Casual Renters", value=total_casual_renters)

with col3:
    total_registered_renters = sum_registered_df.sum_registered.sum()
    st.metric("Total Registered Renters", value=total_registered_renters)

st.markdown("---")

st.subheader(":round_pushpin: Daily Count of Bike Share Renters")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_df["dteday"],
    day_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#7209B7"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader(":round_pushpin: Weekly Count of Bike Share Renters")
fig, ax = plt.subplots(figsize=(10,5))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#E67F0D"]
sns.barplot(
    x="weekday",
    y="cnt",
    data=day_df.sort_values(by="weekday", ascending=False),
    palette=colors,
    ax=ax
    )

plt.xlabel(None)
plt.ylabel(None)
plt.title("Number of Renters in A Week", loc="center", fontsize=20)
plt.tick_params(axis ='x', labelsize=15)
plt.tick_params(axis ='y', labelsize=15)

st.pyplot(fig)

st.subheader(":round_pushpin: Seasonly Count of Bike Share Renters")
fig, ax = plt.subplots(figsize=(10,5))
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#93C572"]
sns.barplot(
    x="season",
    y="cnt",
    data=day_df.sort_values(by="season", ascending=False),
    palette=colors,
    ax=ax
    )

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title("Number of Renters by Season", loc="center", fontsize=20)
ax.tick_params(axis ='x', labelsize=15)
ax.tick_params(axis ='y', labelsize=15)

st.pyplot(fig)

st.caption(':copyright: anindyantsr')
