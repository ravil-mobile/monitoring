from monitoring.visualization import create_dash_app
from monitoring.db_manager import DbManager
from flask import Flask
from flask import request
from io import StringIO
import pandas as pd
import argparse


cmd = argparse.ArgumentParser()
cmd.add_argument('-c', '--clear', action='store_true', help="clear database")
args = cmd.parse_args()


DbManager.init(args.clear)
app = Flask(__name__)
dash_app = create_dash_app(app)


def make_record(meta, data):
  sha = bytes(meta.loc[0]['git_hash'], 'UTF-8')
  data.set_index('kernel type', inplace=True)

  with DbManager() as db:
    meta_info = {
      'git_hash': sha,
      'branch': meta.loc[0]['branch'],
      'exec_time': meta.loc[0]['exec_time'],
      'hostname': meta.loc[0]['hostname']
    }

    run_info = {
      'git_hash': sha,
      'all_kernels': float(data.loc['all']['HW GFLOPS']),
      'ader': float(data.loc['ader']['HW GFLOPS'])
    }
    db.cursor.execute(f"INSERT INTO runs VALUES (:git_hash, :branch, :exec_time, :hostname)", meta_info)
    db.cursor.execute(f"INSERT INTO hw_flops VALUES (:git_hash, :all_kernels, :ader)", run_info)


@app.route('/post', methods=['POST'])
def update():
  response = app.response_class(status=200, mimetype='application/json')
  try:
    measurements_file = request.files['data']
    measurements = measurements_file.stream.read().decode("UTF8")
    data = pd.read_csv(StringIO(measurements))

    meta_file = request.files['meta']
    meta = meta_file.stream.read().decode("UTF8")
    meta = pd.read_csv(StringIO(meta))
    make_record(meta, data)

  except Exception as err:
    response = app.response_class(status=406,
                                  response=f'Error: {err}',
                                  mimetype='application/json')
  return response


if __name__ == '__main__':
  app.run(debug=True)