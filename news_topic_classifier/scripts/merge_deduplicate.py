from utils.data_io import get_project_root, save_to_jsonl
from pathlib import Path
import json
import pandas as pd

RAW_FOLDER = "01_raw"
INTERMEDIATE_FOLDER = "02_intermediate"
CRITERIA = 'title'

def main():
    """
        Merge all .jsonl files in a folder into a single JSON Lines file.
    """
    input_folder = get_project_root()/"data"/RAW_FOLDER
    output_file = get_project_root()/"data"/INTERMEDIATE_FOLDER/"merged.jsonl"
    articles = []
    for path in Path(input_folder).glob("*.jsonl"):
        with open(path, "r", encoding = "utf-8") as f:
            for line in f:
                try:
                    articles.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    
    df = pd.DataFrame(articles)
    if CRITERIA in df.columns:
        df = df.drop_duplicates(subset = [CRITERIA])
        articles = df.to_dict(orient = "records")
    save_to_jsonl(articles, Path(output_file).name, Path(output_file).parent)

if __name__ == "__main__":
    main()