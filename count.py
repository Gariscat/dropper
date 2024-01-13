import pandas as pd
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json

label_df = pd.read_csv("annotations/class_labels_indices.csv")
label_decode_map = {row["mid"]: row["display_name"] for _, row in label_df.iterrows()}


def process_csv(csv_path: str, print: str = False) -> None:
    label_cnt = dict()
    
    with open(csv_path, "r") as f:
        lines = f.readlines()
        lines = lines[3:] # exclude header
        
    for i, line in tqdm(enumerate(lines)):
        line = line.strip()
        line = line.split(",")
        for _ in line[3:]:
            id = _.strip('" ')
            if label_decode_map[id] not in label_cnt:
                label_cnt[label_decode_map[id]] = 1
            else:
                label_cnt[label_decode_map[id]] += 1
                
    df = pd.DataFrame.from_dict(label_cnt, orient="index", columns=["cnt"])
    """"""
    if print:
        print(df)
        plt.figure(num=None, figsize=(20,18), dpi=80, facecolor='w', edgecolor='r')
        sns.barplot(x=df.index, y=df.cnt)
        plt.show()
        plt.close()
    
    output_path = csv_path.replace(".csv", "_cnt.json")
    with open(output_path, 'w') as f:
        json.dump(label_cnt, f, indent=4)
        
if __name__ == "__main__":
    process_csv("annotations/eval_segments.csv")
    process_csv("annotations/balanced_train_segments.csv")
    process_csv("annotations/unbalanced_train_segments.csv")
    
    # print(label_cnt)
    