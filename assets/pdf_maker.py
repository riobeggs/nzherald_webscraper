import re
from fpdf import FPDF


def make_pdf(article_title: str, article_text: str):
    """
    Creates a pdf file containing the chosen article.

    Returns the file name as a string
    """

    pdf = FPDF()
    pdf.add_font("TNR", "", r"assets/fonts/times new roman.ttf")
    pdf.set_margins(30,23,30)
    pdf.add_page()

    # create title
    pdf.set_font("TNR", size=28)
    pdf.multi_cell(150, 14, txt=article_title, align="L")

    # insert line break
    pdf.cell(150, 7, ln=2)

    # create text
    pdf.set_font("TNR", size=12)
    pdf.set_y(pdf.get_y())
    pdf.multi_cell(150, 8, txt=article_text, align="L")

    article_title = re.sub(r"[^a-zA-Z0-9]", "|", article_title)
    article_title = article_title.replace(" ", "")

    # save the pdf as article_title.pdf
    file = f"/Users/riobeggs/Documents/code/nzherald_webscraper/assets/articles/{article_title}.pdf"
    pdf.output(file)

    # returns the file name as a string
    return file