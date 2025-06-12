import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook
import time
import os

def get_yelp_leads(city):
    service = Service(executable_path="/usr/bin/chromedriver")  # Path for Streamlit Cloud
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.yelp.com/search?find_desc=real+estate+agents&find_loc={city.replace(' ', '+')}+AZ"
    driver.get(url)
    time.sleep(5)

    results = []
    listings = driver.find_elements(By.CSS_SELECTOR, "li.border-color--default__09f24__NPAKY")

    for biz in listings[:10]:  # Limit to first 10 for speed
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

        results.append((name, link, phone, website))

    driver.quit()
    return results

def to_excel(data):
    wb = Workbook()
    ws = wb.active
    ws.append(["Business Name", "Yelp Link", "Phone Number", "Website"])
    for row in data:
        ws.append(row)
    file_path = "/tmp/yelp_leads.xlsx"
    wb.save(file_path)
    return file_path

# Streamlit UI
st.title("🏡 Yelp Lead Generator - Real Estate Agents in AZ")
city = st.text_input("Enter city name (e.g., Phoenix):")

if st.button("Generate Leads") and city:
    with st.spinner("Scraping Yelp..."):
        leads = get_yelp_leads(city)
        if leads:
            st.success(f"Found {len(leads)} leads!")
            st.dataframe(leads, use_container_width=True)
            file_path = to_excel(leads)
            with open(file_path, "rb") as f:
                st.download_button("📥 Download Excel File", f, "yelp_leads.xlsx")
        else:
            st.warning("No leads found. Try another city.")
