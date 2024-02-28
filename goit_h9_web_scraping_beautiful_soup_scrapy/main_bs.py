import json

import requests
from bs4 import BeautifulSoup

from packages_from_homework_8.seed import load_json_data, data_seed

"""Script for scraping quotes from https://quotes.toscrape.com/, saving them to a JSON file and
then seeding the database with them - according to the homework assignment (see the README.md file).
"""

URL = "https://quotes.toscrape.com"

# lists of dict to create a JSON file on them
TAGS_LIST_AUTHORS_QUOTES = []
AUTHORS_BORN_DATES_LOCATIONS_DESCRIPTIONS = []


def seed_tags_list_authors_quotes() -> dict:
    """function that feels TAGS_LIST_AUTHORS_QUOTES list and return dict with urls about authors"""
    url_to_request = URL
    about_authors_links = {}
    print("Scraping qutotes started ...")
    while True:
        response = requests.get(url_to_request)
        soup = BeautifulSoup(response.text, "lxml")
        quotes = soup.find_all("span", class_="text")
        authors = soup.find_all("small", class_="author")
        abouts = soup.select("span a")
        tags_lists = soup.find_all("div", class_="tags")
        next_page = soup.find("li", class_="next")

        for quote, author, about, tags in zip(quotes, authors, abouts, tags_lists):
            tags_for_quote = tags.find_all("a", class_="tag")
            about_href = about.get("href")
            about_authors_links[author.get_text()] = f"{URL}{about_href}"
            TAGS_LIST_AUTHORS_QUOTES.append(
                {
                    "tags": [
                        tag_for_quote.text.strip() for tag_for_quote in tags_for_quote
                    ],
                    "author": author.get_text().strip(),
                    "quote": quote.text,
                }
            )

        if next_page:
            url_to_request = f"{URL}{next_page.find('a')['href']}"
            print("Scraping next page...")
        else:
            print("Scraping quotes finished.")
            break
    return about_authors_links


def seed_authors_born_dates_locations_descriptions(urls_about_authors: dict) -> None:
    print("Scraping authors started...")
    for author, link in urls_about_authors.items():
        print(f"Scraping information about: {author}")
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "lxml")

        AUTHORS_BORN_DATES_LOCATIONS_DESCRIPTIONS.append(
            {
                "fullname": author,
                "born_date": soup.select("[class='author-born-date']")[0].text.strip(),
                "born_location": soup.select("[class='author-born-location']")[
                    0
                ].text.strip(),
                "description": soup.select("[class='author-description']")[0].text.strip(),
            }
        )
    print("Scraping authors finished.")


def save_json_file(data: list, file_name: str) -> None:
    print(f"Saving {file_name} file...")
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(
            json.dumps(data, ensure_ascii=False, indent=4)
        )


def main():
    about_authors_links = seed_tags_list_authors_quotes()
    seed_authors_born_dates_locations_descriptions(about_authors_links)
    save_json_file(TAGS_LIST_AUTHORS_QUOTES, "data/quotes.json")
    save_json_file(AUTHORS_BORN_DATES_LOCATIONS_DESCRIPTIONS, "data/authors.json")

    print("Seeding data in database using packages from homework #8...")
    authors = load_json_data("data/authors.json")
    quotes = load_json_data("data/quotes.json")
    data_seed(authors, quotes)
    print("All done!")


if __name__ == "__main__":
    main()
