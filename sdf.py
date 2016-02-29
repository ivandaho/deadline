import datetime
# from datetime import date
import calendar
import tkinter as tk
from tkinter import END
# from tkinter import BOTH
import mysql.connector

from collections import defaultdict

# kivy stuff
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import (
    InstructionGroup,
    Rectangle,
    Color,
    RoundedRectangle,
    Ellipse
)
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty, StringProperty
import sys

from kivy.core.window import Window
from kivy.clock import Clock

from ics import Calendar  # , Event
import arrow
import os
# from dateutil import tz

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
# from kivy.uix.label import Label
# import random

Builder.load_string("""
<SecondScreen>:
    BoxLayout:
        # orientation: 'vertical'
        Button:
            text: 'my settings button'
        Button:
            text: 'back to menu'
            on_press: root.manager.current = '1'
<NW>:
    canvas:
        Color:
            rgba:.2,.2,.2,.8
        Rectangle:
            size:(self.size)
            pos:(self.pos)
    Label:
        text: self.parent.lbltext
        #size_hint:(None,None)
        pos:(self.parent.x +self.width/2, self.parent.y + self.height/2)
""")

def checkl():
    if (Window.width > Window.height):
        return True
    else:
        return False


def rgb256to1(x, y, z):
    x = 1 / 256 * x
    y = 1 / 256 * y
    z = 1 / 256 * z
    return x, y, z, 0.5


class CalGame(GridLayout):  # main class
    cl = []
    cl.append(rgb256to1(246, 216, 74))
    cl.append(rgb256to1(103, 209, 241))
    cl.append(rgb256to1(245, 162, 150))
    cl.append(rgb256to1(114, 233, 154))
    cl.append(rgb256to1(232, 170, 218))
    cl.append(rgb256to1(199, 188, 120))
    cl.append(rgb256to1(179, 222, 100))
    cl.append(rgb256to1(163, 221, 189))
    cl.append(rgb256to1(243, 177, 85))
    cl.append(rgb256to1(185, 193, 232))
    cl.append(rgb256to1(78, 228, 213))
    cl.append(rgb256to1(169, 210, 216))
    cl.append(rgb256to1(208, 242, 153))
    cl.append(rgb256to1(239, 159, 108))
    cl.append(rgb256to1(231, 183, 197))
    cl.append(rgb256to1(220, 197, 96))
    cl.append(rgb256to1(99, 207, 165))
    cl.append(rgb256to1(239, 245, 96))
    cl.append(rgb256to1(161, 194, 111))
    cl.append(rgb256to1(158, 223, 154))
    cl.append(rgb256to1(152, 230, 125))
    cl.append(rgb256to1(176, 205, 159))
    cl.append(rgb256to1(224, 180, 116))
    cl.append(rgb256to1(195, 203, 89))
    cl.append(rgb256to1(104, 242, 197))
    cl.append(rgb256to1(217, 222, 144))
    cl.append(rgb256to1(109, 221, 221))
    cl.append(rgb256to1(222, 244, 122))
    cl.append(rgb256to1(231, 224, 97))
    cl.append(rgb256to1(234, 194, 81))
    seed = 20

    def kivycalpop(self):
        # same draw method, just in kivy instead of tkinter
        # this is for the buttons only. makemarks handles other gfx
        gridindex = dofotm() + 1
        currday = 1
        y = 0
        mnth = arrow.get().month

        while (currday <= ditm()):
            arwdate = arrow.get(2016, mnth, currday).date()

            # binddate = arrow.get(2016, mnth, currday)
            # binddate = binddate.floor('day')
            if (y < gridindex):
                # add empty widgets to fill grid
                ew = EW()
                self.add_widget(ew)
                y = y + 1
            else:
                self.add_widget(DayBtn(text=str(currday), arwin=arwdate))
                currday = currday + 1

    def makemarks(self):
        print('asdlfkjlfjw' + str(self.size))
        getspace(self)
        for child in self.children:
            # draw today's marker
            if (child.arwin == arrow.get().date()):
                child.drawtodaymarker()
            # if event(s) found on this daybtn
            # child is DayBtn
            # contains datetime.datetime in input
            for event in dodwj[child.arwin]:
                # event is i number, doesnt contain job data
                # job data is in dodwj[child.input][event]

                # add instructon for each event
                child.drawnew(dodwj[child.arwin][event])

        self.canvas.add(ig1)


