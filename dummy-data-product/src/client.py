# import dotenv
import logging
from datetime import datetime
from dependencies.cleaning.clean import DataCleaner
from dependencies.geocoding.geocoder import Geocoder
from dependencies.scraping.scraper import Scraper

# dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


def step_2():
    logging.info("Scraped Main Data")
    chromedriver_path = r"C:\Users\derav\Downloads\chromedriver-win64\chromedriver"
    scraper = Scraper(chromedriver_path)

    # Step 1: Scrape organizations
    organizations_url = "https://etenders.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page"
    organizations = scraper.scrape_organizations(organizations_url)
    print(len(organizations))

    # Step 2: Scrape tenders
    tenders = scraper.scrape_tenders(organizations)
    print(len(tenders))

    # # Step 3: Scrape tender data
    datas = scraper.scrape_tender_data(tenders)

    # # Step 4: Save data to CSV
    folder_path = r"C:\Users\derav\Downloads\pt-mesh-pipeline-main\data"
    file_name = "scrapped-data-0.csv"
    full_file_path = f"{folder_path}/{file_name}"
    scraper.save_to_csv(datas, full_file_path)


def step_3():
    logging.info("Cleaned Main Data")
    data_path = (
        r"C:\Users\derav\Downloads\pt-mesh-pipeline-main\data\scrapped-data-1.csv"
    )
    output_path = (
        r"C:\Users\derav\Downloads\pt-mesh-pipeline-main\data\scrapped-cleaned-data.csv"
    )

    # Create an instance of DataCleaner
    cleaner = DataCleaner(data_path)

    # Perform data cleaning
    cleaner.clean_data()

    # Save the cleaned data
    cleaner.save_cleaned_data(output_path)


def step_4():
    logging.info("Geocoding Cleaned Data")
    output_path = r"C:\Users\derav\Downloads\pt-mesh-pipeline-main\data\scrapped-geocoded-data.csv"
    geocoder = Geocoder(
        data_file_path=r"C:\Users\derav\Downloads\pt-mesh-pipeline-main\data\scrapped-data-1.csv",
        postal_codes_file_path=r"C:\Users\derav\Downloads\pt-mesh-pipeline-main\data\csvjson.csv",
    )
    geocoder.read_data()
    geocoder.geocode_data()
    geocoded_data = geocoder.get_geocoded_data()
    geocoded_data.to_csv(output_path, index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="step to be chosen for execution")
    args = parser.parse_args()

    if args.step:
        eval(f"step_{args.step}()")
    else:
        print("Please provide a valid step argument.")

    logging.info(
        {
            "last_executed": str(datetime.now()),
            "status": "Pipeline executed successfully",
        }
    )
