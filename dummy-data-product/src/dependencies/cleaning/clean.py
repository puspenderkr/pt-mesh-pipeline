import pandas as pd
import ast
from datetime import datetime


class DataCleaner:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = pd.read_csv(self.data_path)

    def clean_data(self):
        self.df["budget"] = self.df["budget"].apply(self.rupees_to_dollars)
        self.df["city"] = self.df["state"].apply(self.extract_last_word)
        self.df.drop(["state"], axis=1, inplace=True)
        self.df["project_or_tender"] = self.df["project_or_tender"].apply(
            self.convert_text
        )

        # Apply the conversion function to the "timestamp_range" column
        self.df["timestamp_range"] = self.df["timestamp_range"].apply(
            self.convert_timestamps
        )
        self.df["min_max"] = self.df["timestamp_range"].apply(self.min_max)

    def rupees_to_dollars(self, amount_rupees):
        if not isinstance(amount_rupees, (int, float, str)):
            return None

        if isinstance(amount_rupees, str):
            # Remove commas and check if it's a valid numeric string
            amount_rupees = amount_rupees.replace(",", "")
            if not amount_rupees.replace(".", "", 1).isdigit():
                return None

        amount_rupees = float(amount_rupees)  # Convert to float
        amount_dollars = amount_rupees * 0.013  # Convert to dollars
        return f"{amount_dollars:.2f}$"

    def extract_last_word(self, city_text):
        city_text = str(city_text)
        return city_text.split(",")[-1].strip()

    def convert_text(self, text):
        text = str(text)
        if "tender" in text.lower():
            return "T"
        elif "project" in text.lower():
            return "P"
        else:
            return text

    def convert_timestamps(self, timestamp):
        try:
            if isinstance(timestamp, str):
                timestamp_dict = ast.literal_eval(timestamp)
                if isinstance(timestamp_dict, dict):
                    for key, value in timestamp_dict.items():
                        if value is not None:
                            timestamp_dict[key] = datetime.strptime(
                                value, "%d-%b-%Y %I:%M %p"
                            ).strftime("%Y-%m-%d %H:%M:%S")
                    return timestamp_dict
        except (ValueError, SyntaxError):
            pass
        return timestamp

    def min_max(self, timestamp_range):
        if isinstance(timestamp_range, dict):
            non_null_values = [
                val for val in timestamp_range.values() if val is not None
            ]

            if non_null_values:
                return {"min": min(non_null_values), "max": max(non_null_values)}
        return None

    def save_cleaned_data(self, output_path):
        self.df.to_csv(output_path, index=False)
