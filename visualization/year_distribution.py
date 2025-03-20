import json
import matplotlib.pyplot as plt
from collections import Counter


file_path = '../data/naver_opendict_ko_official.jsonl'
years = []

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        year = data.get("date", "").split("-")[0]
        if year:
            years.append(year)



year_counts = Counter(years)

sorted_years = sorted(year_counts.keys())
sorted_counts = [year_counts[year] for year in sorted_years]

plt.figure(figsize=(8, 5))
plt.bar(sorted_years, sorted_counts, color='black')
plt.xlabel("Year")
plt.ylabel("Frequency")
plt.xticks(rotation=45)
plt.savefig("year_distribution.png", bbox_inches='tight', pad_inches=0.1, dpi=300)
