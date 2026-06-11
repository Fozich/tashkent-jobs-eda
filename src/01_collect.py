"""Collect vacancy counts from hh.uz public search pages.

The official hh API (api.hh.ru) now returns 403 for anonymous calls to
/vacancies, so this script reads the result count shown on the public
search page instead. One request per keyword, ~1s apart, with a normal
browser User-Agent — polite scraping of a public counter, nothing more.

Output: data/skill_demand.csv
"""

import csv
import re
import time

import requests

AREA_TASHKENT = 2759  # hh.ru area id (see api.hh.ru/areas/2759)

# (label, search query) — Russian terms, because most Tashkent postings
# on hh.uz are written in Russian.
KEYWORDS = [
    ("all vacancies", ""),
    ("analyst (any)", "аналитик"),
    ("data analyst", "аналитик данных"),
    ("financial analyst", "финансовый аналитик"),
    ("economist", "экономист"),
    ("data scientist", "data scientist"),
    ("intern", "стажер"),
    ("junior", "junior"),
    ("1C", "1С"),
    ("Excel", "Excel"),
    ("SQL", "SQL"),
    ("Python", "Python"),
    ("Power BI", "Power BI"),
    ("Tableau", "Tableau"),
    ("machine learning", "machine learning"),
]

# The count appears in the page as e.g. "954 вакансии"
COUNT_RE = re.compile(r"([\d][\d\s ]{0,11})ваканси[йия]")

HEADERS = {"User-Agent": "Mozilla/5.0 (tashkent-jobs-eda; student project)"}


def fetch_count(query: str) -> int | None:
    params = {"area": AREA_TASHKENT}
    if query:
        params["text"] = query
    r = requests.get("https://tashkent.hh.uz/search/vacancy",
                     params=params, headers=HEADERS, timeout=30)
    r.raise_for_status()
    text = re.sub(r"<[^>]+>", " ", r.text)  # strip tags before matching
    m = COUNT_RE.search(text)
    return int(re.sub(r"\D", "", m.group(1))) if m else None


def main() -> None:
    rows = []
    for label, query in KEYWORDS:
        count = fetch_count(query)
        rows.append({"label": label, "query": query, "vacancies": count})
        print(f"{label:18s} {count}")
        time.sleep(1)  # stay polite

    with open("data/skill_demand.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["label", "query", "vacancies"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
