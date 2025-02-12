import requests
from bs4 import BeautifulSoup
import pandas as pd

# URLs for searching mobiles and laptops on Flipkart
url_mobiles = 'https://www.flipkart.com/search?q=mobiles'
url_laptops = 'https://www.flipkart.com/search?q=laptops'

def get_flipkart_data(url, category):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    products = []
    for item in soup.find_all('div', class_='_1AtVbE'):
        name = item.find('div', class_='_4rR01T')
        price = item.find('div', class_='_30jeq3 _1_WHN1')
        rating = item.find('div', class_='_3LWZlK')

        if name and price:
            products.append({
                'Name': name.get_text(),
                'Price': price.get_text(),
                'Rating': rating.get_text() if rating else 'N/A',
                'Category': category
            })

    return products

# Example data for mobiles
mobiles_data = [
    {
        'Name': f'Samsung Galaxy Model {i} (Color {i % 5}, 64 GB)',
        'Price': f'₹{9499 + i * 50}',
        'Rating': f'{4.0 + (i % 5) * 0.1:.1f}',
        'Category': 'Mobile'
    } for i in range(1, 26)
]

# Example data for laptops
laptops_data = [
    {
        'Name': f'HP Pavilion Gaming Model {i} Ryzen 5 Quad Core {i}',
        'Price': f'₹{57990 + i * 100}',
        'Rating': f'{4.0 + (i % 5) * 0.1:.1f}',
        'Category': 'Laptop'
    } for i in range(1, 26)
]

# Optionally fetch data from Flipkart
# mobiles_data = get_flipkart_data(url_mobiles, 'Mobile')
# laptops_data = get_flipkart_data(url_laptops, 'Laptop')

# Create DataFrames from example data
df_mobiles = pd.DataFrame(mobiles_data)
df_laptops = pd.DataFrame(laptops_data)

# Save DataFrames to an Excel file
with pd.ExcelWriter('flipkart_data_example.xlsx') as writer:
    df_mobiles.to_excel(writer, sheet_name='Mobiles', index=False)
    df_laptops.to_excel(writer, sheet_name='Laptops', index=False)

print('Data saved to flipkart_data_example.xlsx')
