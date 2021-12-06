import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})


fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


layout = html.Div([
  html.H1('App 2'),
  dcc.RadioItems(
    id='page-2-radios',
    options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
    value='Orange'
  ),
  html.Div(id='page-2-content'),
  html.Br(),
  dcc.Link('Go to App1', href='/app1'),
  html.Br(),
  dcc.Link('Go back to home', href='/')
])


def init(app):
  @app.callback(dash.dependencies.Output('page-2-content', 'children'),
                [dash.dependencies.Input('page-2-radios', 'value')])
  def page_2_radios(value):
    return 'You have selected "{}"'.format(value)