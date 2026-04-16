import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

st.title("Smoothies")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

fruit_options = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")

ingredient_list = st.multiselect("Ingredients:", fruit_options)

if ingredient_list:
    ingredient_string = " ".join(str(fr) for fr in ingredient_list)

    if st.button("OK"):
        session.sql(
            "INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (?, ?)",
            params=[ingredient_string, name_on_order]
        ).collect()
        st.success("Your Smoothie is ordered, " + name_on_order + "!", icon="✅")
