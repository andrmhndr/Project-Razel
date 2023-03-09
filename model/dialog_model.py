class Dialog:
    def __init__(self, role, content):
        self.role = role
        self.content = content
    
    def fromJson(content):
        return Dialog(role=content['role'], content=content['content'])
        # dialogs = []
        # if today in record_data:
        #     for contents in record_data[today]["contents"]:
        #         dialogs.append(Dialog(role=contents['role'],dialog=contents['dialog']))
        
        # return dialogs
    
    def toJson(self):
        return {'role' : self.role, 'content' : self.content}
