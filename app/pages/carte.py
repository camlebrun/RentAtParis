import streamlit as st
from model.data_prep import SelectData

st.set_page_config(layout="wide")

st.title("Quartier à Paris")

select_data = SelectData()
fig = select_data.with_maps()
st.plotly_chart(fig, use_container_width=True)
