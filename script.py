import argparse
import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from markdown_pdf import MarkdownPdf, Section
from PyPDF2 import PdfMerger

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


def merge_pdfs(files, output):
    merger = PdfMerger()
    for file in files:
        merger.append(file)
    # Save the merged PDF
    merger.write(output)
    merger.close()
    print(f"Merged file saved as: {output}")


def markdown_to_pdf(title, markdown_string):
    pdf = MarkdownPdf()
    pdf.add_section(Section(markdown_string))
    if not os.path.exists("./outputs"):
        os.makedirs("./outputs")
    pdf.save("./outputs/" + title + ".pdf")


def rename_files_by_name(directory):
    # Listar archivos en el directory
    archivos = os.listdir(directory)

    # Extraer la fecha del nombre del archivo y ordenarlos
    archivos_con_fechas = []
    for archivo in archivos:
        # Filtrar solo los archivos
        ruta_completa = os.path.join(directory, archivo)
        if os.path.isfile(ruta_completa):
            try:
                # Extraer la fecha del nombre
                partes = archivo.split(" ")
                fecha_str = " ".join(partes[-3:])  # Ejemplo: "Dec 13, 2024"
                fecha_str = fecha_str.replace(".pdf", "")
                fecha = datetime.strptime(fecha_str, "%b %d, %Y")
                archivos_con_fechas.append((archivo, fecha))
            except ValueError:
                print(f"No se pudo procesar la fecha en: {archivo}")

    # Ordenar los archivos por la fecha extraída
    archivos_ordenados = sorted(archivos_con_fechas, key=lambda x: x[1])

    # Renombrar archivos con el prefijo basado en el orden
    for indice, (archivo, _) in enumerate(archivos_ordenados, start=1):
        nuevo_nombre = f"{indice:02d}. {archivo}"
        ruta_actual = os.path.join(directory, archivo)
        nueva_ruta = os.path.join(directory, nuevo_nombre)
        os.rename(ruta_actual, nueva_ruta)


def main(column_id):
    cards = obtain_cards_by_column(column_id)
    if cards:
        cards_title_description = obtain_cards_title_description(cards)
        for title, description in cards_title_description.items():
            if not check_output(title):
                markdown_to_pdf(title, description)
        rename_files_by_name("./outputs")
        merge_pdfs(
            [f"./outputs/{file}" for file in os.listdir("./outputs")],
            "./outputs/00.all_planesdiarios.pdf",
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch Trello cards and generate PDFs."
    )
    parser.add_argument(
        "column_id", help="The ID of the Trello column (list) to fetch cards from."
    )
    args = parser.parse_args()
    main(args.column_id)
