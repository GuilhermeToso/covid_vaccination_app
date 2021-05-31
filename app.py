import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import modules as mod
import pycountry

st.set_page_config(layout="wide")

def title():

    value = "COVID-19 Worldwide Vaccination Progress"

    return st.title(value)

def plot_pie_chart(data, dosage, limit):

    fully_vaccinated, once_vaccinated = data[0], data[1]

    if limit == 'Higher':

        if dosage == '2-Dose':

            graph = px.pie(
                fully_vaccinated, fully_vaccinated.iloc[:5,:].index,fully_vaccinated.iloc[:5,:].people_fully_vaccinated,
                labels={'label':'Country','value':'People'}
            )
            graph.update_layout(
                title="5 highest countries with people fully vaccinated"
            )
            st.plotly_chart(graph)
        elif dosage=='1-Dose':
            graph = px.pie(
                once_vaccinated, once_vaccinated.iloc[:5,:].index,once_vaccinated.iloc[:5,:].people_vaccinated_once,
                labels={'label':'Country','value':'People'}
            )
            graph.update_layout(
                title="5 highest countries with people vaccinated once"
            )
            st.plotly_chart(graph)
    elif limit == 'Lower':

        if dosage == '2-Dose':

            graph = px.pie(
                fully_vaccinated, fully_vaccinated.iloc[-5:,:].index,fully_vaccinated.iloc[-5:,:].people_fully_vaccinated,
                labels={'label':'Country','value':'People'}
            )
            graph.update_layout(
                title="5 lowest countries with people fully vaccinated"
            )
            st.plotly_chart(graph)
        elif dosage=='1-Dose':
            graph = px.pie(
                once_vaccinated, once_vaccinated.iloc[-5:,:].index,once_vaccinated.iloc[-5:,:].people_vaccinated_once,
                labels={'label':'Country','value':'People'}
            )
            graph.update_layout(
                title="5 lowest countries with people vaccinated once"
            )
            st.plotly_chart(graph)

def vaccinations_limits(countries_data):

    loc_group = countries_data.groupby(['location']).max()

    fully_vaccinated = loc_group.sort_values(by='people_fully_vaccinated', ascending=False).people_fully_vaccinated.dropna().to_frame()
    once_vaccinated = loc_group.sort_values(by='people_vaccinated_once', ascending=False).people_vaccinated_once.dropna().to_frame()

    st.sidebar.warning('**Highest/lowest Vaccinated Countries**')
    vaccinated = ['2-Dose','1-Dose']
    dosage = st.sidebar.radio('Vaccination',vaccinated,key='radio_1')
    limit = st.sidebar.selectbox('Select the limit option', ['Higher', 'Lower'])
    plot_pie_chart([fully_vaccinated,once_vaccinated], dosage, limit)

def first_column(world_data):

    fully_vaccinated = world_data[world_data.people_fully_vaccinated.notnull()].people_fully_vaccinated.iloc[-1]
    once_vaccinated =  world_data[world_data.people_vaccinated_once.notnull()].people_vaccinated_once.iloc[-1]
  
    st.markdown("**Worldwide Vaccination**")
    st.warning(f'Fully Vaccinated: {format(fully_vaccinated, ",")}')
    st.warning(f'Once Vaccinated: {format(once_vaccinated, ",")}')


def plot_line(countries_data, dosage, countries):

    df_countries = countries_data

    if dosage=='2-Dose':

        fig = go.Figure()

        for i in range(len(countries)):

            df_country = df_countries[df_countries.location==countries[i]].dropna()

            fig.add_trace(
                go.Scatter(
                    x=df_country.date,
                    y=df_country.people_fully_vaccinated,
                    mode='lines+markers',
                )
            )
        
        fig.update_layout(
            xaxis={'title':'Date'},
            yaxis={'title':'Countries'},
            title=f"People of {dosage} vaccinated per date",
            width=1280, height=500
        )

        st.plotly_chart(fig)

    elif dosage=='1-Dosage':

        fig = go.Figure()

        for i in range(len(countries)):

            df_country = df_countries[df_countries.location==countries[i]].dropna()

            fig.add_trace(
                go.Scatter(
                    x=df_country.date,
                    y=df_country.people_vaccinated_once,
                    mode='lines+markers',
                )
            )
        
        fig.update_layout(
            xaxis={'title':'Date'},
            yaxis={'title':'Countries'},
            title=f"People of {dosage} vaccinated per date",
            width=1280, height=500
        )

        st.plotly_chart(fig)


def second_column(countries_data):

    countries_list = countries_data.location.unique().tolist()

    st.sidebar.warning('**Vaccinated Countries per Date**')
    vaccinated = ['2-Dose','1-Dose']
    dosage2 = st.sidebar.radio('Vaccination',vaccinated,key='radio_2')
    countries = st.sidebar.multiselect('Select the country(ies)', countries_list, default='Albania')
    plot_line(countries_data, dosage2, countries)

