import streamlit as st
from utils import load_data, select_data, recomendation

# -- Loading the data ----------------------------------------------
data = load_data()
# ------------------------------------------------------------------

# -- Sidebar -------------------------------------------------------
# Buttons to select the selection criteria
sort_by = st.sidebar.radio("Sort wines by:",
                           ('points', 'price'))

# Buttons how the data will be ordered whe is showed in the main page
order = st.sidebar.radio('Order:',
                         ('descending', 'ascending'))

# Box to select a list of styles to filter the data
styles = st.sidebar.multiselect('Select some style of wine.',
                                sorted(data['style'].unique()))

# Box to select a list of countries to filter the data
countries = st.sidebar.multiselect('Select some contries.',
                                   sorted(data['country'].unique()))

# Slider to select the points range to filter the data
points = st.sidebar.slider('Interval of avaliation.', 80, 100, (80, 100))

# Box to define the minimum wine value to filter the data
min_price = st.sidebar.number_input('Minimum price:',
                                    min_value = data.price.min(),
                                    max_value = data.price.max(),
                                    value = data.price.min())

# Box to define the maximum vale to filter the data
max_price = st.sidebar.number_input('Maximum price:',
                                    min_value = min_price,
                                    max_value = data.price.max(),
                                    value = data.price.max())
# ----------------------------------------------------------------

# -- Main page --------------------------------------------------- 
st.title('WINER your personal sommelier.') # Main page title

# Set styles in the case when nothing is selected in the sidebar
if not styles:
    styles = data['style'].unique()

# set countries in the when nothing is selected in the sidebar
if not countries:
    countries = data['country'].unique()
    
price_interval = [min_price, max_price]

# Main table where are showed the top 5 wines considering the marked filters in the sidebar
selected_data = select_data(data, styles, countries, points, price_interval, 
                            sort_by, order) # data showed in the main table
st.table(selected_data.head(5)) # Shows the table

# -- Recomeded wines --
st.subheader('We recomend these wines for you')
st.write('Chose a wine to see its description and more wine related with him.')

# wine that will be used as the input for the recomendation system
wine_selected = st.selectbox('Chose a wine:', selected_data['title'].head(5)) 

# Table with the wines more related with the wine_selected
st.table(recomendation(wine_selected, data)[['title', 'description', 'similarity (%)', 
                                             'style', 'variety', 'country', 'province', 
                                             'price', 'points']])