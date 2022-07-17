import streamlit as st
import pandas as pd
from joblib import load
import os
from utils import load_data, select_data, recomendation

system_data = pd.read_csv('https://github.com/duartejr/wine_system_recomendation/blob/main/data/processed/wines_recomendation_system.csv?raw=true')
st.write(system_data.head())

#clf = load('https://github.com/duartejr/wine_system_recomendation/blob/main/app/classifier.joblib')
# st.title('WINER your personal sommelier.')
# data_load_state = st.text('Loading data...')
# data = load_data()
# data_load_state.text('Loading data...done!')

# sort_by = st.sidebar.radio("Sort wines by:",
#                            ('points', 'price'))
# order = st.sidebar.radio('Order:',
#                          ('descending', 'ascending'))

# styles = st.sidebar.multiselect('Select some style of wine.',
#                                data['style'].unique())
# countries = st.sidebar.multiselect('Select some contries.',
#                        data['country'].unique())
# points = st.sidebar.slider('Interval of avaliation.', 80, 100, (80, 100))
# min_price = st.sidebar.number_input('Minimum price:',
#                                     min_value = data.price.min(),
#                                     max_value = data.price.max())
# max_price = st.sidebar.number_input('Maximum price:',
#                                     min_value = min_price,
#                                     max_value = data.price.max(),
#                                     value = data.price.max())

# price = [min_price, max_price]

# if not styles:
#     styles = data['style'].unique()

# if not countries:
#     countries = data['country'].unique()
    
# st.text(points)

# st.subheader('We recomend these wines for you')

# selected_data = select_data(data, styles, countries, points, price, sort_by, order)

# st.table(selected_data.head(5))

# st.write('Chose a wine to see its description and more wine related with him.')
# wine_selected = st.selectbox('Chose a wine:', selected_data['title'].unique())
# st.table(recomendation(wine_selected, data)[['title', 'description', 'similarity (%)', 'style', 'variety', 'country', 'province', 'price', 'points']])