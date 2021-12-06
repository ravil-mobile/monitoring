from monitoring.db_manager import DbManager
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# Note: prefix all widget ids with `cv-`


empty_frame = pd.DataFrame({
    "HW GFLOPs": [],
    "kernels": []
})
fig = px.bar(empty_frame, x="kernels", y="HW GFLOPs",)


layout = html.Div([
  html.H3('Commit View', style={'textAlign': 'center'}),
  dbc.Row([
    dbc.Col(
      dbc.Row([
        dcc.Graph(
          id='cv-main-plot-id',
          figure=fig,
        ),
      ])
    ),

    dbc.Col(
      dbc.Row([
        html.H5('Select Commit:'),
        dcc.Dropdown(
          id='cv-commits-dropdown-id',
          options=[{'label': i, 'value': i} for i in ['none']],
          value='none'
        ),
      ])
    ),
  ]),
  html.Div(id='cv-selected-commit-id'),
  html.Br(),
  dcc.Link('Go to App2', href='/app2'),
  html.Br(),
  dcc.Link('Go back to home', href='/'),
], id='cv-commit-view-main-id')


DISPALY_SHA_LENGTH = 9


def init(app):
  @app.callback(dash.dependencies.Output('cv-commits-dropdown-id', 'options'),
                [dash.dependencies.Input('cv-commit-view-main-id', 'value')])
  def fill_commits_dropdown(value):
    with DbManager() as db:
      db.cursor.execute(f"SELECT git_hash FROM runs")
      sha_values = db.cursor.fetchall()

    sha_values = [sha[0].decode("utf-8") for sha in sha_values]
    options_list = []
    for sha in sha_values:
      options_list.append({'label': sha[:DISPALY_SHA_LENGTH], 'value': sha})

    return options_list


  @app.callback(dash.dependencies.Output('cv-selected-commit-id', 'children'),
                [dash.dependencies.Input('cv-commits-dropdown-id', 'value')])
  def display_selected_commit(value):
    return f'Commit: {value[:DISPALY_SHA_LENGTH]}'


  @app.callback(dash.dependencies.Output('cv-main-plot-id', 'figure'),
                [dash.dependencies.Input('cv-commits-dropdown-id', 'value')])
  def update_plot(value):
    if value == 'none':
      return empty_frame

    sha = bytes(value, 'UTF-8')
    with DbManager() as db:
      db.cursor.execute(f"SELECT * FROM hw_flops WHERE git_hash = :sha", {'sha': sha})
      flops = db.cursor.fetchall()
      col_name_list = [tuple[0] for tuple in db.cursor.description]

    # Note: needs to skip the primary key which is the fist entry
    frame = pd.DataFrame({
      "HW GFLOPs": [item for item in flops[0][1:]],
      "kernels": [name.upper().replace('_', ' ') for name in col_name_list[1:]]
    })

    fig = px.bar(frame, x="kernels", y="HW GFLOPs")
    fig.update_layout(xaxis=go.layout.XAxis(tickangle=0))
    return fig
