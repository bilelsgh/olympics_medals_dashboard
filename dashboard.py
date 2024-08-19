import streamlit as st
import plotly.express as px

from proccess import get_medals_evolution, get_dataset, nb_sports_with_medals, sports_with_medals

st.set_page_config(layout="wide")
st.title("Olympics in data")
df = get_dataset()

# Global filters
st.markdown("#")
global_filter = st.toggle('Global filter')
if global_filter:
    l0, r0 = st.columns(2)

    global_country = l0.multiselect(
        'Country-ies', df['country'].unique().tolist(),
        default=['France', 'Japan', 'United States']
    )
    global_sex = r0.radio("Athletes", ["Men", "Women", "All"], index=2, horizontal=True)
    st.markdown("#")

# ====== Medals evolution ======
with st.expander('Medals evolution'):
    l0, r0 = st.columns(2)

    countries = l0.multiselect(
        'Country-ies', df['country'].unique().tolist(),
        default=['France', 'Japan', 'United States']
    ) if not global_filter else global_country

    sex = r0.radio("Athletes", ["Men", "Women", "All"], index=2, horizontal=True) if not global_filter \
        else global_sex
    st.markdown("---")

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

    l2, r2 = st.columns(2)
    l2.subheader('Most sports with medals')
    nb_sport_medals = nb_sports_with_medals(df)
    nb_sport_medals = nb_sport_medals if not global_filter else nb_sport_medals[ nb_sport_medals['country'].isin(global_country)]
    fig = px.histogram(nb_sport_medals, "country", "sports_with_medals")
    l2.plotly_chart(fig)

    r2.subheader( 'Sports with medal per country')
    selected_country = r2.selectbox('Select a country', nb_sport_medals['country'].unique().tolist())
    sport_medals = sports_with_medals(df, selected_country)
    r2.dataframe(sport_medals)
