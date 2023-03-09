
import json
from model.dialog_model import Dialog
 
# Data to be written

# dictionary = {
#     "name": "sathiyajith",
#     "rollno": 56,
#     "cgpa": 8.6,
#     "phonenumber": "9976770500"
# }

test = Dialog('user', 'test')
 
dictionary = [test.toJson(), test.toJson()]
 
with open("data/sample.json", "w") as outfile:
    json.dump(dictionary, outfile)