# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

st.success("Snowpark is working!")
helpful_links = [
     "https://docs.streamlit.io",
     "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
     "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
     "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
 ]

# Write directly to the app
st.title(":cup_with_straw: Custom Smoothies Here!! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st. text_input ( 'Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st. connection ("snowflake")
session = cnx.session()

#session = get_active_session()
#my_dataframe = session. table ("smoothies.public.fruit_options").select (col ('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe. to_pandas()
st. dataframe (pd_df)
st.stop()

ingredients_list = st.multiselect( 'Choose up to 5 ingredients:', my_dataframe, max_selections=5)
if ingredients_list:

    ingredients_string = ''
     #search on SEARCH_ON
    for fruit_chosen in ingredients_list:
          ingredients_string += fruit_chosen + ' '
          st. subheader (fruit_chosen + ' Nutrition Information' )
          smoothiefroot_response = requests.get ("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
          sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

     #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
             values ('""" + ingredients_string + """','"""+name_on_order+ """') """

time_to_insert = st. button ('Submit Order') 

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered,' + name_on_order + '!', icon="✅")
