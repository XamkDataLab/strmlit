import streamlit as st
y_tunnus = st.session_state.get('y_tunnus')
st.title(f"Details for {y_tunnus}")
# detailed_info.py


def app():
    y_tunnus = st.session_state.get('y_tunnus', 'Unknown')  # Get y_tunnus from session state
    query_type = st.session_state.get('type', 'Unknown')  # Get query type from session state

    st.title(f"Details for {y_tunnus}")

    if y_tunnus != 'Unknown' and query_type != 'Unknown':
        data = another_fetch_data_function(y_tunnus, query_type)
        
        if not data.empty:
            # Code to display data and visualization
            ...
        else:
            st.write("No data found.")
    else:
        st.write("Invalid or missing parameters.")


