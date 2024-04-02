from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import layout

app = Dash(__name__, suppress_callback_exceptions=True)
app.index_string = layout.index_string

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    layout.create_sidebar(),
    layout.create_global_filters(),  # Place the global filters above the page content
    html.Div(id='page-content')
])

df = pd.read_csv('Activities.csv')
df['Date'] = pd.to_datetime(df['Date'])  # Ensure 'Date' column is in datetime format for filtering


# Plot functions (updated to return figures instead of calling fig.show())
def create_activity_pie_chart(df):
    activity_counts = df['Activity Type'].value_counts()
    fig = px.pie(activity_counts, values=activity_counts.values, names=activity_counts.index, 
                 title='Distribution of Activity Types', color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

def create_running_distance_histogram(df):
    df_running = df[df['Activity Type'].isin(['Running', 'Trail Running'])]
    fig = px.histogram(df_running, x='Distance', color='Activity Type',
                       title='Distribution of Distances for Running/Trail Running Activities',
                       labels={'Distance': 'Distance (km)', 'count': 'Number of Activities'},
                       barmode='overlay', histnorm='percent',
                       color_discrete_map={'Running': '#1f77b4', 'Trail Running': '#ff7f0e'})
    fig.update_traces(xbins=dict(start=0, end=df_running['Distance'].max(), size=2))
    fig.update_traces(hovertemplate='Distance: %{x} km<br>Percentage: %{y}%<extra></extra>')
    return fig

def create_running_distance_calories_scatter(df):
    df_running = df[df['Activity Type'].isin(['Running', 'Trail Running'])]
    fig = px.scatter(df_running, x='Distance', y='Calories',
                     title='Calories Burned vs. Distance for All Running Activities',
                     labels={'Distance': 'Distance (km)', 'Calories': 'Calories Burned'})
    fig.update_yaxes(type="linear")
    return fig

def create_running_time_series_moving_time(df):
    df_running = df[df['Activity Type'].isin(['Running', 'Trail Running'])].copy()
    df_running['Date'] = pd.to_datetime(df_running['Date'])
    df_running['Moving Time'] = pd.to_timedelta(df_running['Moving Time'], errors='coerce')
    df_running.dropna(subset=['Moving Time'], inplace=True)
    df_running['Moving Time Seconds'] = df_running['Moving Time'].dt.total_seconds()
    df_running.sort_values(by='Date', inplace=True)
    fig = px.line(df_running, x='Date', y='Moving Time Seconds',
                  title='Moving Time for All Running Activities')
    fig.update_layout(yaxis_tickformat='%H:%M:%S', yaxis_title='Moving Time (hh:mm:ss)')
    return fig

@app.callback(
    [Output('activity-pie-chart-graph', 'figure'),
     Output('distance-calories-scatter-graph', 'figure'),
     Output('running-time-series-graph', 'figure'),
     Output('running-distance-histogram-graph', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_plots(start_date, end_date):
    if start_date is not None and end_date is not None:
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    else:
        filtered_df = df

    return [
        create_activity_pie_chart(filtered_df),
        create_running_distance_calories_scatter(filtered_df),
        create_running_time_series_moving_time(filtered_df),
        create_running_distance_histogram(filtered_df)
    ]

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/analytics':
        return html.Div([
            dcc.Graph(id='activity-pie-chart-graph', figure=create_activity_pie_chart(df)),
            dcc.Graph(id='distance-calories-scatter-graph', figure=create_running_distance_calories_scatter(df)),
            dcc.Graph(id='running-time-series-graph', figure=create_running_time_series_moving_time(df)),
            dcc.Graph(id='running-distance-histogram-graph', figure=create_running_distance_histogram(df))
        ], className='grid-container')  # Use this class name

    else:
        return layout.render_content(pathname)

if __name__ == '__main__':
    app.run_server(debug=True)
