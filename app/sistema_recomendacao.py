import streamlit as st
import pandas as pd
#from utils import load_data, select_data, recomendation
import numpy as np
from joblib import load

clf = load('classifier.joblib') 
vetorizador = load('vectorizer.joblib')
system_data = pd.read_csv('../data/processed/wines_recomendation_system.csv')

@st.cache
def load_data():
    data = pd.read_csv(f'../data/processed/wines_user_consult.csv')
    data = data.drop_duplicates()
    return data

@st.cache
def select_data(data, styles, countries, points, price, sort_by, order):
    data = data[data['style'].isin(styles)]
    data = data[data['country'].isin(countries)]
    data = data[data['points'].between(points[0], points[1])]
    data = data[data['price'].between(price[0], price[1])]
    
    if order == 'ascending':
        order = True
    else:
        order = False
    data = data.sort_values(by=sort_by, ascending=order)
    return data[['title', 'variety', 'style', 'winery', 'province', 'country', 'points', 'price']]

#%%
def recomendation(wine, user_data):
    test = system_data.query(f"title == '{wine}'")
    user_count_vec = vetorizador.transform(test.description)
    NNs_clf = clf.kneighbors(user_count_vec, return_distance=True)
    answer = user_data.loc[NNs_clf[1][0, :]]
    answer['similarity (%)'] = np.round(100 * (1 - NNs_clf[0][0, :]), 2)
    return answer


st.title('WINER your personal sommelier.')
data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('Loading data...done!')

sort_by = st.sidebar.radio("Sort wines by:",
                           ('points', 'price'))
order = st.sidebar.radio('Order:',
                         ('descending', 'ascending'))

styles = st.sidebar.multiselect('Select some style of wine.',
                               data['style'].unique())
countries = st.sidebar.multiselect('Select some contries.',
                       data['country'].unique())
points = st.sidebar.slider('Interval of avaliation.', 80, 100, (80, 100))
min_price = st.sidebar.number_input('Minimum price:',
                                    min_value = data.price.min(),
                                    max_value = data.price.max())
max_price = st.sidebar.number_input('Maximum price:',
                                    min_value = min_price,
                                    max_value = data.price.max(),
                                    value = data.price.max())

price = [min_price, max_price]

if not styles:
    styles = data['style'].unique()

if not countries:
    countries = data['country'].unique()
    
st.text(points)

st.subheader('We recomend these wines for you')

selected_data = select_data(data, styles, countries, points, price, sort_by, order)

st.table(selected_data.head(5))

st.write('Chose a wine to see its description and more wine related with him.')
wine_selected = st.selectbox('Chose a wine:', selected_data['title'].unique())
st.table(recomendation(wine_selected, data)[['title', 'description', 'similarity (%)', 'style', 'variety', 'country', 'province', 'price', 'points']])