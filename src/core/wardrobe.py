import csv
import pandas as pd
from shiny import App, ui, render

class wardrobe:
    def __init__(self):
        self.clothing_categories = self.__load_file("clothing_categories")
        
    def __load_file(self, table_name):
        data_file = f'data/prod/{table_name}.csv'
        try:
            return pd.read_csv(data_file)
        except FileNotFoundError:
            print(f"Data file {data_file} not found.")

my_wardrobe = wardrobe()

app_ui = ui.page_fluid(
    ui.h2("Wardrobe Clothing Categories"),
    ui.output_data_frame("categories_df")
)

def server(input, output, session):
    @output
    @render.data_frame
    def categories_df():
        return my_wardrobe.clothing_categories

app = App(app_ui, server)