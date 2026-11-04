
# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("My Parents New Healthy Diner")

st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)

# Get customer's name
name_on_order = st.text_input("Name of the Smoothie:")

st.write("The name on your smoothie will be:", name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()


# Read fruit options from Snowflake
my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col("FRUIT_NAME"))


# Display fruit options
# st.dataframe(data=my_dataframe, use_container_width=True)


# Allow user to select up to 5 ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    [row["FRUIT_NAME"] for row in my_dataframe.collect()],
    max_selections=5
)


# Process selected ingredients
if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # Prepare SQL INSERT statement
    my_insert_stmt = """INSERT INTO smoothies.public.orders
                        (ingredients, name_on_order)
                        VALUES ('""" + ingredients_string.strip() + """', '""" + name_on_order.replace("'", "''") + """')"""

    # Display SQL statement for testing
    st.write(my_insert_stmt)

    # Submit order button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:

        if not name_on_order.strip():
            st.warning("Please enter your name before submitting!")

        else:
            session.sql(my_insert_stmt).collect()

            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
