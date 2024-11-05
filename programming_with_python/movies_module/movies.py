import pandas as pd
import os
from typing import Dict, List


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
        return results


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
