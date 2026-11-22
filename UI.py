import streamlit as st
from pyserini.search.lucene import LuceneSearcher

from bm25_retrieval import load_books, search_books


@st.cache_resource
def load_resources():
    books = load_books("data/whatsthatbook_14441_gold_books.jsonl")
    searcher = LuceneSearcher("book_index")
    searcher.set_bm25(k1=0.9, b=0.4)
    return books, searcher


st.title("BookFinder")
st.write("Describe a book you remember and we will try to find it.")

books, searcher = load_resources()

query = st.text_area("Book description", height=150)
top_k = st.slider("Number of results", 1, 20, 10)

if st.button("Search") and query.strip():
    results = search_books(searcher, books, query, top_k=top_k)
    if not results:
        st.write("No results found.")
    for rank, r in enumerate(results, start=1):
        record = books[r["id"]]
        st.subheader(f"{rank}. {r['title']}")
        st.write(f"by {r['author']} | score: {r['score']:.3f}")
        with st.expander("Description"):
            st.write(record.get("description", ""))
