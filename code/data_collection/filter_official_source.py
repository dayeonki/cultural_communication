# import json

# input_file = "../data/naver_opendict_ko.jsonl"
# output_file = "../data/naver_opendict_ko_official.jsonl"


# with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
#     for line in infile:
#         data = json.loads(line)
#         if data.get("writer") == "국어사전 신조어":
#             outfile.write(json.dumps(data, ensure_ascii=False) + "\n")



# Find distribution of year
import json
import matplotlib.pyplot as plt
from collections import Counter

input_file = "../data/naver_opendict_ko.jsonl"
year_counter = Counter()

with open(input_file, "r", encoding="utf-8") as infile:
    for line in infile:
        data = json.loads(line)
        date = data.get("date", "")
        if date:
            year = int(date.split("-")[0])
            year_counter[year] += 1

print("Year Count:", year_counter)
sorted_years = sorted(year_counter.items())
years, counts = zip(*sorted_years)

# Plot year distribution
plt.figure(figsize=(10, 5))
plt.bar(years, counts)
plt.xlabel("Year")
plt.ylabel("Count")
plt.xticks(years, rotation=45)
plt.savefig("year_distribution.png", bbox_inches='tight', dpi=300)