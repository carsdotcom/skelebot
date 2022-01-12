from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from config import PORT, DEBUG
from server import get_graph_output, get_text_output

app = Dash(__name__)

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Tab One', children=[
            html.H1(children="Tab One Title"),
            html.Label("Chart Title"),
            dcc.Input(id='text-input', value='', type='text'),
            html.Br(),
            html.Button(id='submit-button-one', n_clicks=0, children='Submit'),
            html.Br(),
            dcc.Graph(id='output-one')
        ]),
        dcc.Tab(label='Tab Two', children=[
            html.H1(children="Tab Two Title"),
            html.Label("Select Make"),
            dcc.Dropdown(id='dropdown-input', value='ford',
                options=[
                    {'label': 'Ford', 'value': 'ford'},
                    {'label': 'Mini', 'value': 'mini'},
                    {'label': 'Mazda', 'value': 'mazda'}
                ]
            ),
            html.Br(),
            html.Button(id='submit-button-two', n_clicks=0, children='Submit'),
            html.Br(),
            html.Div(id='output-two')
        ])
    ])
])

@app.callback(Output('output-one', 'figure'),
              [Input('submit-button-one', 'n_clicks')],
              [State('text-input', 'value')])
def graph_output(n_clicks, text_input):
    return get_graph_output(text_input)

@app.callback(Output('output-two', 'children'),
              [Input('submit-button-two', 'n_clicks')],
              [State('dropdown-input', 'value')])
def text_output(n_clicks, dropdown_input):
    return get_text_output(dropdown_input)

if __name__ == '__main__':
    app.run_server(debug=DEBUG, host="0.0.0.0", port=PORT)
