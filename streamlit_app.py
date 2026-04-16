import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests  

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

cnx = st.connection("snowflake")
session = cnx.session()

st.title("Smoothies")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

fruit_options = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")

ingredients_list = st.multiselect("Ingredients:", fruit_options)

if ingredients_list:
    ingredient_string = " ".join(str(fr) for fr in ingredients_list)

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    if st.button("OK"):
        session.sql(
            "INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (?, ?)",
            params=[ingredient_string, name_on_order]
        ).collect()
        st.success("Your Smoothie is ordered, " + name_on_order + "!", icon="✅")
