import pandas as pd
import streamlit as st
from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread

# Google Sheets Setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1ZssUo6wfy4wZO9eQPljOTdwzF7dTSpxZ1_wNa6yGqaw"  # Replace with your Google Sheets ID

# Load credentials from secrets
credentials_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
credentials = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Read data from Google Sheets
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.title("Monitorização de Gastos 😁")
st.write("Current data:")
st.write(df)

# Add a new entry
category = st.selectbox("Categoria", ["renda", "restauração", "combustível", "outros"])
value = st.number_input("Value", value=None)
comments = st.text_area("Comentários")

if st.button("Add Entry"):
    new_row = {
        "Insert_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Category": category,
        "Value": value,
        "Comments": comments
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Update Google Sheets
    sheet.clear()  # Clear the sheet
    sheet.update([df.columns.values.tolist()] + df.values.tolist())  # Write new data
    st.success("Entry added and Google Sheets updated!")
