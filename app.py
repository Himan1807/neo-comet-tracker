import streamlit as st  # python framework used for building interactive web applications for Data Science and Machine Learning
import requests  # for making HTTP requests
import pandas as pd  # for data manipulation
import plotly.express as px  # for data visualization
from datetime import datetime, timedelta  # for data operations
import sys  # to handle system-specific parameters and functions
import io  # to handle I/O operations

# Mapping of display names to API body codes
# Define a dictionary mapping celestial bodies to their API codes
BODY_CODES = {
    'Mercury': 'Merc',
    'Venus': 'Venus',
    'Earth': 'Earth',
    'Mars': 'Mars',
    'Jupiter': 'Juptr',
    'Saturn': 'Satrn',
    'Uranus': 'Urnus',
    'Neptune': 'Neptn',
    'Moon': 'Moon'
}

# Function to fetch close approach data
# Define function with default parameters
def fetch_close_approaches(body_code='Earth', min_date='now', max_date='+60', max_dist='0.05', dist_unit='AU', my_limit=100, object_type='NEO'):
    url = 'https://ssd-api.jpl.nasa.gov/cad.api'  # define the API URL
    my_params = {     # create a dictionary of parameters for API request
        'body':body_code,
        'date-min': min_date,
        'date-max': max_date,
        'dist-max': f"{max_dist}{dist_unit}",
        'limit': my_limit
    }
    
    # Filter by object type if selected
    if object_type == 'NEO':   # check if object type is Near-Earth Object
        my_params['neo'] = 'true'    # add 'neo' parameter to API request
    elif object_tye == 'Comet':   # check if object type is comet
        my_params['comet'] = 'true'   # Add 'comet' parameter to API request
        
    # Start try block to handle potential exceptions
    try: 
        response = requests.get(url, params=my_params)  # make GET request to API
        response.raise_for_status()  # raise HTTPError for bad responses
        data = response.json()  # parse JSON response
        return data  # return the fetched data
    except requests.exceptions.HTTPError as http_err:   # Handle HTTP errors
        st.error(f"⚠️ HTTP error occurred: {http_err}")    # Display HTTP Error message in Streamlit
        try:  # Start nested try block to parse error details
            error_info = response.json()   # attempt to parse error details from response
            st.error(f"🔍 Error Details: {error_info}")    # display error details in Streamlit
        except ValueError:   # Handle cases where response is not JSON
            st.error(f"🔍 No additional error information provided.")   # inform user no extra error info is available
        return None   # return None due to error
    except requests.exceptions.RequestException as e:   # handle other request exceptions
        st.error(f"⚠️ Error fetching data from API: {e}")      # display general error message in Streamlit
        return None
    
# function to parse the data
def parse_data(data):   # Define function to parse API data
    if data is None or data.get('count', 0) == 0:  # check if data is empty or count is zero
        st.warning("⚠️ No close approached found for the given parameters.")
        return pd.DataFrame()  # return empty DataFrame
    
    fields = data.get('fields', [])   # get field names from data
    records = data.get('data', [])    # get records from data
    fd = pd.DataFrame(records, columns=fields)   # create DataFrame from records and fields
    
    # convert relevant columns to appropriate data types
    fd['cd'] = pd.to_datetime(fd['cd'], format='%Y-%b-%d %H:%M')   # convert 'cd' columns to datetime
    fd['dist'] = pd.to_numeric(fd['dist'], errors='coerce')   # convert 'dist' columnt to numeric, coercing errors
    fd['v_rel'] = pd.to_numeric(fd['v_rel'], errors='coerce')   # convert  'v_rel' column to numeric, coercing errors
    fd['v_inf'] = pd.to_numeric(fd['v_inf'], errors='coerce')   # convert 'v_inf' column to numeric, coercing errors
    
    return fd    # return the parsed DataFrame

