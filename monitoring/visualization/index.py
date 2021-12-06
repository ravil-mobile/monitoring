import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from .apps import app1, app2


def create_dash_app(flask_app):
  dash_app = dash.Dash(server=flask_app,
                       name='board',
                       url_base_pathname='/',
                       external_stylesheets=[dbc.themes.FLATLY])
  dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
  ])

  init_callbacks(dash_app)
  return dash_app


index_page = html.Div([
    dcc.Link('Commit View', href='/app1'),
    html.Br(),
    dcc.Link('Open App2', href='/app2'),
])


def init_callbacks(app):
  app1.init(app)
  app2.init(app)

  @app.callback(dash.dependencies.Output('page-content', 'children'),
                [dash.dependencies.Input('url', 'pathname')])
  def display_page(pathname):
    if pathname == '/app1':
      return app1.layout
    elif pathname == '/app2':
      return app2.layout
    else:
      return index_page




