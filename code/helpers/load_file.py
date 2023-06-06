import pandas as pd
import os
from json import loads

def load_file(academic_data: str) -> dict[dict[str]]:
    """Load the specified .csv file in a JSON format.

    academic_data (str): file to load.
        Either "studenten_en_vakken", "vakken or "zalen".
    """
    # Source:
    # https://stackoverflow.com/questions/68921025/converting-the-csv-file-to-specified-json-format
    file_path = os.path.abspath(f"../data/{academic_data}.csv")
    df = pd.read_csv(file_path)
    return loads(df.to_json(orient="columns"))
