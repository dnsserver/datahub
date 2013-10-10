import sys
sys.path.append('./gen-py')

from core.db import *

from datahub import DataHub
from datahub.constants import *
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 9, 2013

DataHub Server
'''

class DataHubHandler:
  def __init__(self):
    self.con = Connection()

  def get_version(self):
    return VERSION

  def create_database(self, db_name):
    try:
      self.con.create_database(db_name)
      return True

    except:
      return False

  def drop_database(self, db_name):
    try:
      self.con.drop_database(db_name)
      return True

    except:
      return False

  def show_databases(self):
    try:
      return str(self.con.show_databases())

    except Exception, e:
      return str(e)

  def show_tables(self, db_name):
    try:
      con = Connection(db_name=db_name)
      return str(con.show_tables())

    except Exception, e:
      return str(e)

  def execute_sql(self, db_name, query, params=None, commit=False):
    try:
      con = Connection(db_name=db_name)
      return str(con.execute_sql(query, params, commit))

    except Exception, e:
      return str(e)



handler = DataHubHandler()
  
processor = DataHub.Processor(handler)
transport = TSocket.TServerSocket('localhost', 9000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

print 'Starting DataHub Server'
server.serve()