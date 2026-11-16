import json
import os
import json
from tqdm import tqdm
import subprocess


def preprocess_whatsthatbook_corpus(input_file, output_dir):
    """
    Preprocess the What's that Book dataset before indexing
    """
    os.makedirs(output_dir, exist_ok=True)
    with open(input_file, 'r') as file:
        records = [json.loads(line) for line in file if line.strip()]
        for i, record in enumerate(tqdm(records, desc="Preprocessing corpus")):
            title = record.get("title", "")
            author = record.get("author", "")
            desc_raw = record.get("description", "").rstrip(r"/././.more").strip()
            if len(desc_raw) > 376:
                desc_clean = desc_raw[376:].strip()
            else:
                desc_clean = desc_raw
            genres = record.get("genres", [])
            genre_concat = ", ".join(genres)

            doc_content = f"{title} {author} {desc_clean} {genre_concat}"

            doc = {
                "id": record.get("id", ""),
                "contents": doc_content,
            }
            with open(os.path.join(output_dir, f"doc{i}.json"), 'w') as out:
                json.dump(doc, out)


def build_index(input_dir: str, index_dir: str):
    """
    Build a BM25 index using Pyserini’s command-line interface.
    """
    if os.path.exists(index_dir) and os.listdir(index_dir):
        print(f"Index already exists at {index_dir}. Skipping index building.")
        return

    cmd = [
        "python", "-m", "pyserini.index.lucene",
        "--collection", "JsonCollection",
        "--input", input_dir,
        "--index", index_dir,
        "--generator", "DefaultLuceneDocumentGenerator",
        "--threads", "1",
        "--storePositions", "--storeDocvectors", "--storeRaw",
    ]

    print("Building index (this may take a few minutes)...")
    subprocess.run(cmd, check=True)
    print(f"Index built successfully at {index_dir}")


def main():
    """main function for preprocessing and indexing"""
    raw_data_file = f"data/whatsthatbook_14441_gold_books.jsonl"

    # Directories where the processed corpus and index will be stored for toolkit
    processed_corpus_dir = "processed_corpus"
    os.makedirs(processed_corpus_dir, exist_ok=True)
    index_dir = "book_index"

    # Preprocess corpus
    if not os.path.exists(processed_corpus_dir) or not os.listdir(processed_corpus_dir):
        preprocess_whatsthatbook_corpus(raw_data_file, processed_corpus_dir)
    else:
        print(f"Preprocessed corpus already exists at {processed_corpus_dir}. Skipping preprocessing.")

    # Build index
    build_index(processed_corpus_dir, index_dir)

    print("Preprocessing and indexing completed.")



if __name__ == "__main__":
    main()