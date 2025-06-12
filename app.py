import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_yellow_pages(city):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.yellowpages.com/search?search_terms=real+estate+agents&geo_location_terms={city.replace(' ', '+')}+AZ"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    listings = soup.find_all("div", class_="result")
    leads = []

    for listing in listings:
        name = listing.find("a", class_="business-name")
        phone = listing.find("div", class_="phones phone primary")
        website_tag = listing.find("a", class_="track-visit-website")

        if name:
            lead = {
                "Business Name": name.text.strip(),
                "Phone Number": phone.text.strip() if phone else "Not listed",
                "Website": website_tag["href"] if website_tag else "Not listed"
            }
            leads.append(lead)

    return leads

st.title("Arizona Real Estate Agent Lead Finder")

city = st.text_input("Enter a city in Arizona:")

if st.button("Find Leads"):
    if city:
        with st.spinner("Searching YellowPages..."):
            leads = scrape_yellow_pages(city)
            if leads:
                df = pd.DataFrame(leads)
                st.success(f"✅ Found {len(leads)} leads!")
                st.dataframe(df)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download CSV", data=csv, file_name="real_estate_leads.csv", mime="text/csv")
            else:
                st.error("❌ No leads found. Try another city.")
    else:
        st.warning("⚠️ Please enter a city name.")
