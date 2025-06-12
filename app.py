import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("🏡 Arizona Real Estate Lead Generator")
st.markdown("Enter an Arizona city to find real estate agents from Yelp.")

city = st.text_input("City Name", "Phoenix")

def search_agents(city):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = f"real estate agents in {city}, Arizona site:yelp.com"
    url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    leads = []
    results = soup.find_all("li", class_="b_algo")

    for result in results:
        a_tag = result.find("a")
        if a_tag and "href" in a_tag.attrs:
            link = a_tag["href"]
            title = a_tag.get_text(strip=True)
            if "yelp.com" in link:
                leads.append({"Name": title, "Link": link})

    return leads

if st.button("🔍 Find Leads"):
    if city:
        st.write(f"Searching for real estate agents in **{city}**, Arizona...")
        leads = search_agents(city)
        if leads:
            df = pd.DataFrame(leads)
            st.success(f"✅ Found {len(leads)} leads!")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Leads as CSV", data=csv, file_name=f"{city}_real_estate_leads.csv", mime='text/csv')
        else:
            st.warning("❌ No leads found. Try another city.")
    else:
        st.error("Please enter a city name.")
