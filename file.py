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

pattern = r'(\d{2}\.\d{2}\.\d{2})\s+([\+\-])\s+([\d\s]+,\d+)\s+₸\s+([^\n]+)\n(\([^\)]+\))?\s*([^\n]+)?'

result = re.findall(pattern,data)

with open(os.path.expanduser('~/Desktop/docs/kaspi_output.csv'), 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date', 'Amount', 'Operation', 'Description', 'Currency Amount 1'])
    
    for row in result:
        date = row[0]
        operand = row[1]
        amount = row[2]
        description_parts = re.split(r'\s{3,}', row[3])
        operation = description_parts[0]
        description = description_parts[1] if len(description_parts) > 1 else ''
        currency_amount = row[4] if row[4] else ''
        
        writer.writerow([date, operand + amount, operation, description, currency_amount])