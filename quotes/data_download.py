import json
from connection import connect
from mongo_models import Author, Quote


def upload_authors_to_json(filename):
    author_data = Author.objects().to_json()

    with open(filename, "w") as f:
        json.dump({"authors": json.loads(author_data)}, f)


def upload_quotes_to_json(filename):
    quotes_data = []

    for quote in Quote.objects():
        
        quote_dict = {
            "quote": quote.quote,
            "tags": quote.tags,
            "author": quote.author.fullname,
        }
        quotes_data.append(quote_dict)

    with open(filename, "w") as f:
        json.dump({"quotes": quotes_data}, f)


if __name__ == "__main__":
    upload_authors_to_json("mongodb_authors_data.json")
    upload_quotes_to_json("mongodb_quotes_data.json")
