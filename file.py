import PyPDF2
import re
import os
import csv

pdf_file = open(os.path.expanduser('~/Desktop/docs/kaspi_statement_23.03.30.pdf'), 'rb')
reader = PyPDF2.PdfReader(pdf_file)

data = ''

for page in range(len(reader.pages)):
    page_obj = reader.pages[page]
    data += page_obj.extract_text()

# Find the data in pdf after the line "Дата Сумма Операция Детали"
match = re.search(r'Дата Сумма Операция\s+Детали\s+(.+)', data, re.DOTALL)
data_after_header = match.group(1) if match else ''

# Divide text to rows by date
lines = re.split(r'(?=\d{2}\.\d{2}\.\d{2})', data_after_header)


with open(os.path.expanduser('~/Desktop/docs/kaspi_output.csv'), 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    for line in lines:
        writer.writerow([line])