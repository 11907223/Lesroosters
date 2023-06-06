import pandas as pd
import os


def load_file(academic_data: str) -> None:
    """ Load the specified .csv file in a JSON format. 
    
        academic_data (str): file to load. 
            Either "studenten_en_vakken", "vakken or "zalen".
    """
    # Source:
    # https://stackoverflow.com/questions/68921025/converting-the-csv-file-to-specified-json-format
    file_path = os.path.abspath(f"lesroosters/data/{academic_data}.csv")
    df = pd.read_csv(file_path)
    print(df)

    dic = {}

    
load_file("zalen")
