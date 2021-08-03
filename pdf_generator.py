from filestack import Client
from fpdf import FPDF
import os
from dotenv import load_dotenv
import time

load_dotenv(override=True)


class PdfGenerator:

    def __init__(self, results, api_key=os.environ["FILESTACK_API_KEY"]):
        self.results = results
        self.api_key = api_key
        self.filename = f"cosing{time.strftime('%Y%m%d-%H%M%S')}.pdf"

    def create(self):
        pdf = FPDF("P", "mm", "A4")
        pdf.add_page("P")

        pdf.set_font("Courier", "B", 28)
        pdf.set_text_color(1, 9, 60)
        pdf.cell(0, 20, "Cosmetic Ingredients App", 0, align="C", ln=1)

        pdf.image("flask.png", w=14, h=16, )

        pdf.set_font("Courier", "B", 18)
        pdf.set_text_color(246, 162, 229)
        pdf.cell(0, 18, "Your search:\n", 0, align="L", ln=2)

        pdf.set_font("Arial", "", 14)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 8, self.results, 0, align="L")

        pdf.output(self.filename)

    def share(self):
        client = Client(self.api_key)
        link = client.upload(filepath=self.filename)
        return link.url
