<p align="center">
  <img src="https://i.imgur.com/2H10REK.png" width="200" alt="TrelloCardsToPDF" />
</p>

[python-version]: https://img.shields.io/badge/python-3.8%2B-blue
[python-url]: https://www.python.org/
[requests-version]: https://img.shields.io/badge/requests-2.26.0-green
[dotenv-version]: https://img.shields.io/badge/python--dotenv-0.20.0-orange
[markdown-pdf-version]: https://img.shields.io/badge/markdown--pdf-1.0.0-yellow

<p align="center">Automate Trello card retrieval and generate PDFs with Markdown content.</p>
<p align="center">
  <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python Version" /></a>
  <a href="https://pypi.org/project/requests/" target="_blank"><img src="https://img.shields.io/badge/requests-2.26.0-green" alt="Requests Version" /></a>
  <a href="https://pypi.org/project/python-dotenv/" target="_blank"><img src="https://img.shields.io/badge/python--dotenv-0.20.0-orange" alt="Dotenv Version" /></a>
  <a href="https://pypi.org/project/markdown-pdf/" target="_blank"><img src="https://img.shields.io/badge/markdown--pdf-1.0.0-yellow" alt="Markdown PDF Version" /></a>
</p>

## Description

This project retrieves Trello cards from a specified column (list) and generates PDF files with the Markdown content of each card’s description. The script is ideal for users seeking automated documentation generation for project tasks, ideas, or notes stored in Trello.

## Features

- **Trello Integration**: Fetch cards by specifying a Trello list ID.
- **Automated PDF Generation**: Converts card descriptions in Markdown to PDFs.
- **File Caching**: Saves card descriptions in a local cache to avoid duplicate processing.

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Trello API Key and Token](https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/) for authorization.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Set up a virtual environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   Ensure all required packages are installed by using `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your Trello API credentials:
   ```plaintext
   TRELLO_API_KEY=your_trello_api_key
   TRELLO_API_TOKEN=your_trello_api_token
   ```

## Usage

To use the script, specify the `column_id` as an argument:

```bash
python main.py <COLUMN_ID>
```

## Project Structure

```
.
├── .env                  # Environment variables
├── .cache/               # Directory to store cached markdown files
├── outputs/              # Directory to save generated PDF files
├── main.py               # Main script
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Testing

You can verify that the cache and output directories are created correctly and that PDF files are generated for each card in the specified column.
