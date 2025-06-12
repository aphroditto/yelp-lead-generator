import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def get_leads(city):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = f"real estate agents in {city} Arizona site:yellowpages.com"
    url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")
    leads = []
    for link in links:
        href = link.get("href")
        if href and "yellowpages.com" in href and "/mip/" in href:
            leads.append({
                "Business Name": link.get_text(strip=True),
                "Website Link": href
            })

    return leads

st.title("🏠 Arizona Real Estate Lead Finder")

city = st.text_input("Enter an Arizona city:", "Phoenix")

if st.button("Search Leads"):
    with st.spinner("Searching for leads..."):
        results = get_leads(city)
        if results:
            df = pd.DataFrame(results)
            st.success(f"✅ Found {len(results)} leads")
            st.dataframe(df)
            st.download_button("📥 Download as CSV", df.to_csv(index=False), "leads.csv")
        else:
            st.error("❌ No leads found. Try another city.")
