from datetime import date

import streamlit as st
import plotly.express as px

from proccess import get_medals_evolution, get_dataset, nb_sports_with_medals, sports_with_medals, get_ranking

st.set_page_config(layout="wide")
st.title("Olympics in data")
df = get_dataset()

# Global filters
with st.sidebar:
    st.subheader('Countries')
    if st.toggle("Every country"):
        countries = df['country'].unique().tolist()
    else:
        countries = st.multiselect(
            'Country-ies', df['country'].unique().tolist(),
            default=['France', 'Japan', 'United States']
        )
    st.markdown("---")

    # Sex
    st.subheader('Athletes')
    sex = st.radio("Sex", ["Men", "Women", "All"], index=2, horizontal=True)

    # Date
    st.markdown("---")
    st.subheader('Date')
    min_date, max_date = min(df['date'].unique().tolist()), max(df['date'].unique().tolist())
    date_ = st.date_input("",value=date( *[ int(elt) for elt in max_date.split("-")]), min_value=date( *[ int(elt) for elt in min_date.split("-")] ),
                          max_value=date( *[ int(elt) for elt in max_date.split("-")] ))
    date_ = str(date_).replace('/','-')

# ====== Ranking ======
with st.expander('Ranking'):
    st.table( get_ranking(df, date_).drop(['index'], axis=1) )


# ====== Medals evolution ======
with st.expander('Medals evolution'):
    l0, r0 = st.columns(2)

    # Total
    l1, r1 = st.columns(2)
    l1.subheader('Total medals')
    total_medals, idx = get_medals_evolution(df, sex.lower(), 'total', False)
    fig = px.line(total_medals[total_medals['country'].isin(countries)],
                  x="date", y=idx, color='country', markers=True)
    l1.plotly_chart(fig)

    # Gold
    r1.subheader('Gold medals')
    gold_medals, idx = get_medals_evolution(df, sex.lower(), 'gold', False)
    fig = px.line(gold_medals[gold_medals['country'].isin(countries)],
                  x="date", y=idx, color='country', markers=True)
    r1.plotly_chart(fig)


# ====== Sports =======

with st.expander("Sports"):

    # Most sports with medals
    l2, r2 = st.columns([70,30])
    l2.subheader('Most sports with medals')
    nb_sport_medals = nb_sports_with_medals(df)
    nb_sport_medals = nb_sport_medals[ nb_sport_medals['country'].isin(countries)]
    fig = px.histogram(nb_sport_medals, "country", "sports_with_medals")
    l2.plotly_chart(fig)

    # Sports with medals per country
    r2.subheader( 'Sports with medal per country')
    selected_country = r2.selectbox('Select a country', nb_sport_medals['country'].unique().tolist())
    sport_medals = sports_with_medals(df, selected_country)
    r2.dataframe( {"Sports": sport_medals}, height=200)
