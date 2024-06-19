import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup

def search_medicine_1mg(medicine_name):
    url = f'https://www.1mg.com/search/all?name={medicine_name}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup_obj = soup(response.content, 'html.parser')
            products = soup_obj.find_all('div', class_='style__horizontal-card___1Zwmt')

            product_name = []
            pack_size = []
            product_price = []
            product_link = []

            for product in products:
                name_tag = product.find('div', class_='style__product-description___1vPQe')
                if name_tag:
                    product_name.append(name_tag.find('span', class_='style__pro-title___3zxNC').text.strip())

                pack_tag = product.find('div', class_='style__pack-size___254Cd')
                if pack_tag:
                    pack_size.append(pack_tag.text.strip())

                price_tag = product.find('div', class_='style__price-tag___B2csA')
                if price_tag:
                    price_text = price_tag.text.strip().replace('₹', '').replace('MRP', '').strip()
                    product_price.append(format(float(price_text), '.2f'))

                link_tag = product.find('a', href=True)
                if link_tag:
                    product_link.append('https://www.1mg.com' + link_tag['href'])

            df = pd.DataFrame({
                'Product name': product_name,
                'Package size': pack_size,
                'Price': product_price,
                'Link': product_link
            })

            return df

        else:
            st.error(f'Failed to retrieve data from 1mg. Status code: {response.status_code}')
            return None
    
    except Exception as e:
        st.error(f'Error occurred: {e}')
        return None

def main():
    st.title('Medicine Finder')

    # Input field for medicine name
    medicine_name = st.text_input('Enter the name of the medicine:')

    if st.button('Search'):
        # Call the scraper function
        results_df = search_medicine_1mg(medicine_name)

        # Display results
        if results_df is not None and not results_df.empty:
            st.dataframe(results_df)
        elif results_df is not None:
            st.write("No results found")
            
if __name__ == '__main__':
    main()
