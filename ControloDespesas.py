import streamlit as st
import pandas as pd

# Set the layout to wide
st.set_page_config(layout="wide")

# Add a title
st.title("Monitorização de Gastos 😁")

# Create a dropdown box with the specified options
category = st.selectbox("Categoria", ["renda", "restauração", "combustível", "outros"])

# Create a textbox for comments
comments = st.text_area("Comentários")

# Create a submit button
if st.button("Submeter"):
    st.success("Submetido")