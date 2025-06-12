import streamlit as st
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

def get_leads(city):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.bing.com/search?q=real+estate+agents+in+{city}+AZ"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    leads = []
    for a in soup.select("li.b_algo h2 a"):
        title = a.get_text(strip=True)
        link = a['href']
        if "yelp" in link or "realtor" in link or "zillow" in link:
            leads.append((title, link))
    return leads

def to_excel(data):
    wb = Workbook()
    ws = wb.active
    ws.append(["Name or Company", "Link"])
    for row in data:
        ws.append(row)
    file = "/tmp/leads.xlsx"
    wb.save(file)
    return file

# Streamlit UI
st.title("🏡 Real Estate Lead Generator (AZ)")
city = st.text_input("Enter an Arizona city (e.g., Phoenix):")

if st.button("Find Leads") and city:
    with st.spinner("Searching..."):
        leads = get_leads(city)
        if leads:
            st.success(f"Found {len(leads)} leads!")
            st.dataframe(leads, use_container_width=True)
            excel = to_excel(leads)
            with open(excel, "rb") as f:
                st.download_button("📥 Download Excel", f, "leads.xlsx")
        else:
            st.warning("No leads found. Try another city.")
