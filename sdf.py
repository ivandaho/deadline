import datetime
from datetime import date
import calendar
import tkinter as tk
from tkinter import END
# from tkinter import BOTH
import mysql.connector

from collections import defaultdict

# kivy stuff
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import InstructionGroup, Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
import sys

from kivy.core.window import Window
from kivy.clock import Clock


class CalGame(GridLayout):  # main class
    def kivycalpop(self):
        # same draw method, just in kivy instead of tkinter
        gridindex = dofotm() + 1
        currday = 1
        y = 0
        mnth = datetime.datetime.today().month

        while (currday <= ditm()):
            binddate = datetime.date(2016, mnth, currday)
            if (y < gridindex):
                # add empty widgets to fill grid
                ew = EW()
                self.add_widget(ew)
                y = y + 1
            else:
                self.add_widget(DayBtn(text=str(currday), input=binddate))
                currday = currday + 1

    def makemarks(self):
        for child in self.children:
            # if event(s) found on this daybtn
            # child is DayBtn
            # contains datetime.datetime
            for event in dodwj[child.input]:
                # event is i number, doesnt contain job data
                # job data is in dodwj[child.input][event]

                # add instructon for each event
                child.drawnew(dodwj[child.input][event])

        self.canvas.add(ig1)


class EW(Widget):  # empty widget class

    # TODO: dummy var and method to be consistent with DayBtn class
    input = ObjectProperty

    def drawnew(self, job):
        pass


class DayBtn(Button):  # day button class
    input = ObjectProperty()
    background_color = (1, 1, 1, 1)
    text_size = (100, 100)
    halign = 'right'
    valign = 'top'
    font_size = 32

    def on_release(self):
        ntf(self.input)

    def drawnew(self, job):
        # TODO: pass into function better, maybe dont need job
        #       datetime.datetime in DayBtn
        # doesnt actually draw but only add instrucions.
        ig1.add(Color(1, 1, 0, 0.5))
        ig1.add(Rectangle(size=(self.width-40,
                                self.height-40),
                          pos=(self.x+20,
                               self.y+20)))
        # calculate timereq indicator stuff...
        secwidth = Window.width/7./180000.
        # timeReq width
        trw = job.timeReq*secwidth

        # 0 is sunday, 6 is saturday
        dayindex = job.doBy.weekday() + 1
        if (dayindex == 7):
            dayindex = 0

        # max possible bar width, based on day of the week
        maxtrw = Window.width / 7 * dayindex

        fillx = 20

        fullbars = 0
        topbar = 0
        iteration = 3
        btmbar = 0

        if (trw >= maxtrw):
            # if can't fit
            btmbar = maxtrw
            remaining = trw - maxtrw  # width of remaining trw
            fullbars = int(remaining/Window.width)  # number of full bars
            topbar = remaining - fullbars*Window.width   # width of top bar

            iteration = fullbars + 1    # number of full bars + top bar
            # this is if can't fit.
            # handle btmbar later

            for x in range(1, iteration+1):
                if (x == iteration):
                    # dont draw full bars. draw last(top) bar.
                    ig1.add(Color(1, 1, 0, 0.2))
                    ig1.add(Rectangle(size=(topbar,
                                            self.height-80),
                                      pos=(Window.width-topbar,
                                           self.y+20+Window.height/5.*x)))
                else:
                    # draw full bars
                    ig1.add(Color(1, 1, 0, 0.2))
                    ig1.add(Rectangle(size=(Window.width,
                                            self.height-80),
                                      pos=(0,
                                           self.y+20+Window.height/5.*x)))

        btmbar = trw
        ig1.add(Color(1, 1, 0, 0.2))
        ig1.add(Rectangle(size=(btmbar+fillx,
                                self.height-80),
                          pos=(self.x-btmbar,
                               self.y+20)))


class CalApp(App):

    def delayed(self, dt):
        self.root.makemarks()

    def build(self):
        main = CalGame(cols=7)

        with main.canvas:
            Rectangle(pos=main.pos, size=Window.size)

        main.kivycalpop()
        Clock.schedule_once(self.delayed, 0.5)  # TODO: refine delay
        return main

# dodwj = {} #dictionary of days with jobs
dodwj = defaultdict(dict)
ig1 = InstructionGroup()


class Database:

    host = "localhost"
    user = "root"
    passwd = "asdf"
    db = "test"

    def __init__(self):
        self.cnx = mysql.connector.connect(host=self.host,
                                           user=self.user,
                                           passwd=self.passwd,
                                           db=self.db)

    def query(self, q):
        cursor = self.cnx.cursor()
        cursor.execute(q)
        return cursor.fetchmany(size=999999)  # fetchall doesnt work??

    def __del__(self):
        self.cnx.close()

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
    def __init__(self, name,
                 datetime,
                 timereq, job_id):
        self.name = name
        self.timeReq = timereq
#       doBy is the date of occurence
#                                     year  m  d   h   m   s   mics  tz
        self.doBy = datetime
        # self.doBy = datetime.datetime(2016, 1, 27, 20, 46, 43, 0, None)
        self.job_id = job_id

#   time left (calculated from current time)
    def timeLeft(self):

        self.timeUntil = self.doBy - datetime.datetime.today()
        return self.timeUntil

