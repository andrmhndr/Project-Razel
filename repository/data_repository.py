from model.dialog_model import Dialog
import json

class DataRepository:
    def __init__(self, today, data, full_record):
        self.today = today
        self.data = data
        self.full_record = full_record
        self.record = self.get_record_from_all()
    
    def get_record_from_all(self):
        dialogs = []
        if self.today in self.full_record:
            for content in self.full_record[self.today]:
                dialogs.append(Dialog.fromJson(content=content))
        return dialogs
    
    def record_to_json(self):
        new_record = []
        for dialog in self.record:
            new_record.append(dialog.toJson())
        return new_record
    
    def save_json(self):
        self.full_record[self.today] = self.record_to_json()
        with open('data/record.json', 'w') as output:
            json.dump(self.full_record, output)
    
    # def getRecordList(self):
    #     dialogs = []
    #     if today in self.record:
    #         for contents in record[today]['']