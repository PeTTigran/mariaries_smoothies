# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruties you want in your custom Smoothie!
    """
)

name_of_order = st.text_input("Name of Smoothie:")
st.write("Name of your Smoothie will be", name_of_order)
cnx=st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
st.dataframe(data=my_dataframe, use_container_width=True)
#st.dataframe(data=my_dataframe, use_container_width=True)

ingrediente_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=6
)
if ingrediente_list:
    #st.write(ingrediente_list)
    #st.text(ingrediente_list)

    ingredients_string =''

    for fruit_chosen  in ingrediente_list:
        ingredients_string += fruit_chosen +' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """', '""" + name_of_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
