import json
import psycopg2
from quotes.settings import DATABASES

postgres_conn = psycopg2.connect(
    dbname=DATABASES["default"]["NAME"],
    user=DATABASES["default"]["USER"],
    password=DATABASES["default"]["PASSWORD"],
    host=DATABASES["default"]["HOST"],
    port=DATABASES["default"]["PORT"],
)
postgres_cursor = postgres_conn.cursor()


def delete_all_data():
    postgres_cursor.execute("DELETE FROM quotesapp_quote_tags")
    postgres_cursor.execute("DELETE FROM quotesapp_quote")
    postgres_cursor.execute("DELETE FROM quotesapp_tag")
    postgres_cursor.execute("DELETE FROM quotesapp_author")
    postgres_conn.commit()


def import_author_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        authors = data["authors"]

        for author in authors:
            postgres_cursor.execute(
                "INSERT INTO quotesapp_author (fullname, born_date, born_location, description) VALUES (%s, %s, %s, %s)",
                (
                    author["fullname"],
                    author["born_date"],
                    author["born_location"],
                    author["description"],
                ),
            )

    postgres_conn.commit()


def import_quote_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        quotes = data["quotes"]

        tag_names = set()
        for quote in quotes:
            tag_names.update(quote["tags"])

        for tag_name in tag_names:
            postgres_cursor.execute(
                "INSERT INTO quotesapp_tag (name) VALUES (%s)",
                (tag_name,),
            )

        for quote in quotes:
            author_name = quote["author"]
            author_id = None

            postgres_cursor.execute(
                "SELECT id FROM quotesapp_author WHERE fullname = %s", (author_name,)
            )
            result = postgres_cursor.fetchone()
            if result:
                author_id = result[0]

            if author_id is not None:
                postgres_cursor.execute(
                    "INSERT INTO quotesapp_quote (author_id, quote) VALUES (%s, %s) RETURNING id",
                    (author_id, quote["quote"]),
                )
                quote_id = postgres_cursor.fetchone()[0]

                for tag_name in quote["tags"]:
                    postgres_cursor.execute(
                        "SELECT id FROM quotesapp_tag WHERE name = %s", (tag_name,)
                    )
                    tag_id = postgres_cursor.fetchone()[0]
                    postgres_cursor.execute(
                        "INSERT INTO quotesapp_quote_tags (quote_id, tag_id) VALUES (%s, %s)",
                        (quote_id, tag_id),
                    )

    postgres_conn.commit()
    postgres_cursor.close()
    postgres_conn.close()


if __name__ == "__main__":
    delete_all_data()
    import_author_from_json("mongodb_authors_data.json")
    import_quote_from_json("mongodb_quotes_data.json")
