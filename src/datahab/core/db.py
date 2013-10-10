import psycopg2
import re

'''
@author: anant bhardwaj
@date: Oct 3, 2013

datahub connection manager
'''

class Connection:
  def __init__(self, user="postgres", password="postgres", host='localhost', port=5432, db_name='postgres'):
    self.connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=db_name)

  def __del__(self):
    self.connection.close()

  def execute_sql(self, query, params=None, commit=False):
    tuples = None
    c = self.connection.cursor()
    c.execute(query, params)
    try:
      tuples = c.fetchall()
    except:
      pass
    c.close()
    if commit:
      self.connection.commit()
    return tuples

  def show_databases(self):
    s = "SELECT datname FROM pg_catalog.pg_database WHERE NOT datistemplate"
    return self.execute_sql(s)

  def show_tables(self):
    s = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    return self.execute_sql(s);

  def create_database(self, db_name):   
    self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    c = self.connection.cursor()
    s = "CREATE DATABASE %s" % (db_name)
    c.execute(s, None)

  def drop_database(self, db_name):   
    self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    c = self.connection.cursor()
    s = "DROP DATABASE %s" % (db_name)
    c.execute(s, None)

  def close(self):    
    self.connection.close()


if __name__ == '__main__':
  con = Connection()
  print  con.show_databases()
  con = Connection(db_name='datahub')
  print con.show_tables()
  con.execute_sql('create table test(id integer, name varchar(20))')
  print con.show_tables()
  con = Connection(db_name='datahub')
  print con.show_tables()
