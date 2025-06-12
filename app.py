import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_yellowpages_leads(city):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    query_city = city.replace(" ", "+")
    url = f"https://www.yellowpages.com/search?search_terms=real+estate+agents&geo_location_terms={query_city}%2C+AZ"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    businesses = soup.find_all("div", class_="info")

    results = []

    for biz in businesses:
        try:
            name = biz.find("a", class_="business-name").text.strip()
        except:
            name = "Not listed"
        try:
            phone = biz.find("div", class_="phones phone primary").text.strip()
        except:
            phone = "Not listed"
        try:
            website = biz.find("a", class_="track-visit-website")["href"]
        except:
            website = "Not listed"

        results.append({"Name": name, "Phone": phone, "Website": website})

    return results

# Streamlit UI
st.title("🔍 Arizona Real Estate Lead Finder")
city_input = st.text_input("Enter a city in Arizona", "Phoenix")

if st.button("Find Leads"):
    with st.spinner("Scraping YellowPages..."):
        leads = get_yellowpages_leads(city_input)
    if leads:
        df = pd.DataFrame(leads)
        st.success(f"✅ Found {len(df)} leads in {city_input}")
        st.dataframe(df)
        st.download_button("📥 Download as CSV", df.to_csv(index=False), file_name="real_estate_leads.csv")
    else:
        st.error("❌ No leads found. Try another city or check your spelling.")
