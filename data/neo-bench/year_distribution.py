import json
import pandas as pd
import matplotlib.pyplot as plt

input_file = 'neobench_twitter.jsonl'
filtered_output_file = 'neobench_twitter_212223.jsonl'

years = []
filtered_entries = []

with open(input_file, 'r') as infile:
    for line in infile:
        data = json.loads(line)
        if 'date' in data and data['date']:
            year_str = data['date'][:4]
            if year_str.isdigit():
                year = int(year_str)
                years.append(year)
                if year in [2021, 2022, 2023]:
                    filtered_entries.append(data)

filtered_entries.sort(key=lambda x: x['date'])

with open(filtered_output_file, 'w') as outfile:
    for entry in filtered_entries:
        outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')

df = pd.DataFrame(years, columns=['year'])
year_counts = df['year'].value_counts().sort_index()

plt.figure(figsize=(8, 6))
plt.bar(year_counts.index, year_counts.values)
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Distribution of Neologism by Year (Twitter only)')
plt.xticks(year_counts.index)
plt.savefig('neobench_per_year_twitter.png', dpi=300)
plt.show()