def getspace(self):
    ditmvar = ditm()
    # check job against each day (in month)
    currday = 1
    while (currday <= ditmvar):
        datetocheck = arrow.get(2016, 2, currday)
        jobstodo = []
        daydict[datetocheck.date()] = jobstodo

        for job in joblist:
            # minimum start work date in int
            # compensate for time zone headache (TODO: solve later)
            mswd = arrow.get(job.doBy.timestamp - job.timeReq)
            dobyarrow = (arrow.get(job.doBy))

            mswd = mswd.floor('day')
            dobyarrow = dobyarrow.ceil('day')

            # if the day is a working day
            # x > y means x is more recent than y
            if (datetocheck.floor('day') <= dobyarrow):
                if (datetocheck.floor('day') >= mswd):
                    jobstodo.append(job)
                    if (currday == 7 or currday == 8):
                        print('need to do ' + str(job.name))
            daydict[datetocheck] = jobstodo

            # modindex converted (because children are in reverse order)

        # dtmc =index of button in list of children
        # dtmc = ditm() - currday + dofotm()
        # self.children[dtmc].text = self.children[dtmc].text  # + "\n" + \
            # str(len(daydict[arrow.get(2016, 2, currday)])) + " js"

        ###################################
        x = 1
        for item in daydict[arrow.get(2016, 2, currday).date()]:
            if (item.line == 0):
                item.line = x
            x = x + 1

        currday = currday + 1


class NW(StackLayout):

    lbltext = StringProperty()

    def draw(self, jobitem):
        self.lbltext = 'no jobs to do'
        if (len(jobitem) > 0):
            self.lbltext = ''
            for item in jobitem:
                self.lbltext = self.lbltext + str(item.name) + \
                        ' due on ' + str(item.doBy) + \
                        ' (' + str(arrow.get(item.doBy).humanize()) + \
                        ')' + '\n'

    def on_touch_down(self, touch):
        self.parent.remove_widget(self)
        return True  # eats touch
        if self.collide_point(*touch.pos):
            # if clicked on box. for later
            print(self.collide_point)
            self.parent.remove_widget(self)
            return True  # eats touch


nw = NW(size=(Window.width*.85,Window.height*.85))
nw.size_hint = (None, None)
nw.pos = (Window.width/2 - nw.width/2, Window.height/2 - nw.height/2)# + EWB.height)


def spawnnw(self, job):
    nw.draw(job)
    self.parent.parent.parent.add_widget(nw)


class EWB(Button):
    screeninput = ObjectProperty()

    def on_release(self):
        self.parent.parent.parent.parent.current = '2'
        print(self.parent.parent.parent)


class EW(Widget):  # empty widget class

    # TODO: dummy var and method to be consistent with DayBtn class
    arwin = arrow.get()

    def drawnew(self, job):
        pass


