import pandas as pd
import requests


class Geocoder:
    def __init__(self, data_file_path, postal_codes_file_path):
        self.data_file_path = data_file_path
        self.postal_codes_file_path = postal_codes_file_path

    def read_data(self):
        self.df = pd.read_csv(self.data_file_path)
        self.postal_codes_df = pd.read_csv(self.postal_codes_file_path)
        self.postal_codes_df["Pincode"] = (
            self.postal_codes_df["Pincode"].fillna(0).astype(str)
        )

    def geocode_data(self):
        # Convert the "pincode" column data type to integer
        self.df["pincode"] = self.df["pincode"].fillna(0).astype(str)

        # Merge the two DataFrames based on the "Pincode" column
        self.df = self.df.merge(
            self.postal_codes_df, left_on="pincode", right_on="Pincode", how="left"
        )

        # Create new columns "Country" and "State"
        self.df["Country", "City"] = "India"

        # Map country to region and add relevant columns
        self.df["country_data"] = self.df["Country"].apply(
            lambda x: self.map_country_to_region(x)
        )
        self.df["Country ID"] = self.df["country_data"].apply(
            lambda x: x.get("Country ID")
        )
        self.df["Region"] = self.df["country_data"].apply(lambda x: x.get("Region"))
        self.df["Region ID"] = self.df["country_data"].apply(
            lambda x: x.get("Region ID")
        )
        self.df["Region Code"] = self.df["country_data"].apply(
            lambda x: x.get("Region Code")
        )

        # Drop unnecessary columns
        self.df.drop(["Pincode"], axis=1, inplace=True)

    def map_country_to_region(self, country_name):
        api_url = "https://api.worldbank.org/v2/country"

        try:
            # Send a request to get country information
            response = requests.get(api_url, params={"format": "json", "per_page": 500})
            data = response.json()

            for country_data in data[1]:
                if country_data["name"] == country_name:
                    country_id = country_data["id"]
                    region_id = country_data["region"]["id"]
                    region = country_data["region"]["value"]
                    region_code = country_data["region"]["iso2code"]
                    return {
                        "Country": country_name,
                        "Country ID": country_id,
                        "Region": region,
                        "Region ID": region_id,
                        "Region Code": region_code,
                    }

            return {"error": "Country not found."}
        except Exception as e:
            return {"error": str(e)}

    def get_geocoded_data(self):
        return self.df
