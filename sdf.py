import datetime
from datetime import date
import calendar
import tkinter as tk
from tkinter import BOTH, END
import MySQLdb

from collections import defaultdict

# dodwj = {} #dictionary of days with jobs
dodwj = defaultdict(dict)

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
    def __init__(self, name, year, month, day, hour, minute, second, job_id):
        self.name = name
        self.timeReq = 3600  # in seconds, defaults to 1h
#       doBy is the date of occurence
#       
#                                     year  m  d   h   m   s   mics  tz
        self.doBy = datetime.datetime(year, month, day, hour, minute, second, 0, None)
        # self.doBy = datetime.datetime(2016, 1, 27, 20, 46, 43, 0, None)
        self.job_id = job_id

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

        self.outstr = self.name + " "
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
    INSERT INTO wt VALUES('laundry','7200', STR_TO_DATE('2016/02/20 20:46:43', '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('something new on same date','8400', STR_TO_DATE('2016/02/27 23:46:43', '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('database project','0', STR_TO_DATE('2016/02/15 08:00:00', '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('paper','18000', STR_TO_DATE('2016/02/08 14:00:00', '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('csc club meeting','3600', STR_TO_DATE('2016/02/08 11:00:00', '%Y/%m/%d %T'), NULL);
    """
    db.query(q)
    db.connection.commit()


def dofotm(): # day of first of this month
    return date(datetime.datetime.today().year, datetime.datetime.today().month, 1).weekday()

def dofotm_specific(y, m): # day of first of a specific month
    return date(y, m, 1).weekday()

def ditm(): # days in this month
    return calendar.monthrange(datetime.datetime.today().year, datetime.datetime.today().month)[1]

def ditm_specific(y, m): # days in this month
    return calendar.monthrange(y, m)[1]

def tf(arg):
    print("button pressed, tf(" + str(arg) + ") invoked")
    joblistbox.delete(0, END)
    for item in dodwj[arg]:
        joblistbox.insert(END, dodwj[arg][item])
    #print(dodwj[arg])

def calpop():
# populates a grid with the days of the month in a button format
    gridindex = dofotm() + 1
    currday = 1
    daywidth = 32 # 32 pixels width
    calwidth = daywidth * 7 # 7 days in a week
    #calheight = daywidth * 5 # max 5 weeks in a month?

    
    calwidth = 2 # temp calwidth, 2 is width based on characters
    for x in range(0, 9): # will just break after done? max=99 is ok?
        if (currday == ditm()):
            break
        for y in range(0, 7):
            y = gridindex
            mnth = datetime.datetime.today().month
            binddate = datetime.date(2016, mnth, currday)
            btn1 = tk.Button(root, width=calwidth, text=currday, command=lambda j=binddate: tf(j))
            btn1.grid(row=x, column=y)
            if (currday == ditm()):
                break
            currday = currday + 1
            gridindex = gridindex + 1
            if (gridindex == 7):
                gridindex = 0
                break
    

def refreshjoblist():
    q="""
    SELECT * from wt;
    """
    dbdata = db.query(q)

    for item in dbdata:
        # parse doby from db into python datetime format
        datetimestr = str(item['doby'])
        yearstr = int(datetimestr[0:4])
        monthstr = int(datetimestr[5:7])
        daystr = int(datetimestr[8:10])
        hourstr = int(datetimestr[11:13])
        minutestr = int(datetimestr[14:16])
        secondstr = int(datetimestr[17:19])
        joblist.append(Job(item['name'], yearstr, monthstr, daystr, hourstr, minutestr, secondstr, item['job_id']))

    matches = 0 # dont even need this anymore

    for item in joblist:
        if (item.doBy.date() in doBylist):
            matches = matches + 1
        else:
            doBylist.append(item.doBy.date())
    
    
    newlist = [x for x in doBylist if x == joblist[0].doBy.date()]
    print("sdf " + str(newlist)) # newlist contains unique dates?
    i = 1
    global dodwj
    for item in joblist:
        if(item.doBy.date() in dodwj):
            i = i + 1
            dodwj[item.doBy.date()][i] = item.name # dict can override
        else:
            dodwj[item.doBy.date()][i] = item.name # dict can override
        i = 1
    print("printing dodwj:")
    print(dodwj)
    # - get the dates from doBylist (this contains unique dates)
    # - traverse list of jobs. create new array for first occurence of
    #   a date. add job to that date. for other jobs on that date, add 
    #   them to the created array

    # - when populating cal, change color when there is event
    # 

    print("#########################")
    print("refreshed job DB. items: ")
    print("#########################")
    for item in joblist:
        print(item)


if __name__ == "__main__":
    db = Database() # custom database class (mysql)

    initdbclass()
    joblist = []
    doBylist = []
    refreshjoblist()

    c = calendar
    year = 2016
    month = 1

    #db.additem('wt', 'newdbitem', '3600')

    ################
    # tkinter stuff
    root = tk.Tk()
    root.title("tkinter window")
    test1 = tk.Label(root, text = "thistext")

#    f = tk.Frame(root, height=32, width=32)
#    f.pack_propagate(0)
#    f.pack()

#    btn1 = tk.Button(f, text = "a button", command=tf)
#    btn1.pack(fill=BOTH, expand=1)

    joblistbox = tk.Listbox(root, width=35, height=5)
    for item in joblist:
        joblistbox.insert(END, item.name) # insert in listbox

    joblistbox.grid(row=5, columnspan=7) # figure this out

    calpop()

    root.mainloop()
