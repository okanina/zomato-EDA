import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Zomato EDA", page_icon=":bar_chart", layout="wide")
st.title(":bar_chart: Zomato EDA")

df1=pd.read_csv("data\zomato.csv", encoding="latin -1")
df2=pd.read_excel("data\Country-Code.xlsx")

df=pd.merge(df1, df2, on="Country Code", how="left")

# Country
country_name=df.Country.value_counts().index
country_val=df.Country.value_counts().values

col1, col2 =st.columns(2)
# plot pie
with col1:
    st.subheader("Sales by Country")
    fig=px.pie(df, names=country_name, values=country_val, hole=0.5)
    fig.update_traces(text=country_name, textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.write(f"There are 15 represented countries in this dataset. Most of Zomato records/transaction comes from India, followed by United States, then United Kingdoms. The country with the least records is Canada.")

ratings=df.groupby(['Aggregate rating', 'Rating color', 'Rating text']).size().reset_index().rename(columns={0:"Rating Count"})


with col2:
    st.subheader("Service Ratings")
    fig=px.bar(ratings, x="Rating color", y="Rating Count", template="seaborn")
    st.plotly_chart(fig, use_container_width=True)
    st.write("More than 3000 customers in this dataset rated the service 'average'.More than 2000 customers did not rate the service at all, more than 2000 rated the service 'good' while more than 1000 rated the service 'very good' and a less number of customers rated the service 'Excellent' and 'Poor'")

low_rating_countries=df[df["Rating color"]=="White"].groupby("Country").size()
zero_ratings_country_name=df[df["Rating color"]=="White"].groupby("Country").size().index
zero_rating_country_values=df[df["Rating color"]=="White"].groupby("Country").size().values

with col1:
    st.subheader("Zero Ratings Countries")
    fig=px.bar(low_rating_countries, x=zero_ratings_country_name, y=zero_rating_country_values, template="seaborn")
    st.plotly_chart(fig, use_container_width=True)
    st.write("There are only 4 countries that have rated the service 0. The country with the highest zero rating is India.")

with col2:
    online_deliveries=df[['Has Online delivery', "Country"]]
    online_del=online_deliveries[online_deliveries['Has Online delivery']=="Yes"].groupby("Country").size()
    st.subheader("Online Deliveries by Countries")
    fig=px.bar(online_del, x=online_del.index, y=online_del.values, template="seaborn") 
    st.plotly_chart(fig, use_container_width=True)
    st.write("Online deliveries is only available in 2 countries, India and UAE")