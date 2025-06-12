import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def search_agents(city):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = f"real estate agents in {city}, Arizona site:yelp.com"
    url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    leads = []
    for item in soup.select("li.b_algo h2 a"):
        name = item.get_text(strip=True)
        link = item["href"]
        leads.append({"Name": name, "Link": link})

    return leads

st.title("Arizona Real Estate Agent Finder (via Bing)")

city = st.text_input("Enter a city in Arizona")

if st.button("Search"):
    if not city.strip():
        st.warning("Please enter a city.")
    else:
        st.info("Searching Bing for agent listings...")
        results = search_agents(city)
        if results:
            df = pd.DataFrame(results)
            st.success(f"Found {len(results)} leads.")
            st.dataframe(df)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", data=csv, file_name="agent_leads.csv", mime="text/csv")
        else:
            st.error("No leads found. Try another city.")
