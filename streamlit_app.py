# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Custom Smoothie Order form! :cup_with_straw:")
st.write(
    """Choose the fruties you want in your custom Smoothie!
    """
)

name_of_order = st.text_input("Name of Smoothie:")
st.write("Name of your Smoothie will be", name_of_order)
cnx=st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
            st.success("OK.",icon='👍')
        except:
            st.write("Something went wrong")
else:
    st.success('There are no order')
    
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
