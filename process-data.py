import json

with open("./train/d.json") as f:
    data = json.load(f)

for i in data[:300]:
    i["task_name"] = "dialog"

for i in data[300:]:
    i["task_name"] = "picture"

with open("./train/d-with-taskname.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
