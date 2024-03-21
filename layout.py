from dash import html, dcc
from datetime import date

index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" type="text/css" href="/assets/style.css">
    </head>
    <body>
        <div class="main-container">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>'''



def create_global_filters():
    global_filters = html.Div([
        html.Div([
            html.Label('Select Date Range:'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=date(2023, 1, 1),  # Adjust these dates based on your data
                end_date=date(2028, 12, 31),
                display_format='YYYY-MM-DD',
                end_date_placeholder_text='Select a date!'
            ),
        ], style={'margin-bottom': '20px'}),
        # Add more global filters here as needed
    ], style={'padding': '20px', 'margin-bottom': '20px', 'border': '1px solid #ddd', 'marginLeft': '260px'})  # Adjusted marginLeft

    return global_filters

def create_sidebar():
    sidebar = html.Div([
        html.Div(html.Img(src='/assets/logo.png', className='logo'), className='logo-container'),
        html.H2('Menu', className='sidebar-title'),
        html.Div([
            dcc.Link('Home', href='/', className='sidebar-link', id='home-link'),
            dcc.Link('Analytics', href='/analytics', className='sidebar-link', id='analytics-link'),
            dcc.Link('Settings', href='/settings', className='sidebar-link', id='settings-link'),
        ], className='menu-links')
    ], id='sidebar')
    return sidebar

def render_content(pathname):
    """Render content based on the navigation path."""
    if pathname == '/analytics':
        content = html.Div([
            create_global_filters(),  # This adds the global filters section to the top of the page
            html.Div([
                html.H3('Analytics Dashboard', className='content-title'),
                html.Div(id='running-time-series-container'),  # Container for running time series plot
                html.Div(id='activity-pie-chart-container'),   # Container for activity pie chart
                html.Div(id='distance-calories-scatter-container'),  # Container for distance vs. calories scatter plot
                # Add more containers as needed for additional plots
            ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))', 'gap': '20px'}),
        ])
        
        return content


