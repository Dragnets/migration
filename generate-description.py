import pandas as pd
from bs4 import BeautifulSoup

# Load the Excel file
file_path = 'internal_all.xlsx'
df = pd.read_excel(file_path)

# Extract columns that start with 'Description'
description_columns = [col for col in df.columns if col.startswith('Description')]

# Define the phrases to disregard
disregard_phrases = [
    'Collection Address',
    '12 Months Warranty',
    'Delivery & Installation'
]

# Function to filter, combine description cells with commas, and remove HTML tags
def filter_and_combine(row):
    combined_text = []
    for col in description_columns:
        cell = row[col]
        if isinstance(cell, str) and not any(phrase in cell for phrase in disregard_phrases):
            # Remove HTML tags
            cell = BeautifulSoup(cell, "html.parser").get_text()
            combined_text.append(cell)
    return ', '.join(combined_text)

# Apply the function to each row
df['Combined_Description'] = df.apply(filter_and_combine, axis=1)

# Save the result to a new Excel file
output_file_path = 'combined_descriptions_with_commas.xlsx'
df.to_excel(output_file_path, index=False)

# Inform the user
print(f"Combined descriptions saved to {output_file_path}")
