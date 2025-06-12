import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_leads(city):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.yellowpages.com/search?search_terms=real+estate+agents&geo_location_terms={city}+AZ"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.select(".result")

    leads = []
    for biz in listings:
        name = biz.select_one(".business-name")
        phone = biz.select_one(".phones")
        website = biz.select_one("a.track-visit-website")

        leads.append({
            "Business Name": name.text.strip() if name else "N/A",
            "Phone": phone.text.strip() if phone else "N/A",
            "Website": website['href'] if website else "N/A"
        })

    return leads

st.title("📍 Arizona Real Estate Agent Lead Finder")

city = st.text_input("Enter a City in Arizona", "")

if st.button("Find Leads"):
    if city.strip():
        with st.spinner("🔎 Searching..."):
            leads = get_leads(city)
            if leads:
                df = pd.DataFrame(leads)
                st.success(f"✅ Found {len(leads)} leads.")
                st.dataframe(df)
                st.download_button("Download CSV", df.to_csv(index=False), "leads.csv", "text/csv")
            else:
                st.warning("❌ No leads found. Try another city.")
    else:
        st.warning("⚠️ Please enter a city name.")
