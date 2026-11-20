import json
from pyserini.search.lucene import LuceneSearcher


def load_books(book_file):
    books = {}
    with open(book_file, 'r') as f:
        for line in f:
            record = json.loads(line)
            books[record["id"]] = record
    return books


def search_books(searcher, books, query, top_k=10):
    query = " ".join(query.split()[:500])
    hits = searcher.search(query, k=top_k)
    results = []
    for hit in hits:
        record = books[hit.docid]
        results.append({
            "id": hit.docid,
            "score": hit.score,
            "title": record["title"],
            "author": record["author"],
        })
    return results


def print_results(results):
    rank = 1
    for r in results:
        print(f"{rank}. {r['title']} by {r['author']} (score: {round(r['score'], 3)})")
        rank = rank + 1


def main():
    books = load_books("data/whatsthatbook_14441_gold_books.jsonl")
    searcher = LuceneSearcher("book_index")
    searcher.set_bm25(k1=0.9, b=0.4)

    while True:
        query = input("\nDescribe the book (or type quit): ")
        if query == "quit":
            break
        results = search_books(searcher, books, query, top_k=10)
        print_results(results)


if __name__ == "__main__":
    main()
