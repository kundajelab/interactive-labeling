import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from dash.dependencies import State, Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


dict = {i: np.random.uniform(0,20,30) for i in ['X', 'Y']}
dict['Class'] = np.random.randint(3, size=30)
xyDf = pd.DataFrame(dict)

# nbrs = NearestNeighbors(n_neighbors = 5, algorithm = 'ball_tree').fit(xyDf)
# distances, indices = nbrs.kneighbors(xyDf)
# print(distances)
# print(indices)

colors = {
    0: 0,
    1: 120,
    2: 240
}

# groups = []
# for label in labelDf['label'].unique():
#     groups.append({
#         'x':
#         'y':
#         'legendgroup': i,
#         'name': i,
#         'mode': 'markers',
#         'marker': {
#             'color': colors[i]
#         }
#     })

print(xyDf)

app.layout = html.Div([
    html.H2(children = 'Insert Title Here', style={'text-align':'center'}),
    html.Div([
        html.H5(children = 'Choose Color Scheme:'),
        dcc.RadioItems(
            id='color-options',
            options=[{'label':'Labels Only', 'value':'labels'},
                     {'label':'kNN Predictions', 'value':'gradient'}],
            value='labels',
            labelStyle={'display': 'inline-block', 'padding': '5px'}
        )
    ],
    style={'width': '49%'}),

    dcc.Graph(
        id = 'main-scatter'
    )
])

@app.callback(Output('main-scatter', 'figure'),
              [Input('color-options', 'value'),
               Input('main-scatter', 'clickData')])
def updateGraph(colorOption, clickData):
    if(colorOption == 'gradient'):
        if clickData:
            print(clickData)
            for click in clickData['points']:
                print (click)
                changeColors(click['x'], click['y'])
        clickmode = 'event+select'
    else:
        colorOption = 'hsl(210, 0, 50)'
        clickmode = 'none'

    return {
        'data': [{
            'x': xyDf['X'],
            'y': xyDf['Y'],
            'type': 'scatter',
            #'hoverinfo': ,
            'mode': 'markers+text',
            'marker': {
                'color': colorOption,
                'size': 12,
                'line': {
                    'color': 'rgb(0, 116, 217)',
                    'width': 0.5
                }
            },
        }],
        'layout': go.Layout(
            #xaxis={'title': ''},
            #yaxis={'title': ''},
            margin={'l': 40, 'b': 40, 't': 20, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            clickmode=clickmode
        )

    }

def changeColors (X, Y):
    plotly.addTraces(main-scatter,{
        x: X,
        y: Y,
        type: 'scatter',
        mode: 'markers',
        marker: {'color': 'blue'},
    })

if __name__ == '__main__':
    app.run_server(debug=True)
