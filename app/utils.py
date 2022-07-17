#%%
import os
import numpy as np
import pandas as pd
import streamlit as st
from joblib import load

cwd = os.getcwd() # The current work directory
classifier = load(f'{cwd}/app/classifier.joblib') # git
#classifier = load(f'{cwd}/classifier.joblib') # local
vectorizer = load(f'{cwd}/app/vectorizer.joblib') # git
#vectorizer = load(f'{cwd}/vectorizer.joblib') # local

system_data = pd.read_csv('https://raw.githubusercontent.com/duartejr/wine_system_recomendation/main/data/processed/wines_recomendation_system.csv')

@st.cache
def load_data():
    """Load and returns the data

    Returns:
        pd.DataFrame: The data loaded
    """
    data = pd.read_csv(f'https://raw.githubusercontent.com/duartejr/wine_system_recomendation/main/data/processed/wines_user_consult.csv')
    data = data.drop_duplicates()
    return data

@st.cache
def select_data(data, styles, countries, points, price, sort_by, order):
    """Select data according with the filters passed.

    Args:
        data (pd.DataFrame): Dataframe with the wines data.
        styles (list): List of strings with the wine styles to filter the data.
        countries (list): List of strings with the countries names to filter the data.
        points (list): List of floats containing a range of points to filter the data.
        price (list): List of floats containing a range of prices to filter the data.
        sort_by (string): String ("points" or "price") of the criterion to sort the data.
        order (string): String ("ascending" or "descending") of the criterion to order the data.
        
    Returns:
        data: Dataframe with the filtered data.
    """
    data = data[data['style'].isin(styles)]
    data = data[data['country'].isin(countries)]
    data = data[data['points'].between(points[0], points[1])]
    data = data[data['price'].between(price[0], price[1])]
    
    if order == 'ascending':
        order = True
    else:
        order = False
    
    data = data.sort_values(by=sort_by, ascending=order)
    
    return data[['title', 'variety', 'style', 'winery', 'province', 'country', 
                 'points', 'price']]

@st.cache
def recomendation(wine, user_data):
    """Algorithm responsible to redomends wines that are similar with the one informed.

    Args:
        wine (string): Title of the wine which will be used as references to recomend another wines.
        user_data (dataframe): A dataframe with the data which will be shown for the user.

    Returns:
        dataframe: A daframe with the wines more related with the informed wine considering the description.
    """
    test = system_data.query(f"title == '{wine}'")
    user_count_vec = vectorizer.transform(test.description)
    NNs_clf = classifier.kneighbors(user_count_vec, return_distance=True)
    answer = user_data.loc[NNs_clf[1][0, :]]
    answer['similarity (%)'] = np.round(100 * (1 - NNs_clf[0][0, :]), 2)
    return answer
