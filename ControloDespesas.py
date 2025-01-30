import pandas as pd
import streamlit as st
from datetime import datetime
from google.oauth2.service_account import Credentials
import gspread
from streamlit_echarts import st_echarts

# Google Sheets Setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1ZssUo6wfy4wZO9eQPljOTdwzF7dTSpxZ1_wNa6yGqaw"  # Replace with your Google Sheets ID

# Load credentials from Streamlit secrets
credentials = Credentials.from_service_account_info(st.secrets["GOOGLE_CREDENTIALS"], scopes=SCOPES)

# Authenticate with Google Sheets
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Read data from Google Sheets
data = sheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

st.title("Monitorização de Gastos 😁")
st.write(df.tail(5))

# Add a new entry
existing_categories = df['Category'].unique().tolist()
category = st.selectbox("Categoria", existing_categories)
new_category = st.text_input("Nova Categoria")
value = st.number_input("Value", value=None)
comments = st.text_area("Comentários")
if new_category != "":
    category = new_category

if st.button("Add Entry"):
    new_row = {
        "Insert_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Category": category,
        "Value": str(value),
        "Comments": comments
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Update Google Sheets
    sheet.clear()  # Clear the sheet
    sheet.update([df.columns.values.tolist()] + df.values.tolist())  # Write new data
    st.success("Entry added and Google Sheets updated!")

## Data visualization
st.header("Visualização de dados")

# Convert 'insert_date' to datetime and 'value' to float
df['Insert_date'] = pd.to_datetime(df['Insert_date'])
df['Value'] = df['Value'].astype(float)

# Creating a container to insert pretended month and respective piechart
with st.container():
    # Filter DataFrame for rows where 'insert_date' is in selected month
    month = st.selectbox("Month:",("Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"))
    month_mapping = {"Janeiro": 1,"Fevereiro": 2,"Março": 3,"Abril": 4,"Maio": 5,"Junho": 6,"Julho": 7,"Agosto": 8,"Setembro": 9,"Outubro": 10,"Novembro": 11,"Dezembro": 12}
    month_number = month_mapping[month]
    month_df = df[df['Insert_date'].dt.month == month_number]

    # Get sum of total spendings
    month_sum = sum(month_df["Value"])

    # Convert DataFrame to list of dictionaries for ECharts
    echarts_data = month_df[['Value', 'Category']].rename(columns={'Value': 'value', 'Category': 'name'}).to_dict(orient='records')

    # Group by 'Category' and sum the 'Value' column
    grouped_df = month_df.groupby('Category')['Value'].sum().round(2).reset_index()

    # Order the DataFrame by the sum of the 'Value' column in descending order
    grouped_df = grouped_df.sort_values(by='Value', ascending=False)

    # Convert DataFrame to list of dictionaries for ECharts
    echarts_data = grouped_df.rename(columns={'Value': 'value', 'Category': 'name'}).to_dict(orient='records')

    # Define the ECharts option
    option = {
        "title": {
            "text": f"Gastos por categoria",
            "subtext": f"Total de {month}: {month_sum}",
            "left": 'center'
        },
        "tooltip": {
            "trigger": 'item'
        },
        "legend": {
            "orient": 'vertical',
            "left": 'left'
        },
        "series": [
            {
                "name": 'Access From',
                "type": 'pie',
                "radius": '50%',
                "data": echarts_data,
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    }

    # Display the ECharts pie chart in Streamlit
    st_echarts(options=option, height="500px")
