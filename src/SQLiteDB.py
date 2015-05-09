import sqlite3

class SQLiteDB(EliteDB):
  def __init__(self, fileName):
    super().__init__(self)
    


  def __enter__(self): 
    self.conn = sqlite3.connect(fileName )

  def __exit__(self):
    if self.conn is not None:
      self.conn.close()

  def _createDB(self):
    self.conn.


