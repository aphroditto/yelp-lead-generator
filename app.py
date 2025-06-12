import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_leads(city):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://www.yelp.com/search?find_desc=real+estate+agents&find_loc={city}+AZ"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for biz in soup.select("li.border-color--default__09f24__NPAKY")[:10]:
        name_tag = biz.select_one("a.css-19v1rkv")
        phone_tag = biz.select_one("p.css-8jxw1i")
        link = "https://www.yelp.com" + name_tag["href"] if name_tag else None

        if name_tag:
            name = name_tag.get_text()
            phone = phone_tag.get_text() if phone_tag else "Not listed"
            results.append({
                "Business Name": name,
                "Phone": phone,
                "Yelp Link": link
            })

    return results

# Streamlit interface
st.title("Arizona Real Estate Agent Lead Generator")
city = st.text_input("Enter a city in Arizona (e.g., Phoenix)")

if st.button("Find Leads"):
    if city:
        with st.spinner("Searching Yelp..."):
            leads = get_leads(city)
            if leads:
                df = pd.DataFrame(leads)
                st.success(f"✅ Found {len(leads)} leads.")
                st.dataframe(df)
                st.download_button("Download CSV", df.to_csv(index=False), "leads.csv", "text/csv")
            else:
                st.warning("❌ No leads found. Try another city or check spelling.")
    else:
        st.warning("⚠️ Please enter a city name.")
