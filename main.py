import customtkinter as gui
from datetime import datetime
import json
import asyncio

from repository.data_repository import DataRepository
from view.main_view import *
from model.dialog_model import *
from controller.main_controller import *

def main():
    # initialize
    today = datetime.now().strftime("%Y-%m-%d")
    record_data = json.load(open('data/record.json'))
    api_data = json.load(open('data/data.json'))
    
    root = gui.CTk()
    repository = DataRepository(today, api_data, record_data)
    view = MainView(root, "Project-Razel")
    controller = MainController(view, repository)
    controller.create_view()
    
    root.mainloop()
    
if __name__ == '__main__':
    main()