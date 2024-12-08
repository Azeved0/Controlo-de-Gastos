import pandas as pd
import streamlit as st
from datetime import datetime

st.title("Monitorização de Gastos 😁")

# File Uploader
uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])

if uploaded_file:
    # Read the uploaded CSV
    df = pd.read_csv(uploaded_file)
    st.write(df)
else:
    # Initialize an empty DataFrame if no file is uploaded
    df = pd.DataFrame(columns=["Insert_date", "Category", "Value", "Comments"])

# Add new entry
category = st.selectbox("Categoria", ["renda", "restauração", "combustível", "outros"])
value = st.number_input("Value", value=None)
comments = st.text_area("Comentários")

new_row = pd.DataFrame([{
    "Insert_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "Category": category,
    "Value": value,
    "Comments": comments
}])

# Concatenate the new row with the existing DataFrame
df = pd.concat([df, new_row], ignore_index=True)

st.write(df)

# File Downloader
st.download_button(
    label="Download Updated CSV",
    data=df.to_csv(index=False),
    file_name="Despesas.csv",
    mime="text/csv"
)
