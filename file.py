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

    # Write the header row
    writer.writerow(['line', 'date', 'amount', 'operation', 'note', 'amount2', 'currency'])

    for line in lines:
        if line.strip() and ' ' in line:
           # Extract the date using the split() method
            date = line.split()[0]

            # Use a regular expression to extract the amount
            match = re.search(r'([+-].+₸)', line)
            amount = match.group(1) if match else ''
            # Delete spaces, change , sign to . sign, delete the tenge symbol, and delete the + operand
            amount = amount.replace(' ', '').replace(',', '.').replace('₸', '').replace('+', '')
            
            # Use a regular expression to extract the operation
            match = re.search(r'\S+\s+\S+\s{2,}(\S+)', line)
            operation = match.group(1) if match else ''
            
            # Use a regular expression to extract the note
            match = re.search(r'\S+\s+\S+\s{2,}\S+\s{3,}(.+)', line)
            note = match.group(1) if match else ''
            
            # Use a regular expression to extract the currency
            match = re.search(r'\((.+?)\)', line)
            currency = match.group(1) if match else ''
            # Check if the currency value is empty
            if currency:
                # Split the currency value by space
                amount2, currency = currency.split()
            else:
                amount2 = ''
                currency = ''

            # Write the data to the CSV file
            writer.writerow([line, date, amount, operation, note, amount2, currency])
        else:
            writer.writerow([line])