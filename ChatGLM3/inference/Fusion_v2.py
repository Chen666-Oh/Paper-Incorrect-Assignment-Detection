import json

with open(f'./result/title_v2.json', 'r') as f:
    data1 = json.load(f)
with open(f'./result/author_v2.json', 'r') as f:
    data2 = json.load(f)
with open(f'./result/all_info_v2.json', 'r') as f:
    data3 = json.load(f)

merged_dict = {}
for author, score_dict in data1.items():
    merged_dict[author] = {}
    for pid, score in score_dict.items():
        merged_dict[author][pid] = data1[author][pid] * 0.3 + data2[author][pid] * 0.1 + data3[author][pid] * 0.6

with open(f'./result/merge_v2.json', 'w') as f:
    json.dump(merged_dict, f)
