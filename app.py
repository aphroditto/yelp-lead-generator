import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def get_yelp_leads(city):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://www.yelp.com/search?find_desc=real+estate+agents&find_loc={city.replace(' ', '+')}+AZ"
    driver.get(url)
    time.sleep(5)

    results = []
    listings = driver.find_elements(By.CSS_SELECTOR, "li.border-color--default__09f24__NPAKY")

    for biz in listings[:10]:  # Adjust how many you want
        try:
            name = biz.find_element(By.XPATH, ".//a[contains(@href, '/biz/')]").text
            link = biz.find_element(By.XPATH, ".//a[contains(@href, '/biz/')]").get_attribute("href")
        except:
            continue

        try:
            phone = biz.find_element(By.XPATH, ".//p[contains(text(),'(')]").text
        except:
            phone = "Not listed"

        try:
            website = biz.find_element(By.XPATH, ".//a[contains(@href, 'biz_redir')]").get_attribute("href")
        except:
            website = "Not listed"

        results.append({
            "Name": name,
            "Link": link,
            "Phone": phone,
            "Website": website
        })

    driver.quit()
    return results

# Streamlit UI
st.title("Arizona Real Estate Lead Generator")

city = st.text_input("Enter Arizona city name (e.g. Phoenix):")

if st.button("Search"):
    if city.strip() == "":
        st.warning("Please enter a city.")
    else:
        with st.spinner("Searching Yelp..."):
            leads = get_yelp_leads(city)
            if leads:
                df = pd.DataFrame(leads)
                st.success(f"Found {len(leads)} leads!")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download CSV", data=csv, file_name="real_estate_leads.csv", mime="text/csv")
            else:
                st.error("No leads found. Try a different city.")
