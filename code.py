import dash
from dash import dcc, html
import dash_leaflet as dl
import yfinance as yf
from dash.dependencies import Input, Output
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
from plotly.subplots import make_subplots
import plotly.graph_objects as go


BLACK = '#212121'
WHITE = '#F9F9F9'


# Fonction pour obtenir les coordonnées géographiques
def get_coordinates(address, city, country):
    api_key = ""  # Remplacez par votre clé API OpenCageData
    url = f"https://api.opencagedata.com/geocode/v1/json?q={address}, {city}, {country}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        if data["results"]:
            latitude = data["results"][0]["geometry"]["lat"]
            longitude = data["results"][0]["geometry"]["lng"]
            return latitude, longitude
        else:
            pass
    else:
        pass
    
    return None, None

# Fonction pour obtenir la valeur d'un champ dans un dictionnaire formatée avec un nombre de décimales donné
def get_value_dictionnary(df,key, round_number = 0):
    if key in df:
        if isinstance(df[key], (int, float, complex)):
            formatted = "{:,." + str(round_number) + "f}"
            return formatted.format(df[key])
        else:
            return df[key]
    else:
        return "N/A"

# Fonction pour obtenir la date formatée à partir d'un timestamp
def get_date(df,key):
    if key in df:
        return str(datetime.utcfromtimestamp(df[key]).strftime("%Y-%m-%d"))
    else:
        return "N/A"
    
# Fonction pour obtenir le symbole de la devise
def get_currency_symbol(currency):
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CAD": "C$",
        "AUD": "A$",
        "CHF": "Fr.",
        "CNY": "¥",
        "SEK": "kr",
        "NZD": "NZ$",
        "KRW": "₩",
        "NOK": "kr",
        "MXN": "Mex$",
        "SGD": "S$",
        "HKD": "HK$",
        "INR": "₹",
        "BRL": "R$",
        "ZAR": "R",
        "RUB": "₽",
        "TRY": "₺",
    }

    if currency in currency_symbols:
        return currency_symbols[currency]
    else:
        return "N/A"

    
# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Définition des éléments de l'interface utilisateur

# En-tête
header = html.Header(
        style={
            'color': 'white', 
            'text-align': 'center',
            'font-family': 'Verdana', 
            'font-size': '28px',
            'font-style': 'italic'},
    children=[
    html.P("Data Analysis")
    ])


# Section de recherche
recherche = html.Section(
    style={'text-align': 'center'},
    children=[
        html.P('Enter your ticker :', style={'color': 'white'}),
        dcc.Input(
            id='input',
            type='search',
            value='AAPL',
            style={'font-size': '28px', 'font-family': 'Verdana'}
        ),
        html.Div(id='output')
        ]
    )

# Section du graphique
graphique_viz = html.Div(
    style={
        "width": "60%",
        'height' : '100%',
        'backgroundColor': BLACK,
        'margin' : '0px 5px'},
    children=[
        html.H1("Financial chart", style={'color': 'white', 'text-align': 'center'}),
        dcc.DatePickerRange(style={
            "width": "100%",
            'text-align': 'center',
            'margin' : '5px'},
            id='my-date-picker-range',
            min_date_allowed=date(1900, 1, 1),
            max_date_allowed=datetime.today().date(),
            initial_visible_month=datetime.today().date(),
            start_date=datetime.today().date() - relativedelta(years=1),
            end_date=datetime.today().date() - timedelta(days=1)
        ),
        html.Div(id="output-graph"),
        ]
    )

# Section de la carte
map_viz = html.Div(
    style={
        "width": "40%",
        'height' : '100%',
        'backgroundColor': BLACK},
    children=[
            html.Div(id="output-map"),
            ]
    )

# Section principale avec le graphique et la carte
visuel = html.Section(
    style={
        'height': '800px', 
        'backgroundColor': BLACK,
        'display': 'flex',
        'justify-content': 'space-between'},
    children=[
        graphique_viz,
        map_viz,
        ]
    )

# Section d'informations supplémentaires
texte_complementaire = html.Section(
    style={ 
        'backgroundColor': BLACK},
    children=[
        html.Div(id="output-info"),
        ]
    )

