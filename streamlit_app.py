import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('My parents new healthy diner.')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#let's put a pick list here so they can chose the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on the page
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice API response
streamlit.header('Fruityvice Fruit Advice!')
#Add atextbox to enter fruit name
fruit_choice=streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

fruityvice_response= requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
#output it to the screen as a table
streamlit.dataframe(fruityvice_normalized)

#let's query our trial account metadata
my_cnx = snowflake.connector.connect(**streamlit.secrets["Snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("Fruit Load List Contains:")


streamlit.dataframe(my_data_row)

#Allow the enduser to add a fruit
add_my_fruit=streamlit.text_input('What fruit would you like to add?', 'Kiwi')
streamlit.write('Thanks for adding', add_my_fruit)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('Test')")
