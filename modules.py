import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

__all__ = [
    'get_data', 'provide_people_vaccinated_once','get_categories','get_data_per_categories'
]

def get_data():

    """ 
    This module read the csv file at the github repository:

    https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/vaccinations.csv

    return: A DataFrame

    """

    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'

    return pd.read_csv(url)


def provide_people_vaccinated_once(data):

    """ 
    This module provide a new feature to data.

    The amount of people only vaccinated once.

    Return: A DataFrame
    
    """

    data['people_vaccinated_once'] = data['people_vaccinated']-data['people_fully_vaccinated']

    return data


def get_categories(data):

    """ This module get the categories at location
    
    Categories: Countries, Continents, Incomes and World

    Return: categories
    
    """

    values = data.location.unique().tolist()

    continents_vals = ['Africa','Asia','Europe', 'European Union','North America', 'Oceania','South America']
    income_vals = ['High income','Low income', 'Lower middle income', 'Upper middle income']
    world_val = ['World'] 
    excluded_vals = continents_vals+income_vals+world_val
    countries_vals = [value for value in values if value not in excluded_vals]

    return countries_vals, continents_vals, income_vals, world_val


def get_data_per_categories(data, categories):

    """ 
    This module returns the dataframes per categories
    
    """

    countries, continents, incomes, world = categories

    df_countries = data[data.location.isin(countries)]
    df_continents = data[data.location.isin(continents)]
    df_incomes = data[data.location.isin(incomes)]
    df_world = data[data.location.isin(world)]

    return df_countries, df_continents, df_incomes, df_world
    

# df_1 = pd.read_csv('iban.csv', names=['country','alpha-2','alpha-3','numeric'], header=0)

# df = get_data()
# df = provide_people_vaccinated_once(df)

# cats = get_categories(df)
# countries, conts, incs, world = get_data_per_categories(df,cats)


# maps = pd.Series(df_1['alpha-3'].values,index=df_1['country']).to_dict()
# print(maps)
# countries.loc[:,"iso_code"] = countries["location"].map(maps)
# print(countries)