class DayBtn(Button):  # day button class
    arwin = ObjectProperty()
    background_color = (1, 1, 1, 1)
    text_size = (int(Window.width*0.7*0.15), int(Window.height*0.7*0.13))
    print(str("SDLFKSJDFLJ TEXT SIze" + str(text_size)))
    halign = 'right'
    valign = 'top'
    font_size = int(text_size[0]*0.25)

    def on_release(self):
        ntf2(self, self.arwin)

    def drawtodaymarker(self):
        ig1.add(Color(1, 1, 1, 0.4))
        scale = 0.9 # scale * button width/height, whichever is lower
        if (checkl()):
            x = self.height*scale
        else:
            x = self.width*scale

        ig1.add(Ellipse(size=(x,
                              x),
                        pos=(self.x + self.width/2 - x/2,
                             self.y + self.height/2 - x/2)))

    def drawnew(self, job):
        # TODO: pass into function better, maybe dont need job
        #       datetime.datetime in DayBtn
        # doesnt actually draw but only add instrucions.
        # ############### COLOR STUFF ############## #
        # 30 random colors from iwanthue
        # H 0 360
        # C 0.4 1.2
        # L 1 1.5
        # light bg | 30 colors | soft

        ri = self.parent.seed
        self.parent.seed = self.parent.seed + 1
        if (self.parent.seed == len(self.parent.cl)-1):
            self.parent.seed = 0
        # ri = random.randint(0, len(self.parent.cl)-1)
        self.parent.cl.pop(ri)

        job.clr = self.parent.cl[ri][0],\
            self.parent.cl[ri][1],\
            self.parent.cl[ri][2]

        ig1.add(Color(self.parent.cl[ri][0],
                      self.parent.cl[ri][1],
                      self.parent.cl[ri][2],))
        # ig1.add(Color(job.clr))
        # basic marker to indicate doBy
        if(checkl()):
            mw = int(self.height*0.8)
        else:
            mw = int(self.width*0.8)
        mh = mw
        rad = int(mw*0.2027)
        ig1.add(RoundedRectangle(size=(mw,
                                 mh),
                                 pos=(self.x+self.width/2-mw/2,
                                      self.y+self.height/2-mh/2),
                                 radius=(rad, rad)))
        # calculate timereq indicator stuff...
        secwidth = self.parent.width/7./86400.  # pixels per second
        # timeReq width
        trw = job.timeReq*secwidth

        # 0 is sunday, 6 is saturday
        dayindex = job.doBy.weekday() + 1
        if (dayindex == 7):
            dayindex = 0

        # max possible bar width, based on day of the week
        maxtrw = self.parent.width / 7 * dayindex

        fillx = self.width/2  # fills out the bar

        fullbars = 0
        topbar = 0
        iteration = 3
        btmbar = 0
        totalspacing = int(mw * 0.03)
        spacing = totalspacing + totalspacing
        bh = int((mw-totalspacing)/3)  # bar height

        ##################
        h1 = self.y+self.height/2-mh/2 # make btm flush with main indicator
        print(h1)
        jlos = bh + spacing  # job line offset
        bos = self.height/2-mh/2  # base offset

        if (trw >= maxtrw):
            # if can't fit
            btmbar = maxtrw
            remain = trw - maxtrw  # width of remain trw
            fullbars = int(remain/self.parent.width)  # number of full bars
            topbar = remain - fullbars*self.parent.width   # width of top bar

            iteration = fullbars + 1    # number of full bars + top bar
            # this is if can't fit.
            # handle btmbar later

            for x in range(1, iteration+1):
                if (x == iteration):
                    # dont draw full bars. draw last(top) bar.
                    ig1.add(Color(self.parent.cl[ri][0],
                                  self.parent.cl[ri][1],
                                  self.parent.cl[ri][2],))
                    ig1.add(Rectangle(size=(topbar,
                                            bh),
                                      pos=(self.parent.width - topbar,
                                           self.y + bos + 
                                           (job.line - 1) * jlos +
                                           self.parent.height / 5. * x)))
                else:
                    # draw full bars
                    ig1.add(Color(self.parent.cl[ri][0],
                                  self.parent.cl[ri][1],
                                  self.parent.cl[ri][2],))
                    ig1.add(Rectangle(size=(self.parent.width,
                                            bh),
                                      pos=(0,
                                           self.y + bos + 
                                           (job.line - 1) * jlos +
                                           self.parent.height / 5. * x)))

        btmbar = trw
        if (btmbar > maxtrw):
            btmbar = maxtrw
        ig1.add(Color(self.parent.cl[ri][0],
                      self.parent.cl[ri][1],
                      self.parent.cl[ri][2],))

        if (job.timeReq > 0):  # if job is an event
            # TODO: timeReq can be used for events? change this to
            #       use a var like jobType or something
            ig1.add(Rectangle(size=(btmbar+fillx,
                                    bh),
                              pos=(self.x-btmbar,
                                   h1)))


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass


