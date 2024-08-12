import streamlit as st
import plotly.express as px

from proccess import get_medals_evolution, get_dataset

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
