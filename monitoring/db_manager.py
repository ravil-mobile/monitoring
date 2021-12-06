import os
import sqlite3


class DbManager:
  LOCATION=f'{os.path.abspath(os.getcwd())}/data.db'

  @staticmethod
  def init(clear=False):
    if clear and os.path.exists(DbManager.LOCATION):
      os.remove(DbManager.LOCATION)

    with sqlite3.connect(f'{DbManager.LOCATION}') as conn:
      curs = conn.cursor()
      try:
        curs.execute("SELECT * FROM runs")
      except sqlite3.OperationalError:
        curs.execute("""CREATE TABLE runs (
                        git_hash BINARY(32) NOT NULL,
                        branch TEXT,
                        exec_time TEXT,
                        hostname TEXT,
                        PRIMARY KEY (git_hash)
                     )""")

      try:
        curs.execute("SELECT * FROM hw_flops")
      except sqlite3.OperationalError:
        curs.execute("""CREATE TABLE hw_flops (
                        git_hash BINARY(32) NOT NULL,
                        all_kernels FLOAT,
                        ader FLOAT,
                        FOREIGN KEY (git_hash) REFERENCES runs(git_hash)
                     )""")
      print('DbManager: databased initialized...')

  def __init__(self):
    self.conn = None
    self.cursor = None

  def __enter__(self):
    self.conn = sqlite3.connect(f'{DbManager.LOCATION}')
    self.cursor = self.conn.cursor()
    return self

  def __exit__(self, exception_type, exception_val, trace):
    try:
       self.conn.commit()
       self.cursor.close()
       self.conn.close()
    except AttributeError:
       print ('Not closable.')
       return True