# time left (calculatd from a specific time)
    def timeLeftFromTime(self, year, month, day,
                         hour, minute, second,
                         microsecond, tzinfo):
        self.timeUntil = self.doBy - \
                datetime.datetime.today(year, month, day,
                                        hour, minute, second,
                                        microsecond, tzinfo)
        return self.timeUntil

    def __str__(self):
        if (self.name == ''):
            self.name == 'Unspecified'

        self.outstr = self.name + " doBy="
        self.outstr += str(self.doBy.year) + "-"
        self.outstr += str(self.doBy.month) + "-"
        self.outstr += str(self.doBy.day) + " "
        self.outstr += str(self.doBy.hour) + ":"
        self.outstr += str(self.doBy.minute) + ":"
        self.outstr += str(self.doBy.second) + " timeReq="
        # self.outstr += str(self.doBy.microsecond) + " "
        # self.outstr += str(self.doBy.tzinfo)
        self.outstr += str(self.timeReq)

        return self.outstr

#####################################


def initdbclass():
    q = "DELETE FROM wt"  # clear table before doing anything
    db.query(q)

    q = """
    INSERT INTO wt VALUES('laundry','180000',
                          STR_TO_DATE('2016/02/18 20:46:43',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('something new on same date','8400',
                          STR_TO_DATE('2016/02/27 23:46:43',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('paper','18000',
                          STR_TO_DATE('2016/02/08 14:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('csc club meeting','720000',
                          STR_TO_DATE('2016/02/08 11:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('database project','2160000',
                          STR_TO_DATE('2016/02/29 08:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)
    db.cnx.commit()


def dofotm():  # day of first of this month
    return date(datetime.datetime.today().year,
                datetime.datetime.today().month, 1).weekday()


def dofotm_specific(y, m):  # day of first of a specific month
    return date(y, m, 1).weekday()


def ditm():  # days in this month
    return calendar.monthrange(datetime.datetime.today().year,
                               datetime.datetime.today().month)[1]


def ditm_specific(y, m):  # days in this month
    return calendar.monthrange(y, m)[1]


def ntf(arg):  # new test function
    print("button pressed, ntf(" + str(arg) + ") invoked")
    for item in dodwj[arg]:
        print(dodwj[arg][item])


def tf(arg):
    print("button pressed, tf(" + str(arg) + ") invoked")
    joblistbox.delete(0, END)
    for item in dodwj[arg]:
        joblistbox.insert(END, dodwj[arg][item])
    # print(dodwj[arg])


def calpop():
    # populates a grid with the days of the month in a button format
    gridindex = dofotm() + 1
    currday = 1
    daywidth = 32  # 32 pixels width
    calwidth = daywidth * 7  # 7 days in a week
    # calheight = daywidth * 5 # max 5 weeks in a month?

    calwidth = 2  # temp calwidth, 2 is width based on characters
    for x in range(0, 9):  # will just break after done? max=99 is ok?
        if (currday == ditm()):
            break
        for y in range(0, 7):
            y = gridindex
            mnth = datetime.datetime.today().month
            binddate = datetime.date(2016, mnth, currday)
            btn1 = tk.Button(root, width=calwidth, text=currday,
                             command=lambda j=binddate: tf(j))
            btn1.grid(row=x, column=y)
            if (currday == ditm()):
                break
            currday = currday + 1
            gridindex = gridindex + 1
            if (gridindex == 7):
                gridindex = 0
                break


def refreshjoblist():
    q = """
    SELECT * from wt;
    """
    dbdata = db.query(q)

    for item in dbdata:
        joblist.append(Job(item[0], item[2],
                       item[1], item[3]))

    matches = 0  # dont even need this anymore

    for item in joblist:
        if (item.doBy.date() in doBylist):
            matches = matches + 1
        else:
            doBylist.append(item.doBy.date())

    newlist = [x for x in doBylist if x == joblist[0].doBy.date()]
    print("sdf " + str(newlist))  # newlist contains unique dates?
    i = 1
    global dodwj
    for item in joblist:
        if(item.doBy.date() in dodwj):
            i = i + 1
            dodwj[item.doBy.date()][i] = item  # dict can override
        else:
            dodwj[item.doBy.date()][i] = item  # dict can override
        i = 1
    print("printing dodwj:")

    # to access list of jobs by date... # TIP
    # for item in dodwj:
    #    for jobitem in dodwj[item]:
    #            #print(dodwj[item][jobitem])

    # - get the dates from doBylist (this contains unique dates)
    # - traverse list of jobs. create new array for first occurence of
    #   a date. add job to that date. for other jobs on that date, add
    #   them to the created array

    # - when populating cal, change color when there is event

    print("#########################")
    print("refreshed job DB. items: ")
    print("#########################")
    for item in joblist:
        print(item)

if __name__ == "__main__":
    db = Database()  # custom database class (mysql)

    initdbclass()
    joblist = []
    doBylist = []
    refreshjoblist()

    c = calendar
    year = 2016
    month = 1

    # db.additem('wt', 'newdbitem', '3600')

    CalApp().run()
    sys.exit()
    ################
    # tkinter stuff
    root = tk.Tk()
    root.title("tkinter window")
    test1 = tk.Label(root, text="thistext")

#    f = tk.Frame(root, height=32, width=32)
#    f.pack_propagate(0)
#    f.pack()

#    btn1 = tk.Button(f, text = "a button", command=tf)
#    btn1.pack(fill=BOTH, expand=1)

    joblistbox = tk.Listbox(root, width=35, height=5)
    for item in joblist:
        joblistbox.insert(END, item.name)  # insert in listbox

    joblistbox.grid(row=5, columnspan=7)  # figure this out

    calpop()

    root.mainloop()
