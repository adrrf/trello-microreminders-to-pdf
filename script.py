import argparse
import os

import requests
from dotenv import load_dotenv
from markdown_pdf import MarkdownPdf, Section

load_dotenv()


def obtain_cards_by_column(column_id):
    url = "https://api.trello.com/1/lists/" + column_id + "/cards"

    headers = {"Accept": "application/json"}

    query = {"key": os.getenv("TRELLO_API_KEY"), "token": os.getenv("TRELLO_API_TOKEN")}

    response = requests.get(url, headers=headers, params=query)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

        return None


def check_cache(title):
    return os.path.exists(f"./.cache/{title}.md")


def check_output(title):
    return os.path.exists(f"./outputs/{title}.pdf")


def obtain_cards_title_description(cards):
    result = {}
    if not os.path.exists("./.cache"):
        os.makedirs("./.cache")
    for card in cards:
        title = card["name"]
        description = card["desc"]
        result.update({title: description})
        if not check_cache(title):
            with open(f"./.cache/{title}.md", "w") as f:
                f.write(description)
    return result


def markdown_to_pdf(title, markdown_string):
    pdf = MarkdownPdf()
    pdf.add_section(Section(markdown_string))
    if not os.path.exists("./outputs"):
        os.makedirs("./outputs")
    pdf.save("./outputs/" + title + ".pdf")


def main(column_id):
    cards = obtain_cards_by_column(column_id)
    if cards:
        cards_title_description = obtain_cards_title_description(cards)
        for title, description in cards_title_description.items():
            if not check_output(title):
                markdown_to_pdf(title, description)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch Trello cards and generate PDFs."
    )
    parser.add_argument(
        "column_id", help="The ID of the Trello column (list) to fetch cards from."
    )
    args = parser.parse_args()
    main(args.column_id)
