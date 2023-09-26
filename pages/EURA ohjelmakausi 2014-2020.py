import datetime
import plotly.express as px


def generate_eura_project_viz(df, filter_ended=True):
    # Convert the start and end date columns to datetime format
    df['Aloituspvm'] = pd.to_datetime(df['Aloituspvm'])
    df['Päättymispvm'] = pd.to_datetime(df['Päättymispvm'])

    # Filter only ongoing projects if required
    if filter_ended:
        today = pd.Timestamp(datetime.date.today())
        df = df[df['Päättymispvm'] > today]

    # Add a truncated name column
    max_length = 60
    df['Truncated Name'] = df['Hankekoodi'].apply(lambda x: truncate_text(x, max_length))

    # Create a custom column for the hover information
    df['Hover Info'] = 'Budget: ' + df['Myönnetty_EU_ja_valtion_rahoitus'].astype(str)

    # Create the Gantt chart using plotly
    fig = px.timeline(df, x_start="Aloituspvm", x_end="Päättymispvm", y="Truncated Name", 
                      color="Truncated Name", 
                      hover_name="Hankekoodi", 
                      hover_data=["Hover Info"], 
                      title="EURA2020 Projects")

    fig.update_yaxes(categoryorder="total ascending")  # Sort projects based on start date
    fig.update_traces(marker_line_width=df['Myönnetty_EU_ja_valtion_rahoitus']/500000)  # Set line width based on budget

    # Remove the color legend
    fig.update_layout(showlegend=False)
    
    # Hide the y-axis label
    fig.update_layout(yaxis_title_text="")

    # In a real Streamlit app, we would display the plot using st.plotly_chart(fig)
    return fig

# Mock the Streamlit app using a hypothetical filter value (for demonstration purposes)
toteuttaja_name = "Kainuun Liikunta ry"
eura_data_filtered = fetch_eura_data(toteuttaja_name)
generate_eura_project_viz(eura_data_filtered, filter_ended=True)
