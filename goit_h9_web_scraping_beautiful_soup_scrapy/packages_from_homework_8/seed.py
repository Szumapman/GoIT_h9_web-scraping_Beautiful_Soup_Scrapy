import json
from datetime import datetime

from .models import Author, Quote, Tag
from .connect import connect


def load_json_data(path):
    with open(path, "r", encoding='utf-8') as f:
        data = json.load(f)
        return data


def data_seed(authors, quotes):
    for author in authors:
        author_model = Author()
        author_model.name = author["fullname"]
        author_model.born_date = datetime.strptime(author["born_date"], "%B %d, %Y").date()
        author_model.born_location = author["born_location"]
        author_model.description = author["description"]
        author_model.save()
        for quote in quotes:
            tags = []
            if quote["author"] == author["fullname"]:
                for tag in quote["tags"]:
                    tags.append(Tag(name=tag))
                Quote(quote=quote["quote"], author=author_model, tags=tags).save()


if __name__ == "__main__":
    authors = load_json_data("data/authors.json")
    quotes = load_json_data("data/quotes.json")
    data_seed(authors, quotes)
