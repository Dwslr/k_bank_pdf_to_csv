import PyPDF2
import re
import os


pdf_file = open(os.path.expanduser('~/Desktop/docs/kaspi_statement_23.03.30.pdf'), 'rb')
reader = PyPDF2.PdfReader(pdf_file)

data = ''

for page in range(len(reader.pages)):
    page_obj = reader.pages[page]
    data += page_obj.extract_text()

pattern = r'(\d{2}\.\d{2}\.\d{2})\s+([\+\-])\s+([\d\s]+,\d+)\s+₸\s+([^\n]+)\n(\([^\)]+\))?\s*([^\n]+)?'

result = re.findall(pattern,data)

for row in result:
    date = row[0]
    operation = row[1]
    amount = row[2]
    description = row[3]
    currency_amount = row[4] if row[4] else ''
    note = row[5] if row[5] else ''

    print(f'{date} | {amount} | {operation} | {description} | {currency_amount} | {note}')