def plot_bars(df_conts, df_inc, dosage, option):

    df_continents = df_conts.groupby(['location'])
    df_income = df_inc.groupby(['location'])
    
    if dosage == '2-Dose':
        
        if option == 'Continents':

            df = df_continents.max()
            df = df.sort_values(by='people_fully_vaccinated', ascending=False).people_fully_vaccinated.dropna().to_frame()
            
            plot = px.bar(df, df.index, 'people_fully_vaccinated', height=700)
            plot.update_layout(
                xaxis={'title':'Continents'},
                yaxis={'title':'Fully Vaccinated'},
                title=f"People of {dosage} vaccinated per {option}"
            )
            st.plotly_chart(plot)
        elif option == 'Income':

            df = df_income.max()
            df = df.sort_values(by='people_fully_vaccinated', ascending=False).people_fully_vaccinated.dropna().to_frame()
            plot = px.bar(df, df.index, 'people_fully_vaccinated', height=700)
            plot.update_layout(
                xaxis={'title':'Income'},
                yaxis={'title':'Fully Vaccinated'},
                title=f"People of {dosage} vaccinated per {option}"
            )
            st.plotly_chart(plot)

    elif dosage == '1-Dose':

        if option == 'Continents':

            df = df_continents.max()
            df = df.sort_values(by='people_vaccinated_once', ascending=False).people_vaccinated_once.dropna().to_frame()
            
            plot = px.bar(df, df.index, 'people_vaccinated_once', height=700)
            plot.update_layout(
                xaxis={'title':'Continents'},
                yaxis={'title':'Vaccinated Once'},
                title=f"People of {dosage} vaccinated per {option}")
            st.plotly_chart(plot)
        elif option == 'Income':

            df = df_income.max()
            df = df.sort_values(by='people_vaccinated_once', ascending=False).people_vaccinated_once.dropna().to_frame()
            
            plot = px.bar(df, df.index, 'people_vaccinated_once', height=700)
            plot.update_layout(
                xaxis={'title':'Continents'},
                yaxis={'title':'Vaccinated Once'},
                title=f"People of {dosage} vaccinated per {option}")
            st.plotly_chart(plot)

def third_column(continents_data, income_data):

    st.sidebar.warning("Income or Continents")
    vaccinated = ['2-Dose','1-Dose']
    dosage = st.sidebar.radio('Vaccination',vaccinated,key='radio_3')
    option = st.sidebar.selectbox("Select the option",['Continents','Income'])
    plot_bars(continents_data, income_data, dosage, option)

def plot_map(df_countries, dosage):

    df = df_countries

    if dosage=='2-Dose':

        df = df.dropna(subset=['people_fully_vaccinated'])
        
        fig = px.scatter_geo(df, locations="iso_code", color="location", size="people_fully_vaccinated",
                animation_frame='date',color_discrete_sequence=px.colors.qualitative.Dark24,
                projection="natural earth",width=1200, height=600)
        fig.update_geos(
            showcountries=True, countrycolor="Black",
            showocean=True, oceancolor="LightBlue",
            showland=True, landcolor="LightGreen",
        )
        st.plotly_chart(fig)

    elif dosage=='1-Dose':

        df = df.dropna(subset=['people_vaccinated_once'])
        fig = px.scatter_geo(df, locations="iso_code", color="location", size="people_fully_vaccinated",
                animation_frame='date',color_discrete_sequence=px.colors.qualitative.Dark24,
                projection="natural earth",width=1200, height=600)
        fig.update_geos(
            showcountries=True, countrycolor="Black",
            showocean=True, oceancolor="LightBlue",
            showland=True, landcolor="LightGreen",
        )
        st.plotly_chart(fig)


def fourth_column(countries_data):

    st.sidebar.warning("Map of Vaccinated")
    vaccinated = ['2-Dose','1-Dose']
    dosage = st.sidebar.radio('Vaccination',vaccinated,key='radio_4')
    plot_map(countries_data, dosage)
    
    
def app():

    df = mod.get_data()
    df = mod.provide_people_vaccinated_once(df)

    categories = mod.get_categories(df)
    dataframes = mod.get_data_per_categories(df,categories)

    df_countries, df_conts, df_inc, df_world = dataframes

    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3
    df_countries.loc[:,"iso_code"] = df_countries["location"].map(countries)

    df_countries = df_countries[df_countries.location != 'England']
    df_countries = df_countries[df_countries.location != 'Northern Ireland']
    df_countries = df_countries[df_countries.location != 'Scotland']

    truth_vals = {'Bolivia':'BQL', 'Bonaire Sint Eustatius and Saba':'BES',
             'British Virgin Islands':'VGB', 'Brunei':'BRN', 'Cape Verde':'CPV',
              'Curacao':'CUW', 'Faeroe Islands':'FRO','Falkland Islands':'FLK','Iran':'IRN',
              'Laos':'LAO','Moldova':'MDA','Northern Cyprus':'CYP',
              'Palestine':'PSE','Russia':'RUS','Saint Helena':'SHN','South Korea':'KOR',
              'Timor':'TLS','Vietnam':'VNM','Wales':'WLF',"Cote d'Ivoire":'CIV',
       'Democratic Republic of Congo':'COD', 'Kosovo':'XKX', 'Syria':'SYR', 'Taiwan':'TWN',
       'Venezuela':'VEN'
             }

    for key, val in truth_vals.items():
        inds = df_countries[df_countries.location==key].index
        df_countries.loc[inds,'iso_code'] = val

    # Title
    title()

    col_1, col_2 = st.beta_columns(2)

    with col_1:
        first_column(df_world)
        vaccinations_limits(df_countries)

    with col_2:
        third_column(df_conts, df_inc)

  
    second_column(df_countries)
    fourth_column(df_countries)
       
if __name__=='__main__':
    app = app()