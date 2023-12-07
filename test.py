import json

json_filename="data/user.json"

with open(json_filename,"r") as read_file:
	db = json.load(read_file)

print(db)