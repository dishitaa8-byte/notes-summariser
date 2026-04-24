# Notes Summariser (Flask)

This project converts your CLI notes summarizer into a Flask web app while keeping the same core logic:
- `sumy` TextRank summarization
- TXT/PDF reading (with `PyPDF2`)

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Configure environment values:

- Edit `.env`
- Add your API key value to `API_KEY` (kept for future integrations)

3. Run the app:

```bash
python app.py
```

4. Open in browser:

`http://127.0.0.1:5000`

## Features

- Paste notes in a text box
- Upload `.txt` or `.pdf` file
- Click **Summarize**
- View summary on the same page