class CalApp(App):
    calmain = CalGame(cols=7, size_hint=(1, .55))
    calmain.size = (Window.width, Window.height * 0.95)
    calmain.pos = (0, Window.height - Window.height * 0.95)

    def delayed(self, dt):
        self.calmain.makemarks()

    def build(self):
        sm = ScreenManager()
        fs = FirstScreen(name='1')
        ss = SecondScreen(name='2')

        flo = FloatLayout()
        blo = BoxLayout(orientation='vertical')
        blo.add_widget(self.calmain)
        ewb = EWB(text='ewb', screeninput=sm, size_hint=(1, .45))
        # ewb.size = (100,100) # why do i need this??
        blo.add_widget(ewb)

        flo.add_widget(blo)
        fs.add_widget(flo)

        sm.add_widget(fs)
        sm.add_widget(ss)

        with self.calmain.canvas:
            Rectangle(pos=(0, 0), size=Window.size)

        self.calmain.kivycalpop()
        # calmain.makemarks()
        Clock.schedule_once(self.delayed, 1)  # TODO: refine delay
        return sm

# dictionary of days with jobs
dodwj = defaultdict(dict)
# dictionary of days with jobs
daydict = defaultdict(dict)
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
                 arwdt,
                 timereq, job_id):
        self.name = name
        self.timeReq = timereq  # timeReq is time required in SECONDS

        # doBy is the date of occurence
        #                             year  m  d   h   m   s   mics  tz
        self.doBy = arwdt
        # self.doBy = datetime.datetime(2016, 1, 27, 20, 46, 43, 0, None)
        self.job_id = job_id
        self.line = 0

    # time left (calculated from current time)
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
    INSERT INTO wt VALUES('laundry','86400',
                          STR_TO_DATE('2016/02/18 20:46:43',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('something new on same date','604800',
                          STR_TO_DATE('2016/02/27 23:46:43',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('paper','172800',
                          STR_TO_DATE('2016/02/08 14:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('csc club meeting','0',
                          STR_TO_DATE('2016/02/09 11:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('database project','604800',
                          STR_TO_DATE('2016/02/29 08:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)
    icstosql()
    db.cnx.commit()


def icstosql():
    # adds events after 1/1/2016 from ics file, if exists, to sql db
    # i use my personal calendar to populate so it's not uploaded here
    if (os.path.isfile('./cal.ics')):
        print('file found')
        with open('./cal.ics') as f:
            cal = Calendar(imports=f)

        startdate = arrow.get(2016, 1, 1)
        for event in cal.events:
            if (event.begin > startdate):
                inserticsevent(event)


def inserticsevent(event):
    datestr = event.begin.format('YYYY/MM/DD HH:mm:ss')
    print(datestr)
    q = 'INSERT INTO wt VALUES(\''
    q = q + str(event.name)
    q = q + '\',\'0\','
    q = q + 'STR_TO_DATE(\''
    q = q + datestr + '\', \'%Y/%m/%d %T\'), NULL);'
    db.query(q)


def dofotm():  # day of first of this month
    return arrow.get().replace(day=1).weekday()


def dofotm_specific(y, m):  # day of first of a specific month
    return arrow.get(y, m, 1).weekday()


def ditm():  # days in this month
    return arrow.get().ceil('month').day
    # return calendar.monthrange(datetime.datetime.today().year,
                               # datetime.datetime.today().month)[1]


def ditm_specific(y, m):  # days in this month
    return arrow.get(y, m, 1).ceil('month').day


def ntf(arg):  # new test function
    print("button pressed, ntf(" + str(arg) + ") invoked")
    for item in dodwj[arg]:
        print(dodwj[arg][item])


def ntf2(self, arwin):  # new test function

    if (len(daydict[arwin]) > 0):
        jobitem = []
        for item in daydict[arwin]:
            jobitem.append(item)
    else:
        jobitem = []

    spawnnw(self, jobitem)


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
    ditmvar = ditm()

    calwidth = 2  # temp calwidth, 2 is width based on characters
    for x in range(0, 9):  # will just break after done? max=99 is ok?
        if (currday == ditmvar()):
            break
        for y in range(0, 7):
            y = gridindex
            mnth = datetime.datetime.today().month
            binddate = datetime.date(2016, mnth, currday)
            btn1 = tk.Button(root, width=calwidth, text=currday,
                             command=lambda j=binddate: tf(j))
            btn1.grid(row=x, column=y)
            if (currday == ditmvar()):
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
        joblist.append(Job(item[0], arrow.get(item[2]),
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
    reset = False

    if (reset):
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
