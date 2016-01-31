import datetime
import calendar
import tkinter as tk
import MySQLdb

class Database:

    host    = "localhost"
    user    = "root"
    passwd  = "asdf"
    db      = "test"

    def __init__(self):
        self.connection = MySQLdb.connect( host = self.host,
                                           user = self.user,
                                           passwd = self.passwd,
                                           db = self.db )

    def query(self, q):
        cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
        cursor.execute(q)


        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

    def additem(self, table, name, time):
        time = str(time)
        q = "INSERT INTO " + \
            table + " VALUES ('" + \
            name + "', '" + \
            time + "', NULL);"

        self.query(q)
        # db.connection.commit()

    def delitem_byname(self, name):
        pass

class Job:
    def __init__(self, name, year, month, day, hour, minute, second):
        self.name = name
        self.timeReq = 3600  # in seconds, defaults to 1h
#       doBy is the date of occurence
#       
#       doBy can be either the time to deadline or the time to start (if event)
#                                     year  m  d   h   m   s   mics  tz
        self.doBy = datetime.datetime(year, month, day, hour, minute, second, 0, None)
        # self.doBy = datetime.datetime(2016, 1, 27, 20, 46, 43, 0, None)

#   time left (calculated from current time)
    def timeLeft(self):

        self.timeUntil = self.doBy - datetime.datetime.today()
        return self.timeUntil

# time left (calculatd from a specific time)
    def timeLeftFromTime(self, year, month, day, hour, minute, second, microsecond, tzinfo):
        self.timeUntil = self.doBy - \
                datetime.datetime.today(year, month, day, hour, minute, second, microsecond, tzinfo)
        return self.timeUntil

    def __str__(self):
        if (self.name == ''):
            self.name == 'Unspecified'

        self.outstr = "job name: " + self.name + " "
        self.outstr += str(self.doBy.year) + "-"
        self.outstr += str(self.doBy.month) + "-"
        self.outstr += str(self.doBy.day) + " "
        self.outstr += str(self.doBy.hour) + ":"
        self.outstr += str(self.doBy.minute) + ":"
        self.outstr += str(self.doBy.second) + ":"
        self.outstr += str(self.doBy.microsecond) + " "
        self.outstr += str(self.doBy.tzinfo)

        return self.outstr


#####################################
def initdbclass():
    q = "DELETE FROM wt" # clear table before doing anything
    db.query(q)

    q = """
    INSERT INTO wt VALUES('laundry','7200', STR_TO_DATE('2016/01/27 20:46:43', '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('database project','0', STR_TO_DATE('2016/01/30 08:00:00', '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('paper','18000', STR_TO_DATE('2016/02/08 14:00:00', '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('csc club meeting','3600', STR_TO_DATE('2016/02/06 11:00:00', '%Y/%m/%d %T'), NULL);
    """
    db.query(q)
    db.connection.commit()

    # INSERT INTO wt VALUES('2nd','7200', '2016-01-27-20-46-41', NULL);
    #INSERT INTO wt VALUES ('database project','0', NULL);
    #INSERT INTO wt VALUES ('paper for a class','18000', NULL);
    #INSERT INTO wt VALUES ('csc club meeting','3600', NULL);

def refreshjoblist():
    q="""
    SELECT * from wt;
    """
    dbdata = db.query(q)

    joblist = []
    for item in dbdata:
        # parse doby from db into python datetime format
        # 0123456789012345678
        # 2016-01-27 20:46:43
        datetimestr = str(item['doby'])
        yearstr = int(datetimestr[0:4])
        monthstr = int(datetimestr[5:7]    )
        daystr = int(datetimestr[8:10]      )
        hourstr = int(datetimestr[11:13]   )
        minutestr = int(datetimestr[14:16] )
        secondstr = int(datetimestr[17:19] )

        # joblist.append(Job(item['name'], datetimestr)
        joblist.append(Job(item['name'], yearstr, monthstr, daystr, hourstr, minutestr, secondstr))


    print("refreshed job DB. items: ")
    for item in joblist:
        print(item)

if __name__ == "__main__":
    db = Database() # custom database class (mysql)

    initdbclass()
    refreshjoblist()


    #k = Job(db.findalljobs())
    # j = Job('this new job')
    todaysdate = datetime.datetime.today()
    #print('time until ' + str(j.doBy) + ': ' + str(# j.timeLeft()))

    c = calendar
    year = 2016
    month = 1

    #db.additem('wt', 'newdbitem', '3600')

    # str1 = c.prmonth(year, month)
    ################
    # tkinter stuff
    root = tk.Tk()
    root.title("cal")

    # label1 = tk.Label(root, text=str1, font=('courier', 14, 'bold'), bg='yellow')
    # label1.pack(padx=3, pady=5)
    ################
    # root.mainloop()

