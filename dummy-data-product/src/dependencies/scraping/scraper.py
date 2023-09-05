import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import time as tm


class Scraper:
    def __init__(self, chromedriver_path):
        self.chromedriver_path = chromedriver_path
        self.service = ChromeService(executable_path=chromedriver_path)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")

    def scrape_organizations(self, url):
        driver = webdriver.Chrome(service=self.service, options=self.options)
        driver.get(url)
        content = driver.page_source.encode("utf-8").strip()
        soup = BeautifulSoup(content, "html.parser")
        div_1 = soup.find("div", {"id": "content"})
        table = div_1.find("table", {"id": "table"})
        a_tag = table.find_all("a", {"class": "link2"})
        organizations = []

        for i in a_tag:
            link = i.get("href")
            organizations.append(link)

        driver.quit()
        return organizations

    def scrape_tenders(self, organizations):
        tenders = []
        for i in organizations:
            link = "https://etenders.gov.in" + str(i)
            url = link
            driver = webdriver.Chrome(service=self.service, options=self.options)
            driver.get(url)
            driver.find_element(By.LINK_TEXT, "restart").click()
            tm.sleep(2)
            driver.get(url)
            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content, "html.parser")
            table = soup.find("table", {"id": "table"})
            a_tags = table.find_all("a")

            for i in a_tags:
                a_link = i.get("href")
                tenders.append(a_link)

            driver.quit()
            # break

        return tenders

    def scrape_tender_data(self, tenders):
        datas = []
        failed_links = []
        for i in range(0, len(tenders)):
            link = "https://etenders.gov.in" + str(tenders[i])
            url = link

            try:
                driver = webdriver.Chrome(service=self.service, options=self.options)
                driver.get(url)
            except Exception as e:
                failed_links.append(url)
                tm.sleep(5)
                print(e)

            driver.find_element(By.LINK_TEXT, "restart").click()
            tm.sleep(2)
            driver.get(url)
            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content, "html.parser")
            table = soup.find_all("table", {"class": "tablebg"})
            n = len(table)

            tender_data = {}  # Initialize an empty dictionary to store tender data

            try:
                table_0_tr = table[0].find_all("tr")
                td = table_0_tr[2].find_all("td")
                original_id = td[1].text.strip()
                tender_data["original_id"] = original_id
            except Exception as e:
                tender_data["original_id"] = None
                print(e)

            try:
                table_0_tr = table[0].find_all("tr")
                td = table_0_tr[3].find_all("td")
                status = td[1].text.strip()
                tender_data["status"] = status
            except Exception as e:
                tender_data["status"] = None
                print(e)

            try:
                table_5_tr = table[5].find_all("tr")
                td = table_5_tr[0].find_all("td")
                name = td[1].text.strip()
                tender_data["name"] = name
            except Exception as e:
                tender_data["name"] = None
                print(e)

            try:
                table_5_tr = table[5].find_all("tr")
                td = table_5_tr[1].find_all("td")
                desc = td[1].text.strip()
                tender_data["desc"] = desc
            except Exception as e:
                tender_data["desc"] = None
                print(e)

            try:
                table_5_tr = table[5].find_all("tr")
                td = table_5_tr[4].find_all("td")
                budget = td[1].text.strip()
                tender_data["budget"] = budget
            except Exception as e:
                tender_data["budget"] = None
                print(e)

            try:
                table_5_tr = table[5].find_all("tr")
                td = table_5_tr[4].find_all("td")
                sector = td[3].text.strip()
                tender_data["sector"] = sector
            except Exception as e:
                tender_data["sector"] = None
                print(e)

            try:
                table_5_tr = table[5].find_all("tr")
                td = table_5_tr[4].find_all("td")
                sub_sector = td[5].text.strip()
                tender_data["sub_sector"] = sub_sector
            except Exception as e:
                tender_data["sub_sector"] = None
                print(e)

            try:
                table_5_tr = table[5].find_all("tr")
                td = table_5_tr[5].find_all("td")
                contract = td[1].text.strip()
                tender_data["contract"] = contract
            except Exception as e:
                tender_data["contract"] = None
                print(e)

            try:
                table_5_tr = table[5].find_all("tr")
                td = table_5_tr[6].find_all("td")
                state = td[1].text.strip()
                tender_data["state"] = state
            except Exception as e:
                tender_data["state"] = None
                print(e)

            try:
                table_5_tr = table[5].find_all("tr")
                td = table_5_tr[6].find_all("td")
                pincode = td[3].text.strip()
                tender_data["pincode"] = pincode
            except Exception as e:
                tender_data["pincode"] = None
                print(e)

            try:
                table_6_tr = table[6].find_all("tr")
                td = table_6_tr[0].find_all("td")
                published_date = td[1].text.strip()
                tender_data["published_data"] = published_date
            except Exception as e:
                tender_data["published_data"] = None
                print(e)

            try:
                table_6_tr = table[6].find_all("tr")
                td = table_6_tr[0].find_all("td")
                bid_opening_date = td[3].text.strip()
                tender_data["bid_opening_date"] = bid_opening_date
            except Exception as e:
                tender_data["bid_opening_date"] = None
                print(e)

            try:
                table_6_tr = table[6].find_all("tr")
                td = table_6_tr[3].find_all("td")
                submission_start_date = td[1].text.strip()
                tender_data["submission_start_date"] = submission_start_date
            except Exception as e:
                tender_data["submission_start_date"] = None
                print(e)

            try:
                table_6_tr = table[6].find_all("tr")
                td = table_6_tr[3].find_all("td")
                submission_end_date = td[3].text.strip()
                tender_data["submission_end_date"] = submission_end_date
            except Exception as e:
                tender_data["submission_end_date"] = None
                print(e)

            try:
                a_tag = soup.find("a", {"id": "DirectLink_8"})
                document_url = f"https://etenders.gov.in{a_tag.get('href')}"
                tender_data["document_url"] = document_url
            except Exception as e:
                tender_data["document_url"] = None
                print(e)

            try:
                table_n_tr = table[n - 1].find_all("tr")
                td = table_n_tr[1].find_all("td")
                location = td[1].text.strip()
                tender_data["location"] = location
            except Exception as e:
                tender_data["location"] = None
                print(e)

                datas.append(tender_data)

                driver.quit()
            # break

        return datas

    def save_to_csv(self, datas, csv_file_path):
        new_data = pd.DataFrame.from_dict(datas)
        pd.set_option("display.max_rows", None)
        new_data.head(110)
        new_data.to_csv(csv_file_path, index=False)