# Function to visualize the data using Plotly with trendline(optional)          
def visualize_close_approaches(fd, body, add_trendline=False):   # Define visualization fucntion with optional trendline
    if fd.empty:    # check if DataFrame is empty
        return    # exit function if no data is available
    
    # check if trendline is requested and statsmodels is installed
    if add_trendline:
        try:
            import statsmodels.api as statsmodels
        except ImportError:
            st.warning("⚠️ Statsmodels is not installed. Trendline feature is disabled")
            add_trendline = False    # disable trendline feature
    
    if add_trendline:   # check again if trendline is to added after import
        my_trendline = "ols"    # set trendline type to Ordinary Least Squares
    else:    # if trendline is not to be added
        my_trendline = None   # no trendline
         
    fig = px.scatter(    # create a scatter plot using Plotly Express
        fd,    # DataFrame to plot
        x='cd',   # set x-axis to 'cd' column
        y='dist',
        hover_data=['des', 'v_rel', 'v_inf'],
        labels={
            'cd': '📅 Date',
            'dist': f'📏 Distance ({st.session_state.get("dist_unit", "AU")})',   # label for 'dist' axis with unit
            'des': '🪐 Designation',     # label for 'des' hover data
            'v_rel': '⚡ Relative Velocity (km/s)',      # label for 'v_rel' hover data
            'v_inf': '∞ Infinity Velocity (km/s)'   # label for 'v_inf' hover data          
        },
        title = f'🔭 Close Approached to {body}',    # set the title of the plot
        trendline = my_trendline      # add trendline if specified
    )        
    
    fig.update_yaxes(autorange="reversed")    # invert the y-axis for better visualization
    st.plotly_chart(fig, use_container_width = True)    # display the plotly chart in Streamlit
    
    