# Pied de page
footer = html.Footer(style={'color': 'white', 'text-align': 'center'},
            children=[
                html.Div(
                    className="container",
                    children=[
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-md-6",
                                    children=[
                                        html.H3("About me"),
                                        html.P("I am a student passionate about finance and big data, looking to combine these two exciting fields."),
                                        html.P("My academic background allows me to develop a solid expertise in financial analysis while exploiting the opportunities offered by the vast amounts of data available."),
                                        html.P("I am determined to use my skills in finance and big data to bring accurate and innovative insights to the world of finance.")
                                    ],
                                ),
                                html.Div(
                                    className="col-md-6",
                                    children=[
                                        html.H3("Link"),
                                        html.Div(
                                            html.A(
                                                html.Img(src="https://logos-marques.com/wp-content/uploads/2021/03/GitHub-Logo.png", 
                                                         height="100px"), 
                                                href="https://github.com/PxChamp", 
                                                target="_blank" ),   
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                html.Div(
                    className="container",
                    children=[
                        html.Hr(),
                        html.P("© 2023 PxChamp."),
                    ],
                ),
            ]
        )


# Mise en page de l'application Dash
app.layout = html.Div(
    style={
        'backgroundColor': BLACK,  
        'margin' : '-10px',
        'border': 'none',  
        'padding': '20px' 
    },
    children=[
        header,
        recherche,
        visuel,
        texte_complementaire,
        footer,
    ]
)



# Callback pour mettre à jour les éléments de l'interface utilisateur en fonction des entrées de l'utilisateur
@app.callback(
    Output(component_id="output-graph", component_property="children"),
    Output(component_id="output-info", component_property="children"),
    Output(component_id="output-map", component_property="children"),
    [Input(component_id="input", component_property="value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')]
)

def update(input_data, start_date, end_date):
    # Récupérer les données financières à partir de yfinance
    data = yf.download(input_data, start=start_date, end=end_date)
    ticker_info = yf.Ticker(input_data).info
    
    # Création du graphique avec Plotly
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        subplot_titles=("Price", "Volume"), 
                        vertical_spacing=0.08)

    # Valeur fermée
    fig.add_trace(
        go.Scatter(
            x=data.index, 
            y=data["Adj Close"],
            mode="lines",
            line={"color": "blue"},
            name=input_data
        ),
        row=1, col=1
    )
    
    # Valeur haute
    fig.add_trace(
        go.Scatter(
            x=data.index, 
            y=data["High"],
            mode="lines",
            line={"color": "green","dash": "dot"},
            name="High"
        ),
        row=1, col=1
    )
    
    # Valeur basse
    fig.add_trace(
        go.Scatter(
            x=data.index, 
            y=data["Low"],
            mode="lines",
            line={"color": "red","dash": "dot"},
            name="Low"
        ),
        row=1, col=1
    )
    
    # Volume échangé
    fig.add_trace(
        go.Bar(
            x=data.index, 
            y=data["Volume"],
            name="Volume",
            marker={"color": "skyblue"}
        ),
        row=2, col=1
    )

    # Grille
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='gray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='gray')

    # Ajout du titre
    fig.update_layout(
        plot_bgcolor="white",
        title={
            'text' : f"Price chart of {ticker_info['shortName']}",
            'x' : 0.5,
            'xanchor': 'center'
               },
        autosize=True,
    )

    financial_information_first = html.Div(style={
        "width": "33%",
        'height' : '100%',
        'backgroundColor': BLACK},
    children=[
        html.P('52 Week Change : '+ get_value_dictionnary(ticker_info,'52WeekChange',7)),
        html.P('Average Volume : '+ get_value_dictionnary(ticker_info,'averageVolume')),
        html.P('Beta : '+ get_value_dictionnary(ticker_info,'beta',6)),
        html.P('Currency : '+ get_value_dictionnary(ticker_info,'currency')),
        html.P('Current Prise : '+ get_value_dictionnary(ticker_info,'currentPrice',2) + get_currency_symbol(ticker_info['currency']))
        ])
    
    financial_information_second = html.Div(style={
        "width": "33%",
        'height' : '100%',
        'backgroundColor': BLACK},
    children=[
        html.P('Day High : '+ get_value_dictionnary(ticker_info,'dayHigh',2)+ get_currency_symbol(ticker_info['currency'])),
        html.P('Day Low : '+ get_value_dictionnary(ticker_info,'dayLow',2)+ get_currency_symbol(ticker_info['currency'])),
        html.P('Dividend Rate : '+ get_value_dictionnary(ticker_info,'dividendRate',2)),
        html.P('Dividend Yield : '+ get_value_dictionnary(ticker_info,'dividendYield',4)),
        html.P('Entreprise Revenue : '+ get_value_dictionnary(ticker_info,'enterpriseToRevenue',3)+ get_currency_symbol(ticker_info['currency']))
        ])
    
    financial_information_third = html.Div(style={
        "width": "33%",
        'height' : '100%',
        'backgroundColor': BLACK},
    children=[
        html.P('Ex-Dividend date : '+ get_date(ticker_info,'exDividendDate')),
        html.P('Market cap : '+ get_value_dictionnary(ticker_info,'marketCap')+ get_currency_symbol(ticker_info['currency'])),
        html.P('Open : '+ get_value_dictionnary(ticker_info,'open',2)+ get_currency_symbol(ticker_info['currency'])),
        html.P('Previous close : '+ get_value_dictionnary(ticker_info,'previousClose',2)+ get_currency_symbol(ticker_info['currency'])),
        html.P('Return on equity : '+ get_value_dictionnary(ticker_info,'returnOnEquity',7)+ get_currency_symbol(ticker_info['currency']))
        ])


    financial_information = html.Div(style={       
        'backgroundColor': BLACK,
        'color' : 'white',
        'display': 'flex',
        'justify-content': 'space-between'},
    children=[
        financial_information_first,
        financial_information_second,
        financial_information_third
        ])

    graph = html.Div(
        children=[
            dcc.Graph(figure=fig),
            financial_information,
            ])


     # Informations sur l'entreprise
    if all(key in ticker_info for key in ['shortName', 'longBusinessSummary']):
        about = html.Div(
              style={
                  "width": "50%",
                  'height' : '100%',
                  'margin' : '0px 5px',
                  'backgroundColor': BLACK,
                  },
              children=[
                      html.H1("About " + ticker_info["shortName"] + ":"),
                      html.P(ticker_info["longBusinessSummary"],style={
                          'text-align': 'justify'
                          })])
    else:
        about = html.Div(
              style={
                  "width": "50%",
                  'height' : '100%',
                  'margin' : '0px 5px',
                  'backgroundColor': BLACK,
                  },
              children=[
                      html.P("No information about the entreprise")])
                    
    if 'companyOfficers' in ticker_info:
        if all(key in ticker_info["companyOfficers"][0] for key in ['name', 'title']):
            officer = html.Div(
                  style={
                      "width": "30%",
                      'height' : '100%',
                      'margin' : '0px 5px',
                      'backgroundColor': BLACK,
                      'color' : 'white'},
                  children=[
                    html.H1("List of officers :"),
                    html.Ul(
                    [html.Li(people["name"] + "," + people["title"]) for people in ticker_info["companyOfficers"]]  
                    )])
        else:
            officer = html.Div(
                  style={
                      "width": "30%",
                      'height' : '100%',
                      'margin' : '0px 5px',
                      'backgroundColor': BLACK,
                      'color' : 'white'},
                  children=[
                    html.H1("No officers")])
            
    else:
        officer = html.Div(
              style={
                  "width": "30%",
                  'height' : '100%',
                  'margin' : '0px 5px',
                  'backgroundColor': BLACK,
                  'color' : 'white'},
              children=[
                html.H1("No officers")])
         
    site_info = html.Div(
          style={
              "width": "20%",
              'height' : '100%',
              'backgroundColor': BLACK,},
          children=[
            html.H1("Website :"),
            html.A(ticker_info["website"], href=ticker_info["website"], target="_blank" , style={"color": "Silver"}),
            html.H1("Phone :"),
            html.A(ticker_info["phone"], href="tel:" + ticker_info["phone"], target="_blank" , style={"color": "Silver"})
            ])

    info = html.Section(
        style={        
            'backgroundColor': BLACK,
            'color' : 'white',
            'display': 'flex',
            'justify-content': 'space-between'},
        children=[
            about,
            officer,
            site_info,
            ]
        )
        
    coordinates = get_coordinates(ticker_info['address1'], ticker_info['city'], ticker_info['country'])
    mapping = html.Div([
        html.H1("Location", style={'color': 'white', 'text-align': 'center'}),
        dl.Map(style={'height': '700px', 'vertical-align': 'bottom', "border-radius": "10px", 'margin' : '0px 5px'}, center=coordinates, zoom=12, children=[
            dl.TileLayer(),
            dl.Marker(position=coordinates, children=[
                dl.Tooltip(ticker_info["shortName"]),
                dl.Popup([
                    html.H1(ticker_info["shortName"]),
                    html.P(ticker_info['address1'] + ", " + ticker_info['zip'] + " " + ticker_info['city'] +", " + ticker_info['country'])
                ])
            ])
        ])
    ],)
    return graph, info, mapping

if __name__ == '__main__':
    app.run_server(port=8888)
    #app.run_server()