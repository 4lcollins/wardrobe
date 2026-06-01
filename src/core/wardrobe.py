import pandas as pd

class Wardrobe:
    def __init__(self):
        self.clothing_categories = self.__load_file("clothing_categories")
        
    def __load_file(self, table_name):
        data_file = f'data/prod/{table_name}.csv'
        try:
            return pd.read_csv(data_file)
        except FileNotFoundError:
            print(f"Data file {data_file} not found.")
