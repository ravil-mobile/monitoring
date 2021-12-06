from monitoring.db_manager import DbManager
import dash
from dash import dcc
from dash import html


layout = html.Div([
  html.H1('App1'),
  dcc.Dropdown(
    id='page-1-dropdown',
    options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
    value='LA'
  ),
  html.Div(id='page-1-content'),
  html.Br(),
  dcc.Link('Go to App2', href='/app2'),
  html.Br(),
  dcc.Link('Go back to home', href='/'),
])


def init(app):
  @app.callback(dash.dependencies.Output('page-1-content', 'children'),
                [dash.dependencies.Input('page-1-dropdown', 'value')])
  def page_1_dropdown(value):
    print('hello world')
    with DbManager() as db:
      db.cursor.execute(f"SELECT * FROM runs")
      items = db.cursor.fetchall()
      print(f'num items: {len(items)}')
      for item in items:
        print(item)

    return 'You have selected "{}"'.format(value)
