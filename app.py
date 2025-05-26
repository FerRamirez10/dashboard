import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import requests

# Rango de fechas permitido
min_date = pd.to_datetime("2025-01-01").date()
max_date = pd.to_datetime("2027-12-01").date()

# Crear app
app = dash.Dash(__name__)
app.title = "Predicción de Ventas"

# Estilos y fuente
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
        {%metas%}
<title>{%title%}</title>
        {%favicon%}
        {%css%}
<style>
            html, body {
                margin: 0;
                padding: 0;
                background-color: #991111;
                color: #f5f5f5;
                height: 100%;
                font-family: 'Poppins', sans-serif;
            }
</style>
</head>
<body>
        {%app_entry%}
<footer>
            {%config%}
            {%scripts%}
            {%renderer%}
</footer>
</body>
</html>
'''

# Layout
app.layout = html.Div(
    style={
        'backgroundColor': '#991111',
        'color': '#f5f5f5',
        'font-family': "'Poppins', sans-serif",
        'padding': '30px',
        'maxWidth': '950px',
        'margin': 'auto',
        'minHeight': '100vh'
    },
    children=[
        html.Link(
            href='https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap',
            rel='stylesheet'
        ),

        html.H1(
            "📈 Predicción de Ventas Cuajo Líquido x 500 cc",
            style={
                'text-align': 'center',
                'color': '#ffdd00',
                'font-size': '38px',
                'margin-bottom': '40px'
            }
        ),

        html.Div([
            html.Label(
                "Selecciona una fecha para obtener la predicción:",
                style={'font-size': '18px', 'font-weight': 'bold'}
            ),
            html.Div([
                dcc.DatePickerSingle(
                    id='date-picker',
                    min_date_allowed=min_date,
                    max_date_allowed=max_date,
                    initial_visible_month=min_date,
                    date=min_date,
                    display_format='DD MMMM YYYY',
                    style={
                        'background-color': '#cc3333',
                        'color': '#f5f5f5',
                        'border': '1px solid #ffdd00',
                        'border-radius': '6px',
                        'padding': '6px'
                    }
                ),
                html.Button("Obtener Predicción", id='submit-button', n_clicks=0, style={
                    'padding': '10px 25px',
                    'font-size': '17px',
                    'background-color': '#ffdd00',
                    'color': '#1e1e1e',
                    'border': '2px solid #ffdd00',
                    'border-radius': '6px',
                    'cursor': 'pointer',
                    'font-weight': 'bold',
                    'margin-left': '15px'
                })
            ], style={'margin-top': '10px'}),

            html.Div(id='prediction-output', style={
                'margin-top': '25px',
                'padding': '20px',
                'background-color': '#b22222',
                'border-left': '8px solid #ffdd00',
                'border-radius': '6px',
                'box-shadow': '0px 0px 8px rgba(0,0,0,0.2)',
                'font-size': '18px',
                'color': '#ffffff',
                'whiteSpace': 'pre-line'
            })
        ], style={
            'text-align': 'center',
            'margin-bottom': '50px',
            'background-color': '#b22222',
            'padding': '25px',
            'border-radius': '10px',
            'box-shadow': '0px 0px 12px rgba(0,0,0,0.2)',
            'border': '2px solid #790000'
        }),

        dcc.Graph(id='forecast-graph'),

        html.Div([
            html.H2("📊 Estadísticas Descriptivas", style={
                'color': '#ffdd00',
                'margin-bottom': '20px'
            }),
            html.Div(id='stats-table', style={
                'overflowX': 'auto',
                'padding': '15px',
                'background-color': '#b22222',
                'border-radius': '10px',
                'box-shadow': '0px 0px 12px rgba(0,0,0,0.2)',
                'border': '2px solid #790000',
                'margin-top': '20px'
            }),
            dcc.Graph(id='stats-graph'),
            html.Div(id='stats-analysis', style={
                'margin-top': '20px',
                'font-size': '16px',
                'color': '#ffffff'
            })
        ]),

        html.Div([
            html.H3("🧪 Proyecto de Predicción de Ventas", style={
                'color': '#ffdd00',
                'font-size': '22px'
            }),
            html.P("Este trabajo fue desarrollado por Santiago Del Rio para TECNO ALIMENTARIA LTDA.", style={
                'font-size': '16px'
            }),
            html.P("Rango de predicción disponible: Enero 2025 - Diciembre 2027", style={
                'font-size': '16px',
                'color': '#f0f0f0'
            })
        ], style={'text-align': 'center', 'margin-top': '50px'})
    ]
)

# Callback para predicción
@app.callback(
    Output('prediction-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('date-picker', 'date')
)
def obtener_prediccion(n_clicks, fecha):
    if n_clicks > 0 and fecha:
        try:
            payload = {"fechas": [fecha]}
            response = requests.post("https://analitica-production.up.railway.app/predict", json=payload)
            if response.status_code == 200:
                data = response.json()
                pred = data.get("predicciones", [None])[0]

                if pred and all(k in pred for k in ['yhat', 'yhat_lower', 'yhat_upper']):
                    return (
                        f"📅 Predicción para {fecha}:\n"
                        f"🔹 Estimado: {pred['yhat']:,.2f} unidades\n"
                        f"🔻 Límite inferior: {pred['yhat_lower']:,.2f}\n"
                        f"🔺 Límite superior: {pred['yhat_upper']:,.2f}"
                    )
                else:
                    return "⚠️ La respuesta de la API no contiene los datos esperados."
            else:
                return f"❌ Error de la API: {response.status_code}"
        except Exception as e:
            return f"❌ Error al conectar con la API: {str(e)}"
    return ""

# Callback para cargar gráfico y estadísticas
@app.callback(
    Output('forecast-graph', 'figure'),
    Output('stats-table', 'children'),
    Output('stats-graph', 'figure'),
    Output('stats-analysis', 'children'),
    Input('submit-button', 'n_clicks')
)
def cargar_datos(n_clicks):
    try:
        forecast_response = requests.post("https://analitica-production.up.railway.app/predict", json={"fechas": pd.date_range(min_date, max_date, freq='MS').strftime("%Y-%m-%d").tolist()})
        stats_response = requests.get("https://analitica-production.up.railway.app/estadisticas")

        forecast = pd.DataFrame(forecast_response.json()['predicciones'])
        stats = pd.DataFrame(stats_response.json())

        # Filtrar columnas útiles
        stats = stats[[col for col in stats.columns if 'var' not in col.lower()]]

        fig = {
            'data': [
                go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Predicción', line=dict(color='#ffdd00', width=3)),
                go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill='tonexty', fillcolor='rgba(255, 221, 0, 0.15)', line=dict(color='rgba(255, 221, 0, 0.2)'), name='Intervalo Inferior'),
                go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill='tonexty', fillcolor='rgba(255, 221, 0, 0.1)', line=dict(color='rgba(255, 221, 0, 0.2)'), name='Intervalo Superior')
            ],
            'layout': go.Layout(
                title='Predicción Mensual (2025 - 2027)',
                xaxis={'title': 'Fecha', 'color': '#f5f5f5'},
                yaxis={'title': 'Ventas Estimadas', 'color': '#f5f5f5'},
                plot_bgcolor='#991111',
                paper_bgcolor='#991111',
                font={'color': '#f5f5f5'},
                legend=dict(font=dict(color='#f5f5f5'))
            )
        }

        stats_html = html.Table([
            html.Thead(html.Tr([html.Th(col) for col in stats.columns])),
            html.Tbody([
                html.Tr([html.Td(stats.iloc[0][col]) for col in stats.columns])
            ])
        ], style={'width': '100%', 'border-collapse': 'collapse', 'text-align': 'center'})

        # Gráfico de estadísticas (sin varianza)
        numeric_stats = stats.select_dtypes(include=['number']).iloc[0]
        stats_bar = go.Figure()
        stats_bar.add_trace(go.Bar(
            x=numeric_stats.index,
            y=numeric_stats.values,
            text=[
                f'{float(v):,.2f}' if isinstance(v, (int, float)) or str(v).replace(".", "", 1).isdigit() else str(v)
                for v in numeric_stats.values
            ],
            textposition='auto',
            marker_color='#ffdd00'
        ))
        stats_bar.update_layout(
            title="Resumen Estadístico",
            plot_bgcolor='#991111',
            paper_bgcolor='#991111',
            font=dict(color='#f5f5f5'),
            xaxis=dict(title='Métrica'),
            yaxis=dict(title='Valor')
        )

        # Texto genérico de análisis
        analysis_text = (
            "El comportamiento general de las predicciones muestra una media y mediana cercanas, lo cual indica una distribución relativamente equilibrada. "
            "Los valores máximos y mínimos ayudan a establecer los límites esperados de las ventas estimadas durante el periodo considerado."
        )

        return fig, stats_html, stats_bar, analysis_text

    except Exception as e:
        return {}, f"❌ Error al cargar datos: {str(e)}", {}, ""


