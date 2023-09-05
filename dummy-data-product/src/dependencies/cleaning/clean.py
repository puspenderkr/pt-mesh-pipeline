import pandas as pd
import ast


class DataCleaner:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = pd.read_csv(self.data_path)

    def clean_data(self):
        self.df["budget"] = self.df["budget"].apply(self.rupees_to_dollars)
        self.df["city"] = self.df["state"].apply(self.extract_last_word)
        self.df["project_or_tender"] = self.df["project_or_tender"].apply(
            self.convert_text
        )

        # Apply the conversion function to the "timestamp_range" column
        # self.df["timestamp_range"] = self.df["timestamp_range"].apply(
        #     self.convert_timestamps
        # )
        self.df["min_max"] = self.df["timestamp_range"].apply(self.min_max)

    def rupees_to_dollars(self, amount_rupees):
        amount_rupees = str(amount_rupees)
        amount_rupees = amount_rupees.replace(",", "")  # Remove commas
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

    # def convert_timestamps(self, timestamp_str):
    #     try:
    #         # timestamp_dict = ast.literal_eval(timestamp_str)
    #         json_str_double_quotes = timestamp_str.replace("'", '"')
    #         timestamp_dict = json.loads(json_str_double_quotes)
    #         formatted_dict = {}
    #         for key, value in timestamp_dict.items():
    #             if value is None:
    #                 formatted_dict[key] = None
    #             else:
    #                 formatted_dict[key] = pd.to_datetime(
    #                     value, format="%d-%b-%Y %I:%M %p"
    #                 ).strftime("%Y-%m-%d %H:%M:%S")
    #         return formatted_dict
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return {}

    def min_max(self, timestamp_range):
        timestamp_dict = ast.literal_eval(timestamp_range)
        non_null_values = [val for val in timestamp_dict.values() if val is not None]

        if non_null_values:
            return {"min": min(non_null_values), "max": max(non_null_values)}
        else:
            return None

    def save_cleaned_data(self, output_path):
        self.df.to_csv(output_path, index=False)
