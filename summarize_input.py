from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import PyPDF2


def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, 3)
    return " ".join([str(sentence) for sentence in summary])


def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


choice = input("Enter 1 for text or 2 for file: ")

if choice == "1":
    text = input("Enter your text:\n")

elif choice == "2":
    path = input("Enter file path: ")

    if path.endswith(".txt"):
        text = read_txt(path)
    elif path.endswith(".pdf"):
        text = read_pdf(path)
    else:
        print("Unsupported file type")
        exit()
else:
    print("Invalid choice")
    exit()

summary = summarize_text(text)

print("\nSummary:\n")
print(summary)
