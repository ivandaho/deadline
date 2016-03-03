import datetime
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
from kivy.uix.label import Label
# import random

Builder.load_string("""
<SecondScreen>:
    BoxLayout:
        orientation: 'vertical'
        TBWidget:
            InputFields:

                name: 'NAME'
                doby: 'DOBY'
                type: 'TYPE'
                timereq: 'TIMEREQ'

                pos:self.parent.pos
                size:self.parent.size
                orientation: 'vertical'

                TextInput:
                    size:self.size
                    text: str(self.parent.this)
                TextInput:
                    size:self.size
                TextInput:
                    size:self.size
                TextInput:
                    size:self.size
                    canvas:
                        Color:
                            rgba:1,0,0,.3
                        Rectangle:
                            size:self.size
                            pos:self.pos

        Button:
            text: 'submit'
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
    BoxLayout:
        orientation:'vertical'
        NWLabel:
        AddBtn:
            size_hint:(1,0.1)
            text:'Add Job'

<NWLabel>:
    pos:(self.parent.width, self.parent.height*1.2)
    canvas:
        Color:
            rgba:1,0,0,.3
        Rectangle:
            size:(self.size)
            pos:(self.pos)
    text_size: self.size
    text: self.parent.parent.lbltext
    #size_hint:(None,None)
    valign: 'top'

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

    ig1 = InstructionGroup()
    ig2 = InstructionGroup()

    def kivycalpop(self):
        # this is for the calendar buttons only
        gridindex = dofotm() + 1
        currday = 1
        y = 0
        year = arrow.get().year
        mnth = arrow.get().month

        while (currday <= ditm()):
            arwdate = arrow.get(year, mnth, currday).date()

            if (y < gridindex):
                # add empty widgets to fill grid
                # to create offset for first day of week
                ew = EW()
                self.add_widget(ew)
                y = y + 1
            else:
                self.add_widget(DayBtn(text=str(currday), arwin=arwdate))
                currday = currday + 1

    def rm(self, insgrp1, insgrp2):
        self.canvas.remove(insgrp1)
        insgrp2.clear()
        pass
    def makemarks(self):
        self.rm(self.ig1, self.ig2)
        getspace(self)
        self.ig1.clear()
        self.ig2.clear()
        for child in self.children:
            if (isinstance(child, DayBtn)):
                if (child.arwin == arrow.get().date()):
                # draw today's marker
                    child.drawtodaymarker(self.ig1)
                # if event(s) found on this daybtn
                # child is DayBtn
                # contains datetime.datetime in input
                for event in dodwj[child.arwin]:
                    # event is i number, doesnt contain job data
                    # job data is in dodwj[child.input][event]

                    # add instructon for each event
                    child.drawnew(dodwj[child.arwin][event], self.ig2)

        self.canvas.add(self.ig1) # 2 is job related markers
        self.canvas.add(self.ig2) # 2 is job related markers



def getspace(self):
    # get days in this month first
    ditmvar = ditm()
    # check job against each day (in month)
    # this is for the bars. have to check each day
    # to see what jobs need to be done on what days
    currday = 1
    year = arrow.get().year
    mnth = arrow.get().month
    while (currday <= ditmvar):
        datetocheck = arrow.get(year, mnth, currday)
        jobstodo = []

        for job in joblist:
            # minimum start work date in int
            # compensate for time zone headache (TODO: solve later)
            # this is to calculate line number 
            # (for days with multiple jobs)
            mswd = arrow.get(job.doBy.timestamp - job.timeReq)
            dobyarrow = (arrow.get(job.doBy))

            mswd = mswd.floor('day')
            dobyarrow = dobyarrow.ceil('day')

            # if the day is a working day
            # x > y means x is more recent than y
            if (datetocheck.floor('day') <= dobyarrow):
                if (datetocheck.floor('day') >= mswd):
                    jobstodo.append(job)

            daydict[datetocheck.date()] = jobstodo 

        x = 1
        for item in daydict[arrow.get(year, mnth, currday).date()]:
            if (item.line == 0):
                item.line = x
            x = x + 1

        currday = currday + 1

        
class InputFields(BoxLayout):
    this = StringProperty('unmodded')

    strname = StringProperty()
    strdoby = StringProperty()
    strtype = StringProperty()
    strtimereq = StringProperty()

class AddBtn(Button):
    def on_release(self):
        InputFields.this = 'WAFKJF'
        sm = self.parent.parent.parent.parent.parent
        sm.current = '2'
        refwid = sm.children[0].children[1].children[2].children[0]
        timereqw = refwid.children[0]
        typew = refwid.children[1]
        dobyw = refwid.children[2]
        namew = refwid.children[3]

        timereqw.text = 'modded timereqw'
        typew.text = 'modded typew'
        dobyw.text = str(nw.date)
        namew.text = 'modded namew'

class NWLabel(Label):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # if clicked on box. for later
            self.parent.parent.parent.remove_widget(nw)
            return True  # eats touch




class NW(StackLayout):
    date = arrow.get()
    lbltext = StringProperty()

    def draw(self, jobitems):
        self.lbltext = 'no jobs to do'
        if (len(jobitems) > 0):
            self.lbltext = ''
            for item in jobitems:
                self.lbltext = self.lbltext + str(item.name) + \
                        ' due on ' + str(item.doBy.format('M/D/YY HH:mm')) + \
                        ' (' + str(item.doBy.humanize()) + \
                        ')' + '\n'



nw = NW(size=(Window.width*.85,Window.height*.85))
nw.size_hint = (None, None)
nw.pos = (Window.width/2 - nw.width/2, Window.height/2 - nw.height/2)# + EWB.height)

def spawnnw(self, jobitems, arwin):
    nw.draw(jobitems)
    nw.date = arwin
    self.parent.parent.parent.add_widget(nw)


class EWB(Button):
    screeninput = ObjectProperty()

    def on_release(self):
        pass
        # self.parent.parent.parent.parent.current = '2'
        # print(self.parent.parent.parent)


class EW(Widget):  # empty widget class
        pass

class TBWidget(Widget):
    lab = StringProperty()


class DayBtn(Button):  # day button class
    arwin = ObjectProperty()
    background_color = (1, 1, 1, 1)
    text_size = (int(Window.width*0.7*0.15), int(Window.height*0.7*0.13))
    halign = 'right'
    valign = 'top'
    font_size = int(text_size[0]*0.25)

    def on_release(self):
        ntf2(self, self.arwin)

    def drawtodaymarker(self, insgrp):
        insgrp.add(Color(1, 1, 1, 0.4))
        scale = 0.9 # scale * button width/height, whichever is lower
        x = self.width*scale
        y = self.height - self.width + x

        insgrp.add(Rectangle(size=(x,
                              y),
                        pos=(self.x + self.width/2 - x/2,
                             self.y + self.height/2 - y/2)))

    def drawnew(self, job, insgrp):
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
        #self.parent.cl.pop(ri)

        job.clr = self.parent.cl[ri][0],\
            self.parent.cl[ri][1],\
            self.parent.cl[ri][2]

        insgrp.add(Color(self.parent.cl[ri][0],
                      self.parent.cl[ri][1],
                      self.parent.cl[ri][2],))
        # insgrp.add(Color(job.clr))
        # basic marker to indicate doBy
        if(checkl()):
            mw = int(self.height*0.8)
        else:
            mw = int(self.width*0.8)
        mh = mw
        rad = int(mw*0.2027)
        insgrp.add(RoundedRectangle(size=(mw,
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
                    insgrp.add(Color(self.parent.cl[ri][0],
                                  self.parent.cl[ri][1],
                                  self.parent.cl[ri][2],))
                    insgrp.add(Rectangle(size=(topbar,
                                            bh),
                                      pos=(self.parent.width - topbar,
                                           self.y + bos + 
                                           (job.line - 1) * jlos +
                                           self.parent.height / 5. * x)))
                else:
                    # draw full bars
                    insgrp.add(Color(self.parent.cl[ri][0],
                                  self.parent.cl[ri][1],
                                  self.parent.cl[ri][2],))
                    insgrp.add(Rectangle(size=(self.parent.width,
                                            bh),
                                      pos=(0,
                                           self.y + bos + 
                                           (job.line - 1) * jlos +
                                           self.parent.height / 5. * x)))

        btmbar = trw
        if (btmbar > maxtrw):
            btmbar = maxtrw
        insgrp.add(Color(self.parent.cl[ri][0],
                      self.parent.cl[ri][1],
                      self.parent.cl[ri][2],))

        if (job.timeReq > 0):  # if job is an event
            # TODO: timeReq can be used for events? change this to
            #       use a var like jobType or something
            insgrp.add(Rectangle(size=(btmbar+fillx,
                                    bh),
                              pos=(self.x-btmbar,
                                   h1)))


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass


class CalApp(App):
    # main window area
    calmain = CalGame(cols=7, size_hint=(1, .55))
    calmain.size = (Window.width, Window.height * 0.95)
    calmain.pos = (0, Window.height - Window.height * 0.95)

    def delayed(self, dt):
        self.calmain.makemarks()
    def asd2(self, *args):
        self.calmain.makemarks()

    def build(self):
        sm = ScreenManager()
        fs = FirstScreen(name='1')
        ss = SecondScreen(name='2')
        tbw = TBWidget(lab="WHAT")
        ss.add_widget(tbw)

        flo = FloatLayout()
        blo = BoxLayout(orientation='vertical')
        blo.add_widget(self.calmain)
        ewb = EWB(text='reroll colours', screeninput=sm, size_hint=(1, .45), on_release=(self.asd2))
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

    def additem(self, table, name, timereq, doby):
        table = 'wt'
        # time = str(time)
        q = "INSERT INTO " + \
            table + " VALUES ('" + \
            name + "', '" + \
            timereq + "', '" + \
            doby + "', NULL);"

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
                          STR_TO_DATE('2016/03/18 20:46:43',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('something new on same date','604800',
                          STR_TO_DATE('2016/03/27 23:46:43',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('paper','172800',
                          STR_TO_DATE('2016/03/08 14:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('csc club meeting','0',
                          STR_TO_DATE('2016/03/09 11:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('database project','604800',
                          STR_TO_DATE('2016/03/29 08:00:00',
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
        jobitems = []
        for item in daydict[arwin]:
            jobitems.append(item)
    else:
        jobitems = []

    spawnnw(self, jobitems, arwin)


def refreshjoblist(joblist):
    # pull data from sql db
    q = """
    SELECT * from wt;
    """
    dbdata = db.query(q)

    # delete all items in joblist 
    del joblist[0:len(joblist)]
    # add items from sql db to joblist
    for item in dbdata:
        joblist.append(Job(item[0], arrow.get(item[2]),
                       item[1], item[3]))

        doBylist.append(arrow.get(item[2]).date())


    i = 1
    for item in joblist:
        # dictionary of jobs sorted by DATE
        if(item.doBy.date() in dodwj):
            i = i + 1

        dodwj[item.doBy.date()][i] = item  # dict can override
        i = 1
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
    # flag for rest/debug etc

    if (reset):
        initdbclass()
    joblist = []
    doBylist = []
    refreshjoblist(joblist)


    # db.additem('wt', 'newdbitem', '3600')

    CalApp().run()
    sys.exit()
