import pandas as pd
import os
from typing import Dict, List
import matplotlib.pyplot as plt


class MovieServices:
    def __init__(self):
        self.streaming_movies = load_streaming_services_movies()

    def search_movie_in_platforms(self, movie: str, country=None) -> List[str]:
        results = []
        for key, df in self.streaming_movies.items():
            if 'title' in df.columns:  # Check if the column exists in the current DataFrame
                # Find rows where the column contains the search string
                matching_rows = df[df['title'].str.contains(
                    movie, case=False, na=False)]
                if not matching_rows.empty:
                    # Add matching rows to the results dictionary
                    results.append(key)
        print(results)
        return results

    def filtered_movies_per_country(self, country: str) -> dict:
        filtered_movies = {}
        column_name = "availableCountries"

        for key, df in self.streaming_movies.items():
            if column_name in df.columns:
                filtered_df = df[df[column_name].str.contains(
                    rf'\b{country}\b', case=False, na=False)]
                if not filtered_df.empty:
                    filtered_movies[key] = filtered_df

        return filtered_movies

    def show_amount_of_movies_per_country(self, country: str) -> None:
        movies_per_platform = self.filtered_movies_per_country(country=country)

        # Define the specific order and colors for each key
        key_order = ['amazon_prime', 'apple_tv', 'hbo_max', 'hulu', 'netflix']
        colors = {
            'amazon_prime': 'blue',
            'apple_tv': 'orange',
            'hbo_max': 'green',
            'hulu': 'purple',
            'netflix': 'red'
        }

        counts = {key: len(df) for key, df in movies_per_platform.items()}
        # Sort the counts by the specified key order
        sorted_keys = list(counts.keys())
        sorted_counts = [counts[key] for key in sorted_keys]
        sorted_colors = [colors[key] for key in sorted_keys]

        # Plot the bar chart with the sorted order and specified colors
        plt.figure(figsize=(10, 6))
        plt.bar(sorted_keys, sorted_counts, color=sorted_colors)
        plt.xlabel("Streaming Platform")
        plt.ylabel("Quantity of Movies")
        plt.title("Amount of Movies per Streaming Platform")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.2)
        plt.show()


def load_streaming_services_movies() -> Dict[str, pd.DataFrame]:

    dataframes = {}
    folder_path = "programming_with_python/movies_module"

    # Path to the folder containing the CSV files
    folder_path = "programming_with_python/movies_module"

    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        # Check if the file ends with "_data.csv"
        if filename.endswith("_data.csv"):
            # Generate the key by removing "_data.csv" from the filename
            key = filename.replace("_data.csv", "")

            # Load the CSV file into a DataFrame and store it in the dictionary
            file_path = os.path.join(folder_path, filename)
            dataframes[key] = pd.read_csv(file_path)

    return dataframes
