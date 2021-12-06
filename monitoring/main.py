from visualization import create_dash_app
from flask import Flask
from flask import request
from io import StringIO
import pandas as pd


app = Flask(__name__)
dash_app = create_dash_app(app)


@app.route('/post', methods=['POST'])
def update():
  response = app.response_class(status=200, mimetype='application/json')
  try:
    measurements_file = request.files['data']
    measurements = measurements_file.stream.read().decode("UTF8")
    data_frame = pd.read_csv(StringIO(measurements))
    print(data_frame)

    meta_file = request.files['meta']
    meta = meta_file.stream.read().decode("UTF8")
    meta_frame = pd.read_csv(StringIO(meta))
    print(meta_frame)

  except Exception as err:
    response = app.response_class(status=406,
                                  response=f'Error: {err}',
                                  mimetype='application/json')
  return response


if __name__ == '__main__':
  app.run(debug=True)