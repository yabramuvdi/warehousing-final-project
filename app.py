import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from load_final import calls_data

my_acc = calls_data()

app = dash.Dash('dash-tutorial')

app.layout = html.Div(className = 'layout', children = [
    html.H1('Classic Models Dashboard', className = 'title'),

    html.H4('My subtitle for my cool dashboard', className='subtitle'),

    dcc.Graph(id='timeline', figure={
        'data': [go.Bar(x = my_acc[['number_of_persons_injured', 'borough']].groupby(['borough']).sum().index,
                            y = my_acc[['number_of_persons_injured', 'borough']].groupby(['borough']).sum().number_of_persons_injured)],
        'layout': {
            'title': 'My graph'
        }
        })
])

app.run_server(debug=True)
