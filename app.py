import dash
import dash_core_components as dcc
import dash_html_components as html
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

nbrs = NearestNeighbors(n_neighbors = 6, algorithm = 'ball_tree').fit(xyDf)
distances, indices = nbrs.kneighbors(xyDf)

colors = {
    0: 0,
    1: 120,
    2: 240
}

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
    ]),
    dcc.Graph(
        id = 'main-scatter',
    ),
    html.Div(id='hidden-div', style={'display':'none'})
])


@app.callback(Output('main-scatter', 'figure'),
              [Input('color-options', 'value'),
               Input('main-scatter', 'clickData')],
              [State('main-scatter', 'figure')])
def updateGraph(colorOption, clickData, figureData):
    if colorOption == 'gradient':
        clickmode = 'event+select'
        if colorOption:
            colorOption = figureData['data'][0]['marker']['color']
        if clickData:
            for point in clickData['points']:
                index = point['pointIndex']
                if(colorOption[index] == 'gray'):
                    colorOption[index] = 'hsl({},60,70)'.format(colors[xyDf['Class'][index]])
                else:
                    colorOption[index] = 'gray'
    else:
        colorOption = ['gray'] * xyDf.size
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
                'colorscale': 'Viridis',
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


@app.callback(Output('hidden-div', 'children'),
              [Input('main-scatter', 'clickData')],
              [State('hidden-div', 'children')])
def knnColoring(clickData, pastData):
    activatedPoints = []
    if pastData and pastData != ' ':
        activatedPoints = list(map(int, pastData.split(' ')))

    if clickData:
        clickIndex = clickData['points'][0]['pointIndex']
        if clickIndex in activatedPoints:
            activatedPoints.remove(clickIndex)
        else:
            activatedPoints.append(clickIndex)

    activatedString = ' '.join(str(i) for i in activatedPoints)
    return (activatedString)


if __name__ == '__main__':
    app.run_server(debug=True)
