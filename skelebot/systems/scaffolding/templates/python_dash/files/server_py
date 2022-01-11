from dash import html
from dash.dependencies import Input, Output, State

def get_graph_output(text_input):
    return {
        'layout': {
            'title': text_input
        },
        'data': [
            {'x': [1, 2, 3], 'y': [4, 1, 2],
                'type': 'bar', 'name': 'Ford'},
            {'x': [1, 2, 3], 'y': [2, 4, 5],
                'type': 'bar', 'name': 'Mini'},
        ]
    }

def get_text_output(dropdown_input):
    return html.H3(dropdown_input)
