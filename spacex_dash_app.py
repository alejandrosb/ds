import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('spacex_launch_dash.csv')
app = dash.Dash(__name__)
launch_sites = df['Launch Site'].unique()

app.layout = html.Div(children=[
    html.H1(children='SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    html.Label('Select Launch Site:'),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All sites', 'value': 'All sites'}] + [{'label': site, 'value': site} for site in launch_sites],
        value=launch_sites[0]
    ),

    dcc.Graph(id='success-pie-chart'),

    html.Label('Select Payload Range (Kg):'),
    dcc.RangeSlider(
        id='payload-slider',
        min=df['Payload Mass (kg)'].min(),
        max=df['Payload Mass (kg)'].max(),
        value=[df['Payload Mass (kg)'].min(), df['Payload Mass (kg)'].max()],
        marks={i: str(i) for i in range(0, int(df['Payload Mass (kg)'].max()) + 2500, 2500)},
        step=100
    ),

    dcc.Graph(id='success-payload-scatter-chart')
])


@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'All sites':
        success_counts = df[(df['class'] == 1)] 
        fig = px.pie(success_counts, names='Launch Site', values='class',
                    title=f'Total Success Launches by {selected_site}')
        return fig
    else:
        filtered_df = df[df['Launch Site'] == selected_site]
        success_counts = filtered_df['class'].value_counts()
        fig = px.pie(success_counts, names=success_counts.index, values=success_counts.values,
                    title=f'Success Rate for {selected_site}')
    return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'All sites':
        fig = px.scatter(df, x='Payload Mass (kg)', y='class',
                        title=f'Correlation between Payload and Success for {selected_site}',
                        labels={'Success': 'Success (True/False)'}, color="Booster Version Category")
        return fig
    else:
        filtered_df = df[(df['Launch Site'] == selected_site) &
                        (df['Payload Mass (kg)'] >= payload_range[0]) &
                        (df['Payload Mass (kg)'] <= payload_range[1])]
        
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                        title=f'Correlatio between Payload and Success for {selected_site}',
                        labels={'Success': 'Success (True/False)'},color="Booster Version Category")
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    app.run(debug=False)