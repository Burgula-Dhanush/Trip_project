import os
import streamlit as st
from usellm import UseLLM, Message, Options
from utils1 import TOUR_GUIDE_SYSTEM, TRIP_PLANNER_SYSTEM
from utils1 import format_trip_planner_message 

service = UseLLM(service_url="https://usellm.org/api/llm")

st.set_page_config(layout="wide")

page_bg_img = """
<style>

 [data-testid="stApp"]{
 background-image:url('https://raw.githubusercontent.com/Mallika2002/TripGenie/main/sky.jpg');
 background-size:cover;
 }

 [data-testid="stToolbar"]{
 right:2rem;
 }

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Path to the trips.txt file
trips_file_path = os.path.join(os.path.dirname(__file__), '..', 'trips.txt')

# Check if the trips.txt file exists
if os.path.exists(trips_file_path):

# Read the contents of the trips.txt file
    with open(trips_file_path, 'r') as file:
        trips_content = file.read()

# Split the places by commas
    places = [place.strip() for place in trips_content.split(',')]

# Display the places in the Streamlit sidebar
    # st.sidebar.header("Configuration")
    st.sidebar.header("Your Trips:")
    # st.sidebar.write(places)
    # Apply CSS styling to each place
    for place in places:
         
         st.sidebar.markdown(f'<div class="place-block">{place}</div>', unsafe_allow_html=True)

# Add custom CSS for styling the place blocks and adjusting sidebar width
    custom_css = """
        <style>


        .place-list {
            display: flex;
            flex-wrap: wrap;
        }

            .place-block {
            background-color: #eaf9e2; /* Subtle green color */
            padding: 5px;
            margin: 5px;
            display:inline-block;
            border-radius: 5px;
            width: 100px; /* Set a fixed width for each block */
            color:black;
            }
        </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

else:
    st.sidebar.warning("No trips found.")
# st.sidebar.header("Configuration")

# Your Streamlit app content goes here
# st.title("My Streamlit App")
# st.write("Welcome to my app!")


# st.set_page_config(layout="wide")

# @st.cache(allow_output_mutation=True)

# def get_response_cache():
#     return None



    # Custom CSS for styling input box
custom_css = """
    <style>
        .stTextInput{
            width:1200px !important;
        }
        .stTextInput input {
            color: black !important;
            background-color: lightyellow !important;
            border:1px solid black !important;
        }
        
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

places=[] 

def tour_guide_section():
    st.title(r"$\textsf{\Large Tour Guide Assistant}$")
    user_input = st.text_input(r"$\textsf{\normalsize Enter the Place You Want to Visit}$", key="input1")
    if st.button(r"$\textsf{\normalsize Send}$", key="button1"):
        if user_input:
            system_message = TOUR_GUIDE_SYSTEM
            output = get_response(system_message, user_input)
            st.markdown(output.content)
        else:
            st.markdown("Please Enter Some Text")

def trip_planner_section():
    st.title(r"$\textsf{\Large Personal Trip Planner}$")
    user_location_path = os.path.join(os.path.dirname(__file__), 'user_location.txt')
    with open(user_location_path, 'r', encoding='utf-8') as location_file:
        user_location = location_file.read().strip()

    print(f"User Location: {user_location}")

    user_input = st.text_input(r"$\textsf{\normalsize Enter the Place You Want to Visit}$", key="input2")
    days = st.text_input(r"$\textsf{\normalsize Enter the Number of Days}$", key="input3")
    budget = st.text_input(r"$\textsf{\normalsize Enter the Budget per person}$", key="input4")

    if st.button(r"$\textsf{\normalsize Send}$", key="button2"):
        if user_location and user_input:
            system_message = TRIP_PLANNER_SYSTEM.format(days=days, budget=budget, user_location=user_location, user_input=user_input)
            output = get_response(system_message, user_input)
            st.markdown(output.content)


            places.append(user_input)

            # Update the sidebar immediately with the new place
            display_places_sidebar()

             # Path to the user_data file
            shared_data_path = os.path.join(os.path.dirname(__file__), '..', 'user_data.txt')

            # Read existing data from the file
            with open(shared_data_path, "a", encoding='utf-8') as file:
                # Append the new input to all lines in the file with a comma
                file.write(f"{user_input},")
        else:
            st.markdown("Please Enter Some Text")

def display_places_sidebar():
    # Display the places in the Streamlit sidebar
    global places  # Declare places as a global variable

    # Apply CSS styling to each place
    for place in places:
        st.sidebar.markdown(f'<div class="place-block">{place}</div>', unsafe_allow_html=True)

# @st.cache
def get_response(system_message, user_input, *args):
    messages = [
        Message(role="system", content=system_message),
        Message(role="user", content=user_input)
    ]
    options = Options(messages=messages)
    output = service.chat(options)
    # get_response_cache.clear_cache()  # Clear the entire cache
    # get_response_cache()  # Save the new output to the cache
    return output

def show(output):
    if output:
        st.markdown(output.content)
    elif output == "NULL":
        st.markdown("Please Enter Some Text")

def main():
    tab1, tab2 = st.tabs([r"$\textsf{\Large Tour Guide}$", r"$\textsf{\Large Trip Planner}$"])

    with tab1:
        output = tour_guide_section()
        show(output)

    with tab2:
        output = trip_planner_section()
        show(output)

if __name__ == "__main__":
    main()
