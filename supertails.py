import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to scrape product data from Supertails.com
def scrape_product_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Select product elements using appropriate CSS selectors
    product_elements = soup.select('div.findify-components--cards--product__content')

    # Extract product names from each product element
    product_names = []
    for product_element in product_elements:
        product_name_tag = product_element.select_one('h2.findify-components--text.findify-components--cards--product__title')
        if product_name_tag:
            product_name = product_name_tag.text.strip()
            product_names.append(product_name)

    return product_names

# Streamlit app configuration
st.set_page_config(
    page_title="Supertails Product Scraper",
    page_icon="🐾",
    layout="wide"
)

# Streamlit app content
st.title('Supertails Product Scraper')

# Input field for entering search query
search_query = st.text_input('Enter product name to search:', 'Pedigree')

# Button to trigger scraping
if st.button('Search'):
    # Construct URL based on search query
    url = f'https://supertails.com/search?q={search_query}&page=1'

    # Call scraper function to get product names
    product_names = scrape_product_data(url)

    # Display the scraped product names
    if product_names:
        st.header('Scraped Product Names:')
        for idx, product_name in enumerate(product_names[:10], start=1):
            st.write(f"{idx}. {product_name}")
    else:
        st.write('No products found.')

    st.success('Scraping complete!')

# Display footer or additional information
st.markdown("---")
st.write("This is a basic Streamlit app to scrape product names from Supertails.com.")

