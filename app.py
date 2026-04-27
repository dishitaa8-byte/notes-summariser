from flask import Flask, render_template, request
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import PyPDF2
from dotenv import load_dotenv
import os
import nltk


app = Flask(__name__)
load_dotenv()

# Optional API key from .env for future integrations.
API_KEY = os.getenv("API_KEY", "")


def get_local_nltk_data_dir():
    return os.path.join(app.root_path, "nltk_data")


def ensure_nltk_tokenizers():
    """
    Ensure NLTK tokenizers required by sumy are available.
    """
    local_nltk_dir = get_local_nltk_data_dir()
    os.makedirs(local_nltk_dir, exist_ok=True)
    if local_nltk_dir not in nltk.data.path:
        nltk.data.path.insert(0, local_nltk_dir)

    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
    ]
    for resource_path, resource_name in resources:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(resource_name, download_dir=local_nltk_dir, quiet=True)


def summarize_text(text):
    ensure_nltk_tokenizers()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, 3)
    return " ".join([str(sentence) for sentence in summary])


def read_txt_from_upload(file_storage):
    return file_storage.read().decode("utf-8", errors="ignore")


def read_pdf_from_upload(file_storage):
    text = ""
    file_storage.stream.seek(0)
    reader = PyPDF2.PdfReader(file_storage)
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text
    return text


@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    error = ""
    input_text = ""

    if request.method == "POST":
        input_text = (request.form.get("text_input") or "").strip()
        uploaded_file = request.files.get("file_input")

        text_to_summarize = ""

        if input_text:
            text_to_summarize = input_text
        elif uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename.lower()
            try:
                if filename.endswith(".txt"):
                    text_to_summarize = read_txt_from_upload(uploaded_file)
                elif filename.endswith(".pdf"):
                    text_to_summarize = read_pdf_from_upload(uploaded_file)
                else:
                    error = "Unsupported file type. Please upload a .txt or .pdf file."
            except Exception as exc:
                app.logger.exception("File parsing failed: %s", exc)
                error = "Unable to read the uploaded file. Please check file content and try again."
        else:
            error = "Please enter text or upload a file."

        if text_to_summarize and not error:
            try:
                summary = summarize_text(text_to_summarize)
                if not summary.strip():
                    error = "Could not generate summary. Please provide more readable content."
            except Exception as exc:
                app.logger.exception("Summarization failed: %s", exc)
                error = "Unable to process this content right now. Please try another text/file."

    return render_template("index.html", summary=summary, error=error, input_text=input_text)


if __name__ == "__main__":
    app.run(debug=True)
