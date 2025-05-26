import dash
from dash import html, dcc

# Crear la aplicación Dash
app = dash.Dash(__name__)
app.title = "Hello Railway Dash"

# Layout muy básico
app.layout = html.Div([
    html.H1("¡Hola desde Railway Dash!"),
    html.P("Si ves esto, tu aplicación Dash se ha desplegado correctamente."),
    dcc.Graph(
        id='basic-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'A'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'B'},
            ],
            'layout': {
                'title': 'Gráfico de Prueba'
            }
        }
    )
])

# No hay callbacks
# NO hay if __name__ == "__main__": app.run_server()