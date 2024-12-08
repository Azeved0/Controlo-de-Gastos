import pandas as pd
import requests
import base64
import streamlit as st
from datetime import datetime

# Set the layout to wide
st.set_page_config(layout="wide")

# GitHub details
repo = "Azeved0/Controlo-de-Gastos"  # Your repo name
file_path = "Despesas.csv"  # Path to the file in the repository
branch = "main"  # Branch name
token = "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"
#token = "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"

# URL of the raw CSV file
#url = f"https://raw.githubusercontent.com/{repo}/refs/heads/{branch}/{file_path}"
url = f"https://raw.githubusercontent.com/{repo}/{branch}/{file_path}"


# Load the CSV file into a DataFrame
response = requests.get(url)
if response.status_code == 200:
    df = pd.read_csv(url)
    st.write(df)
else:
    st.write("Failed to fetch the CSV file from GitHub.")

# Add a title
st.title("Monitorização de Gastos 😁")

# Create a dropdown box with the specified options
category = st.selectbox("Categoria", ["renda", "restauração", "combustível", "outros"])
value = st.number_input("Value",value=None)
comments = st.text_area("Comentários")

# --- Adding a new row ---
new_row = pd.DataFrame([{
    "Insert_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Example date
    "Category": category,  # Replace with the desired category
    "Value": value,  # Replace with the desired value
    "Comments": comments  # Replace with your comment
}])

# Concatenate the new row with the existing DataFrame
df = pd.concat([df, new_row], ignore_index=True)

st.write(df)

updated_csv = df.to_csv(index=False)  # Convert the updated DataFrame to CSV content

st.write("xau")

# Create a submit button
if st.button("Submeter"):
    # GitHub API URL to update the file
    api_url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    
    # Get the current file's SHA
    headers = {"Authorization": f"token {token}"}
    response = requests.get(api_url, headers=headers)
    st.write(response.status_code)
    st.write(response.json())
    if response.status_code == 200:
        sha = response.json()["sha"]
    else:
        st.error("Erro ao tentar submeter: Falha ao aceder dados do arquivo.")
        st.stop()
    
    # Encode the updated CSV content in base64
    encoded_content = base64.b64encode(updated_csv.encode("utf-8")).decode("utf-8")
    
    # Prepare the API request payload
    data = {
        "message": "Updated Despesas.csv via local script",
        "content": encoded_content,
        "sha": sha,  # Current file SHA
        "branch": branch,
    }
    
    # Update the file in the repository
    response = requests.put(api_url, json=data, headers=headers)
    st.write(response.json())  # Print detailed error response from GitHub for debugging
    
    # Check the response
    if response.status_code in [200, 201]:
        st.success("Submetido")
    else:
        st.error("Erro ao tentar submeter")
        st.write(response.json())  # Print detailed error response from GitHub for debugging
