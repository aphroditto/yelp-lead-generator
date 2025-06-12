import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

def get_leads(city):
    # Set up the Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.yelp.com/search?find_desc=real+estate+agents&find_loc={city}+AZ"
    driver.get(url)
    time.sleep(5)

    listings = driver.find_elements(By.XPATH, "//li[contains(@class, 'border-color--default')]")
    results = []

    for biz in listings[:10]:  # limit for demo
        try:
            name = biz.find_element(By.XPATH, ".//a[contains(@href, '/biz/')]").text
            link = biz.find_element(By.XPATH, ".//a[contains(@href, '/biz/')]").get_attribute("href")
        except:
            continue

        try:
            phone = biz.find_element(By.XPATH, ".//p[contains(text(),'(')]").text
        except:
            phone = "Not listed"

        results.append({"Business Name": name, "Yelp Link": link, "Phone": phone})

    driver.quit()
    return results

# Streamlit UI
st.title("Arizona Real Estate Agent Lead Generator")
city = st.text_input("Enter a city in Arizona:")

if st.button("Find Leads"):
    if city:
        with st.spinner("Searching..."):
            leads = get_leads(city)
            if leads:
                df = pd.DataFrame(leads)
                st.success(f"✅ Found {len(leads)} leads.")
                st.dataframe(df)
                st.download_button("Download as CSV", df.to_csv(index=False), "leads.csv", "text/csv")
            else:
                st.error("❌ No leads found. Try another city.")
    else:
        st.warning("Please enter a city.")
