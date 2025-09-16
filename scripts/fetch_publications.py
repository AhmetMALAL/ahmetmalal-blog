#!/usr/bin/env python3
"""
Fetch publications from Google Scholar and write to data/publications.json.
Requires: scholarly

Usage:
  python scripts/fetch_publications.py --user-id FGRibN8AAAAJ --out data/publications.json
"""
import argparse
import json
from scholarly import scholarly


def fetch_publications(user_id: str):
    author = scholarly.search_author_id(user_id)
    author = scholarly.fill(author, sections=["publications"])
    pubs = []
    for pub in author.get("publications", []):
        filled = scholarly.fill(pub)
        bib = filled.get("bib", {})
        title = bib.get("title")
        authors = ", ".join(bib.get("author", [])) if isinstance(bib.get("author"), list) else bib.get("author")
        year = int(bib.get("pub_year")) if bib.get("pub_year") else None
        venue = bib.get("venue") or bib.get("journal") or bib.get("booktitle")
        eprint = filled.get("eprint_url")
        doi = bib.get("doi")

        pubs.append({
            "title": title,
            "authors": authors,
            "year": year,
            "venue": venue,
            "links": {
                "pdf": eprint,
                "doi": doi
            }
        })
    # Sort by year desc then title
    pubs.sort(key=lambda x: (x.get("year") or 0, x.get("title") or ""), reverse=True)
    return pubs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--out", default="data/publications.json")
    args = parser.parse_args()

    pubs = fetch_publications(args.user_id)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(pubs, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(pubs)} publications to {args.out}")


if __name__ == "__main__":
    main()


