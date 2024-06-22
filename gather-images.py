import pandas as pd

# Function to remove domain if present
def remove_domain(url, domain):
    if url.startswith(domain):
        return url[len(domain):]
    return url

# Load the Excel file
file_path = 'internal_all.xlsx'
df = pd.read_excel(file_path)

# Define the domain to remove
domain = 'https://rethinkyouroffice.co.uk'

# Extract columns that start with 'Alternative photo' and 'Main image 1'
image_columns = ['Main image 1'] + [col for col in df.columns if col.startswith('Alternative photo')]

# Apply the domain removal and create the 'All Images' column
df['All Images'] = df[image_columns].apply(lambda row: ', '.join(remove_domain(url, domain) for url in row.dropna().astype(str)), axis=1)

# Save the updated dataframe to a new Excel file
output_file_path = 'updated_internal_all.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Updated file saved to {output_file_path}")
