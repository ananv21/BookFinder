Data files:
1) **data**: Contains **whatsthatbook_14441_gold_books.jsonl**, the raw book dataset from the "What's that Book?" Hugging Face repository. There are 14441 records totally; each corresponds to a unique book (with fields like title, author, description, etc.)
2) **processed_corpus**: Cleaned and processed book dataset for indexing use
3) **book_index**: BM25-index over books in the "What's that Book?" dataset

Code files:
1) **preprocess_and_index.py**: Contains functionalities for preprocessing and indexing the "What's that Book" gold books dataset