# Streamlit App
def main():
    st.set_page_config(page_title = "🌌 Asteroid and Comet Close Approaches Visualizer", layout="wide")   # set page configuration
    st.title("🌌 Asteroid and Comet Close Approaches Visualizer")    # set the title of the app
    st.markdown("""
    Welcome to the **Asteroid and Comet Close Approaches Visualizer**! 🚀  
    Explore past and future close approaches of asteroids and comets to various celestial bodies.
    Use the sidebar to customize your search parameters and visualize the data interactively.
    """)
    
    st.sidebar.header("Input Parameters")   # add header to the sidebar
    
    # Celestial Body Selection
    body_display_options = list(BODY_CODES.keys())    # get the list of celestial body display options
    body_display = st.sidebar.selectbox(        # create a select box for choosing from the listed celestial bodies
            "🪐 Select Celestial Body",    # label for the select box
            body_display_options,     # options for selection(taken as keys from display_options)
            index = 2,     # default selection index = 2 (Earth)
            help="Choose the celestial body you want to analyze close approaches to."    # Help tooltip                    
    )
    body_code = BODY_CODES[body_display]    # get the API code for the selected body
    
    # date range selection
    st.sidebar.subheader("Date Range")     # add subheader for date range
    today = datetime.today()     # get today's date
    default_end_date = today + timedelta(days=60)    # set default end date to 60 days from today
    
    min_date = st.sidebar.date_input(    # create date input for start date
        "🔹Start Date",    # label for start date
    value=today,    # default value = today
    min_value = datetime(1900, 1, 1),   # min selectable date
    max_value = datetime(2100, 12, 31),  # max selectable date
    help="Select the start date for the close approaches data."   # Help tooltip
    )
    
    max_date_option = st.sidebar.selectbox(     # create select box for end date option
        "🔸End Date Option",     # label for end date option
        options=['Days from Start Date', 'Specific Date'],     # options available
        index=0,
        help="Choose how to specify the end date for the date range"       # help tooltip
    )
    
    if max_date_option == 'Days from Start Date':    # check if end date is based on days from start date
        days_from_start = st.sidebar.number_input(    # create number input for days from start date
            "📅 Number of Days from Start Date",     # label for number input
            min_value = 1,    # min no. of days
            max_value = 36525,    # max no. of days (100 years)
            value = 60,     # default no. of days
            step = 1,   # step size of input
            help = "Specify the number of days from the start date to set the end date."    # help tooltip
        )
        max_date = (datetime.combine(min_date, datetime.min.time()) + timedelta(days=days_from_start)).strftime('%Y-%m-%d')   # calculate end date based on days from start
    elif max_date_option == 'Specific Date':     # check if end date is a specific date
        specific_max_date = st.sidebar.date_input(     # create date input for specific end date
            "📅 End Date",     # label for end date
            value=default_end_date,    # default end date (60 days from today)
            min_value=min_date,    # min selectable date
            max_value=datetime(2100, 12, 41),    # max selectable date
            help="Select a specific end date for the close approaches data."    # help tooltip
        )
        max_date = specific_max_date.strftime('%Y-%m-%d')   # format end date as string
        
    # distance unit selection (AU or LD)
    st.sidebar.subheader("Distance Parameters")    # add subheader
    dist_unit = st.sidebar.selectbox(    # create select box for distance unit
        "📐 Distance Unit",     # label for distance unit selection
        options = ['AU', 'LD'],   # options: Astronomical Units or Lunar Distances
        index = 0,      # default selection type: 'AU'
        help = 'Choose the unit for maximum distance: Astronomical Units(AU) or Lunar Dustances(LD).'  # help tooltip
    )
    default_max_dist = '0.05' if dist_unit == 'AU' else '10'   # set default maximum distance
    max_dist = st.sidebar.text_input(     # create text input for maximum distance
        "🔝 Maximum Distance",
        value = default_max_dist,    # default value for max distance
        help = f"Set the maximum distance for close approaches in {dist_unit}."     # help tooltip with unit
    )
        
    # Object Type Filter
    st.sidebar.subheader("Object Type & Results")    # add subheader for object type and results
    object_type = st.sidebar.selectbox(      # create select box for object type filter
        "☄️ Object Type",      # label for object type selection
        options = ['NEO', 'Comet', 'Both'],   # options: Near-Earth Objects, Comets, or Both
        index = 0,    # default value = 'NEO'
        help = "Filter results by object type: Near-Earth Objects(NEO), Comets, or Both."     # help tooltip 
    )   
        
    # Number of results
    limit = st.sidebar.number_input(    # create number input for result limit
        "📈 Number of Results to Fetch",     # label for no. of results
        min_value = 1,     # min no. of results
        max_value = 1000,     # max no. of results
        value = 100,     # default no. of results   
        step = 1,     # step size for input
        help = "Specify how many close approach records to retrieve."     # help tooltip 
    )
        
    # Submit Button
    fetch_data = st.sidebar.button("🚀 Fetch and Visualize Data")    # create a button to fetch and visualize data
        
    if fetch_data:      # check if the fetch button was clicked
        with st.spinner("⏳ Fetching data...."):    # show a spinner while fetching data
            if object_type in ['NEO', 'Comet']:   # check if object type is 'NEO' or 'Comet'
                # single API call
                data = fetch_close_approaches(     # fetch close approach data using API
                    body_code = body_code,    # pass celestial body code
                    min_date = min_date.strftime('%Y-%m-%d'),      # pass formatted start date
                    max_date = max_date,     # pass end date
                    max_dist = max_dist,      # pass maximum distance 
                    dist_unit = dist_unit,     # pass distance unit
                    my_limit = limit,     # pass result limit 
                    object_type = object_type     # specify object type as 'NEO'
                )
                fd = parse_data(data)  # parse the fetched data into DataFrame
            elif object_type == 'Both':     # check if object type is 'Both'
                # two separate API calls and combine
                data_neo = fetch_close_approaches(
                    body_code = body_code,     # pass celestial body code
                    min_date = min_date.strftime('%Y-%m-%d'),     # pass formatted start date
                    max_date = max_date,     # pass end date
                    max_dist = max_dist,      # pass maximum distance
                    dist_unit = dist_unit,     # pass distance unit
                    my_limit = limit,     # pass result limit
                    object_type = 'NEO'     # specify the object type as 'NEO'
                )
                data_comet = fetch_close_approaches(    # fetch comet data using API  
                    body_code = body_code,    # pass celestial body code
                    min_date = min_date.strftime('%Y-%m-%d'),   # pass formatted start date
                    max_date = max_date,    # pass end date
                    max_dist = max_dist,     # pass maximum distance
                    dist_unit = dist_unit,     # pass distance unit
                    my_limit = limit,    # pass result limit
                    object_type = 'Comet'    # specify object type as 'Comet'    
                )
                fd_neo = parse_data(data_neo)    # parse NEO data into DataFrame
                fd_comet = parse_data(data_comet)   # parse Comet data into DataFrame
                    
                # combine dataframes
                fd = pd.concat([fd_neo, fd_comet], ignore_index = True)    # concatenate NEO and Comet DataFrames
                fd.drop_duplicates(inplace = True)   # remove duplicated records
                    
        if not fd.empty:   # check if DataFrame is not empty
            st.success(f"✅ Found {len(fd)} close approaches to **{body_display}**.")    # display success message with count
                
            # Store DataFrame in Session State
            st.session_state['fd'] = fd  # save DataFrame to session state
            st.session_state['body_display'] = body_display  # save selected body display name to session state
            st.session_state['dist_unit'] = dist_unit   # save distance unit to session state
        else:   # if DataFrame is empty
            st.session_state['fd'] = pd.DataFrame()   # save empty DataFrame to session state
            st.session_state['body_display'] = body_display
            st.session_state['dist_unit'] = dist_unit
                
    # check if data is available in session state
    if 'fd' in st.session_state and not st.session_state['fd'].empty:  # check for data in session state
        fd = st.session_state['fd']   # retrieve DataFrame from session state
        body_display = st.session_state['body_display']   # retrieve selected body display name 
        dist_unit = st.session_state['dist_unit']     # retrieve distance unit
            
        # display the data table
        st.subheader("📊 Close Approach Data")   # add subheader for data table
        st.dataframe(fd[['des', 'cd', 'dist', 'v_rel', 'v_inf']].rename(columns={    # display DataFrame with renamed columns
            'des': '🪐 Designation',   # rename 'des' to 'Designation'
            'cd': '📅 Date',  # rename 'cd' to 'Date'
            'dist': f'📏 Distance ({dist_unit})',   # rename 'dist' to 'Distance' with unit
            'v_rel': '⚡ Relative Velocity (km/s)',   # rename 'v_rel' to 'Relative Velocity'
            'v_inf': '♾️ Infinity Velocity (km/s)'   # rename 'v_inf' to 'Infinity Velocity'
        }))   # end of rename dictionary 
            
        # download button for CSV
        csv = fd.to_csv(index = False).encode('utf-8')   # convert DataFrame to CSV and encode
        st.download_button(    # create a download button for CSV
            label = "📥 Download Data as CSV",   # label for download button
            data = csv,  # data to download
            file_name = 'close_approaches_data.csv',   # name of the downloaded file
            mime = 'text/csv'  # MIME type for csv
        )
            
        # trendline toggle in main area
        st.markdown("---")   # add a horizontal separator
        st.subheader("📈 Visualization")   # add subheader for visualization
        add_trendline = st.checkbox("✨ Add Trendline (Requires statsmodels)")    # Create a checkbox to add trendline
            
        # visualization
        visualize_close_approaches(fd, body_display, add_trendline = add_trendline)   # call visualization function
            
    else:   # if no data is available in session state
        if fetch_data:   # check if fetch button was clicked
            st.info("ℹ️ No data available to display. Please adjust your search parameters.")   # inform user no data found
        else: # if fetch button was not clicked
            st.info("🔍 Awaiting your search parameters. Use the sidebar to get started!")   # inform user to provide search parameters
                
    st.markdown("""
    ---
    **🛰️ Data Source:** JPL's SSD/CNEOS CAD API 
    """)
        
if __name__ == '__main__':   # check if script is run as main program
    main()  # execute the main function to run the Streamlit app