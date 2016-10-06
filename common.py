import MySQLdb
import time

class DB:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="zai1OoRo",
                     db="iot")
        except(AttributeError, MySQLdb.OperationalError) as e:
            time.sleep(5)
            self.connect()
            #raise e

    def query(self, sql, params = ()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
        except(AttributeError, MySQLdb.OperationalError) as e:
            #print 'exception generated during sql connection on query: ', e
            self.__del__()
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
        return cursor

    def insert(self, sql, params = ()):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            self.conn.commit()
        except(AttributeError, MySQLdb.OperationalError) as e:
            #print 'exception generated during sql connection on insert: ', e
            self.__del__()
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
        return cursor

    #def close(self):
    def __del__(self):
        try:
            if self.conn:
                self.conn.close()
                #print 'Closed Database Connection: ' + str(self.conn)
            else:
                #print 'No Database Connection to Close.'
                pass
        except (AttributeError, MySQLdb.OperationalError) as e:
            raise e

#db = DB()
#sql = '''Select * from sensors'''
#for row in db.query(sql).fetchall():
#	print(row)

#sql2 = '''insert into sensors (value, type, location) values (%s, %s, %s)'''
#data = ('40.4', 'temp', 'rpi')
#print(db.query(sql2, data).fetchall())
#db.insert(sql2, data)

#db.close()

