import json
import os

raw_data_file = os.path.join(os.path.dirname(__file__), "raw", "test1", "test1.json")
splited_data_dir = os.path.join(os.path.dirname(__file__), "splited")
if not os.path.exists(splited_data_dir):
    os.makedirs(splited_data_dir)

print("Using raw data file:", raw_data_file)
print("Splited data dir:", splited_data_dir)

with open(raw_data_file, encoding="utf-8") as f:
    data = json.load(f)
    print("Total data size:", len(data))

# Split data into 5 parts
part_size = len(data) // 5

for i in range(5):
    start = i * part_size
    end = (i + 1) * part_size
    with open(os.path.join(splited_data_dir, f"{start}-{end}.json"), "w", encoding="utf-8") as f:
        json.dump(data[start:end], f, ensure_ascii=False, indent=4)
        print(f"Part {i}: {start}-{end} saved.")
