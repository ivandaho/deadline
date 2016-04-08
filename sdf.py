import datetime
import mysql.connector
from dateutil import tz

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
from kivy.properties import (
        ObjectProperty, StringProperty, NumericProperty,
        OptionProperty
)
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
        InputFields:

            name: 'NAME'
            doby: 'DOBY'
            type: 'TYPE'
            timereq: 'TIMEREQ'

            pos:self.parent.pos
            size:self.parent.size
            orientation: 'vertical'

            Label:
                text: 'choose date first'
            TextInput:
                text: str(self.parent.strname)
                size:self.size
            TextInput:
                text: str(self.parent.strtype)
                size:self.size
            TextInput:
                text: str(self.parent.strtimereq)
                size:self.size

        SubmitBtn:
            size_hint: (1, .25)
            text:'Submit Job'
        BackBtn:
            size_hint: (1, .25)
            text: 'back to menu'
            # on_press: root.manager.current = '1'
<NW>:
    canvas:
        Color:
            rgba:.267,.267,.267,.95
            # rgba:.0941,.4118,.5216,.95
        Rectangle:
            size:(self.size)
            pos:(self.pos)
    BoxLayout:
        orientation:'vertical'
        NWLabel:
        AddBtn:
            size_hint:(1,0.1)
            text:'Add Job'

<NW2>:
    canvas:
        Color:
            rgba: self.c0, self.c1, self.c3
            # rgba:.4353,.502,.0784,.95
        Rectangle:
            size:(self.size)
            pos:(self.pos)
    BoxLayout:
        orientation:'vertical'
        NWLabel2:
        BoxLayout:
            size_hint:(1,0.1)
            orientation:'horizontal'
            DelBtn:
                text:'Delete Job'
                background_color: 1,0,0,1
            ModBtn:
                text:'Modify Job'

<NWLabel2>:
    markup: True
    text_size: self.width * 0.9, self.height * 0.9
    text: self.parent.parent.lbltext
    valign: 'top'

    # size_hint:(None,None)
    # size: (self.parent.width * 0.5, self.parent.height * 0.5)

<NWLabel>:
    markup: True
    pos:(self.parent.width, self.parent.height*1.2) # why need this?
    text_size: self.width * 0.9, self.height * 0.9
    text: self.parent.parent.lbltext
    #size_hint:(None,None)
    valign: self.parent.parent.v
    halign: self.parent.parent.h

<MonthDisplay>:
    md: md
    canvas.before:
        Color:
            rgba:1,1,1,1
        Rectangle:
            pos:(self.pos)
            size:(self.size)

        Color:
            rgba:0.4,0.4,0.4,1
        Rectangle:
            pos:(self.x+1, self.y+1)
            size:(self.width-2,self.height-2)

    Label:
        id: md
        color:(1,1,1,1)
        text: self.parent.mnthtext


<DayDisplay>:
    DayLabel:
        text:'[color=ffffff]SUN[/color]'
    DayLabel:
        text:'[color=ffffff]MON[/color]'
    DayLabel:
        text:'[color=ffffff]TUE[/color]'
    DayLabel:
        text:'[color=ffffff]WED[/color]'
    DayLabel:
        text:'[color=ffffff]THU[/color]'
    DayLabel:
        text:'[color=ffffff]FRI[/color]'
    DayLabel:
        text:'[color=ffffff]SAT[/color]'

<DayLabel>:
    markup: True
    halign:'center'
    valign:'middle'
    canvas.before:
        Color:
            rgba:1,1,1,1
        Rectangle:
            pos:(self.pos)
            size:(self.size)

        Color:
            rgba:0.4,0.4,0.4,1
        Rectangle:
            pos:(self.x+1, self.y)
            size:(self.width-2,self.height)
    canvas:
        Color:
            rgba:1,0,0,0.0
    text_size: self.size

<InfoArea>:
    Label:
        markup: True
        id: ilb
        text:self.parent.txt
        canvas.before:
            Color:
                rgba:1,1,1,1
            Rectangle:
                pos:(self.pos)
                size:(self.size)

            Color:
                rgba:0.4,0.4,0.4,1
            Rectangle:
                pos:(self.x+1, self.y)
                size:(self.width-2,self.height)
        canvas:
            Color:
                rgba:1,1,0,1

""")

delaymode = False


class NL(Label):
    pass


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


def hexc(clr):
    x = int(clr[0] * 256)
    y = int(clr[1] * 256)
    z = int(clr[2] * 256)

    s = ''
    s += (hex(x)[2:len(hex(x))])
    s += (hex(y)[2:len(hex(y))])
    s += (hex(z)[2:len(hex(z))])

    return s


class BtnArea(GridLayout):
    pass


class InfoArea(GridLayout):
    ilb = ObjectProperty(None)
    txt = StringProperty()
    pass


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
    dater = ObjectProperty()

    ig0 = InstructionGroup()  # white background
    ig1 = InstructionGroup()
    ig2 = InstructionGroup()
    ig2alt = InstructionGroup()
    ig3 = InstructionGroup()
    ig0.add(Color(1, 1, 1, 1))
    ig0.add(Rectangle(size=(Window.width, Window.height * 0.89)))

    j = None

    def on_touch_down(self, touch):
        if (self.j is not None):
            # TODO: check for ctrl or other modfier to bypass
            #       for buttons that are harder to click on directly

            # event under cursor
            spawnjw(self, self.j)
        else:
            # otherwise propagate touch
            return super(CalGame, self).on_touch_down(touch)

    def kivycalpop(self, yr, mnth):
        ba = self.parent.children[4]  # button area
        ba.md.text = str(self.dater.month) + '/' + str(self.dater.year)
        # for refresh, don't really the next 2 lines need because
        # it will happen later, but the later thing is scheduled
        # 0.01 seconds later because it requires creation. not sure

        self.canvas.remove(self.ig0)
        self.canvas.add(self.ig0)

        # remove widgets for refresh
        for x in range(0, len(self.children)):
            self.remove_widget(self.children[0])
        # this is for the calendar buttons only
        gridindex = dofotm_specific(yr, mnth) + 1
        if (gridindex == 7):
            gridindex = 0
        currday = 1
        y = 0
        # yr = arrow.get(yr, mnth, 1).year
        # mnth = arrow.get(yr, mnth, 1).month

        while (currday <= ditm_specific(yr, mnth)):
            arwdate = arrow.get(yr, mnth, currday, 0, 0, 0, 0, tz.tzlocal())
            arwdate = arwdate.date()
            # arwdate = arrow.get(yr, mnth, currday).date()

            if (y < gridindex):
                # add empty widgets to fill grid
                # to create offset for first day of week
                ew = EW()
                self.add_widget(ew)
                y = y + 1
            else:
                self.add_widget(DayBtn(text=str(currday), arwin=arwdate))
                currday = currday + 1

    def rm(self, insgrp):
        self.canvas.remove(insgrp)
        insgrp.clear()
        pass

    def makemarks(self, yr, mnth):
        for job in joblist:
            job.brp = []
            job.srp = None
        self.rm(self.ig1)  # removes the insgrp from canvas
        self.rm(self.ig2)
        self.rm(self.ig2alt)
        # getspace(self, yr, mnth) # only needed once
        self.ig1.clear()  # clears the insgrp
        self.ig2alt.clear()
        self.ig2.clear()

        for child in self.children:
            if (isinstance(child, DayBtn)):
                if (child.arwin == arrow.get(tz.tzlocal()).date()):
                    # draw today's marker
                    child.drawtodaymarker(self.ig1)

# ################# old draw method based on event #########################
#                 # if event(s) found on this daybtn
#                 # child is DayBtn
#                 # contains datetime.datetime in input
#                 for event in dodwj[child.arwin]:
#                     # event is i number, doesnt contain job data
#                     # job data is in dodwj[child.input][event]
#
#                     # add instructon for each event
#                     child.drawnew(dodwj[child.arwin][event], self.ig2)
#
# ############################## new draw method ###########################

                if (len(daydict[child.arwin]) > 0):
                    ji = []
                    for item in daydict[child.arwin]:
                        ji.append(item)
                else:
                    ji = []

                for item in ji:
                    child.drawnewer(item, self.ig2, self.ig2alt, cleanvar)

        self.canvas.add(self.ig1)  # 2 is daymarker
        self.canvas.add(self.ig2)  # 2 is job related markers
        self.canvas.add(self.ig2alt)  # 2 is job related markers
        # print('MADE MARKS!')

    def getspace(self, yr, mnth):
        # get days in this month first
        ditmvar = ditm_specific(yr, mnth)
        # check job against each day (in month)
        # this is for the bars. have to check each day
        # to see what jobs need to be done on what days
        currday = 1
        while (currday <= ditmvar):
            # date to check
            dtc = arrow.get(yr, mnth, currday, 0, 0, 0, 0, tz.tzlocal())
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

                # dtc.floor('day') to get a date that is 00:00
                if (dtc.floor('day') <= dobyarrow):
                    # if there is a job due after this day's 0:00

                    if (dtc.floor('day') >= mswd):
                        jobstodo.append(job)

                    # why did i do this?
                    if (dtc.floor('day').replace(days=1) >= dobyarrow):
                        if job in jobstodo:
                            jobstodo.remove(job)
                        jobstodo.append(job)
                        pass

                daydict[dtc.date()] = jobstodo

            x = 1
            tj = 0
            for item in daydict[dtc.date()]:
                tj = tj + 1
                if (item.line == 0):
                    item.line = x
                # TODO: write something better for line > 3
                x = x + 1
                if (x == 4):
                    x = 1

            currday = currday + 1


class InputFields(BoxLayout):
    this = StringProperty('unmodded')

    strname = 'enter name'
    strdoby = 'enter doby'
    strtype = 'enter type'
    strtimereq = 'enter timereq in seconds'


class BackBtn(Button):
    def on_release(self):
        sm = self.parent.parent.parent
        sm.current = '1'


class SubmitBtn(Button):

    datevar = arrow.get()

    def calctimereq(self, source):
        # set defaults
        d = 0
        h = 0
        m = 0

        if (source.find(':') != -1):
            # if found ':'
            hpos = source.find(':')
            h = source[0:hpos]
            m = source[hpos+1:len(source)]

        if (source.find('d') != -1):
            # if found 'd'
            dpos = source.find('d')
            x = dpos - 1
            while(x >= 0):
                if (source[x].isdigit()):
                    dstart = x
                    x = x - 1
                else:
                    break

            d = source[dstart:dpos]

        if (source.find('h') != -1):
            # if found 'h'
            hpos = source.find('h')
            x = hpos - 1
            while(x >= 0):
                if (source[x].isdigit()):
                    hstart = x
                    x = x - 1
                else:
                    break

            h = source[hstart:hpos]

        if (source.find('m') != -1):
            # if found 'm'
            mpos = source.find('m')
            x = mpos - 1
            while(x >= 0):
                if (source[x].isdigit()):
                    mstart = x
                    x = x - 1
                else:
                    break

            m = source[mstart:mpos]

        tt = int(d) * 86400 + int(h) * 3600 + int(m) * 60
        return str(tt)

    def on_release(self):

        name = self.parent.children[2].children[2].text
        timereq = self.calctimereq(self.parent.children[2].children[0].text)
        datestr = self.datevar.format('YYYY/MM/DD HH:mm:ss')

        q = 'INSERT INTO wt VALUES(\''
        q = q + name
        q = q + '\',\'' + timereq + '\','
        q = q + ' STR_TO_DATE(\''
        q = q + datestr + '\', \'%Y/%m/%d %T\'), NULL);'
#         print('QUERY: ')
#         print(q)
        db.query(q)
        db.cnx.commit()

        refreshjoblist(joblist, doBylist, dodwj, daydict)

        sm = self.parent.parent.parent
        sm.current = '1'

        refwid = sm.children[0].children[0]
        refwid.remove_widget(nw)

        dater = refwid.children[0].children[2].dater
        refwid.children[0].children[2].getspace(dater.year, dater.month)
        refwid.children[0].children[2].makemarks(dater.year, dater.month)


class ModBtn(Button):
    def on_release(self):
        pass


class DelBtn(Button):

    def on_release(self):

        # deletes from db
        deldbitem(self, self.parent.parent.parent.jb)

        # deletes from joblist (prevent refresh??)
        for job in joblist:
            if (job == self.parent.parent.parent.jb):
                joblist.remove(self.parent.parent.parent.jb)
                break

        refwid = self.parent.parent.parent.parent
        refwid.remove_widget(nw2)

        cm = refwid.children[0].children[2]
        dater = cm.dater

        # makemarks is always happening, but need getspace to refresh
        cm.getspace(dater.year, dater.month)


class AddBtn(Button):
    def on_release(self):
        InputFields.this = 'WAFKJF'
        sm = self.parent.parent.parent.parent.parent
        sm.current = '2'
        refwid = sm.children[0].children[0].children[2]
        timereqw = refwid.children[0]
        typew = refwid.children[1]
        namew = refwid.children[2]
        dobyw = refwid.children[3]

        # 0123456789
        # 2016-03-31
        yearstr = int(str(nw.date)[0:4])
        monthstr = int(str(nw.date)[5:7])
        daystr = int(str(nw.date)[8:10])
        SubmitBtn.datevar = arrow.get(yearstr, monthstr, daystr)

        timereq = 86400  # 1 day, in seconds
        timereqw.text = str(timereq)
        typew.text = 'modded typew'
        dobyw.text = 'Enter info for new job on ' + str(nw.date)
        namew.text = 'modded namew2'


class NWLabel(Label):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # if clicked on box. for later
            pass
        self.parent.parent.parent.remove_widget(nw)
        return True  # eats touch


class NWLabel2(Label):
    def on_touch_down(self, touch):
        self.parent.parent.parent.remove_widget(nw2)
        return True  # eats touch


class NW(StackLayout):
    date = arrow.get()
    lbltext = StringProperty()

    v = OptionProperty("middle", options=["middle", "top"])  # middle/top
    h = OptionProperty("center", options=["center", "left"])  # center/left

    def draw(self, jobitems):
        self.lbltext = '[size=24][b]No jobs on '
        self.lbltext += str(self.date) + '[/b][/size]'
        # self.v = 'middle'
        if (len(jobitems) > 0):

            # self.v = 'top'
            self.v = 'top'
            self.h = 'left'
            self.lbltext = '[size=32][b]Tasks on '
            self.lbltext += str(self.date) + ' :\n[/b][/size]'

            # sort by key doBy
            for item in sorted(jobitems, key=lambda sort: sort.doBy):
                self.lbltext += '[size=24][b][color=' + hexc(item.clr) + ']'
                self.lbltext += str(item.name) + '[/color][/b][/size]'
                if (item.doBy.date() == self.date):
                    self.lbltext += '\n[color=''ffffff'']Due '
                    self.lbltext += '[b]this day[/b]'
                else:
                    self.lbltext += '\n[color=''ffffff'']Due '
                    self.lbltext += str(item.doBy.format('D MMMM YYYY'))

                self.lbltext += ' at ' + str(item.doBy.format('h:mm A'))
                self.lbltext += ' (' + str(item.doBy.humanize())
                if (item.doBy.date() == self.date):
                    self.lbltext += ')[/color]\n\n'
                else:
                    self.lbltext += '/' + str(item.timeLeft(self.date))
                    self.lbltext += ' from this date)[/color]' + '\n\n'
                # str(item.doBy.format('M/D/YY HH:mm')) + \

                # self.lbltext += item.doBy.humanize(self.date) + '\n'
        else:
            self.v = 'middle'
            self.h = 'center'


class NW2(StackLayout):
    lbltext = StringProperty()
    jb = ObjectProperty()

    c0 = 0
    c1 = 0
    c2 = 0
    c3 = 0

    ig = InstructionGroup()

    def rm(self, insgrp):
        self.canvas.before.remove(insgrp)
        insgrp.clear()

    def draw(self, job):
        self.rm(self.ig)  # removes the insgrp from canvas
        self.ig.clear()  # clears the insgrp

        self.jb = job
        self.c0 = job.clr[0]
        self.c1 = job.clr[1]
        self.c2 = job.clr[2]

        self.ig.add(Color(self.c0, self.c1, self.c2, 0.7))
        self.ig.add(Rectangle(size=self.size, pos=self.pos))

        self.canvas.before.add(self.ig)

        if (job.timeReq > 0):
            trs = str(job.timeReq/86400.) + ' days'  # time req simplified
            mswd = arrow.get(job.doBy.timestamp - job.timeReq)
            mswdd = mswd.format('d MMMM YYYY')
            mswdt = mswd.format('h:mm A')
        self.lbltext = ''
        self.lbltext += '[color=444444][b][size=24]'
        self.lbltext += str(job.name) + '[/size][/b]\n'
        if (job.timeReq > 0):
            self.lbltext += 'Due ' + str(job.doBy.format('D MMMM YYYY'))
        else:
            self.lbltext += ' at ' + str(job.doBy.format('h:mm A'))
        self.lbltext += ' (' + job.doBy.humanize() + ')\n\n'
        if (job.timeReq > 0):
            self.lbltext += 'Approximately ' + trs + ' to complete' + '\n'
            self.lbltext += 'Latest date to start is ' + str(mswdd)
            self.lbltext += ' at ' + str(mswdt) + ' ('
            self.lbltext += mswd.humanize() + ')[/color]\n\n'


nw = NW(size=(Window.width*.85, Window.height*.85))
nw.size_hint = (None, None)
nw.pos = (Window.width/2 - nw.width/2, Window.height/2 - nw.height/2)

nw2 = NW2(size=(Window.width*.85, Window.height*.85))
nw2.size_hint = (None, None)
nw2.pos = (Window.width/2 - nw2.width/2, Window.height/2 - nw2.height/2)
cleanvar = False


def spawnnw(self, jobitems, arwin):
    nw.date = arwin
    nw.draw(jobitems)
    self.parent.parent.parent.add_widget(nw)


def spawnjw(self, job):
    nw2.draw(job)
    self.parent.parent.add_widget(nw2)


class EWB(Button):
    shift = NumericProperty()
    yr = NumericProperty()
    mnth = NumericProperty()
    sm = ObjectProperty()

    def getshift(self):
        self.cm.dater = self.cm.dater.replace(months=+self.shift)

    def dates(self):
        self.yr = self.cm.dater.year
        self.mnth = self.cm.dater.month

    def delayed(self, dt):
        cm = self.parent.parent.children[2]  # calmain
        cm.getspace(self.yr, self.mnth)

    def on_release(self):
        self.cm = self.parent.parent.children[2]  # calmain
        self.getshift()
        self.dates()
        self.cm.kivycalpop(self.yr, self.mnth)
        global delaymode
        if (delaymode):
            Clock.schedule_once(self.delayed, .01)  # TODO: refine delay
        else:
            self.delayed(0)

        # sm = self.parent.parent.parent.parent
        # self.parent.children[1].makemarks()
        # sm.current = '2'
        # self.parent.parent.parent.parent.current = '2'
        # print(sm.current)


class RedrawBtn(Button):
    def on_release(self):
        global cleanvar
        if (cleanvar):
            cleanvar = False
        else:
            cleanvar = True


class DayLabel(Label):  # empty widget class
    pass


class MonthDisplay(BoxLayout):
    md = ObjectProperty(None)
    mnthtext = StringProperty()


class DayDisplay(BoxLayout):
    pass


class EW(Widget):  # empty widget class
        pass


class TBWidget(Widget):
    lab = StringProperty()


class DayBtn(Button):  # day button class
    arwin = ObjectProperty()
    # background_color = (1, 1, 1, 1) ????? why did I add this before
    text_size = (int(Window.width*0.7*0.15), int(Window.height*0.7*0.13))
    halign = 'right'
    valign = 'top'
    font_size = int(text_size[0]*0.25)
    ph = 0

    def on_release(self):
        ntf2(self, self.arwin)

    def drawtodaymarker(self, insgrp):
        insgrp.add(Color(1, 1, 1, 0.4))
        scale = 0.9  # scale * button width/height, whichever is lower
        x = self.width*scale
        y = self.height - self.width + x

        insgrp.add(Rectangle(size=(x, y),
                             pos=(self.x + self.width/2 - x/2,
                                  self.y + self.height/2 - y/2)))

    def drawnewer(self, job, insgrp, insgrpalt, clean):
        ri = self.parent.seed
        self.parent.seed = self.parent.seed + 1
        if (self.parent.seed == len(self.parent.cl)-1):
            self.parent.seed = 0

        if(checkl()):
            mw = int(self.height*0.8)
        else:
            mw = int(self.width*0.8)
        mw = mw * job.s
        mh = mw
        oh = mh

###########################
# stuff for when there are more than 1 jobs due in a day

        posi = (self.x + self.width/2 - mw/2,
                self.y + self.height/2 - mh/2)

        if ((len(dodwj[self.arwin])) > 1):
            if (job == dodwj[self.arwin][2]):
                oh = mh
                mh = mh * (1/len(dodwj[self.arwin]))

                posi = (self.x + self.width/2 - mw/2,
                        self.y + self.height/2 - oh/2)

###########################

        totalspacing = mw * 0.03
        spacing = totalspacing + totalspacing
        bh = (mw-spacing-spacing)/3.  # bar height
        bw = self.width
        bos = self.height/2-mh/2  # base offset
        jlos = bh + spacing  # job line offset

        if (job.clr is None):
            # dont reroll colors if already have color
            job.clr = self.parent.cl[ri][0],\
                self.parent.cl[ri][1],\
                self.parent.cl[ri][2]

        insgrp.add(Color(job.clr[0], job.clr[1], job.clr[2]))
        insgrpalt.add(Color(job.clr[0], job.clr[1], job.clr[2]))

        xos = 0
        mswd = arrow.get(job.doBy.timestamp - job.timeReq)

        if (job.doBy.date() == self.arwin):
            # if the date due is on current day
            rad = int(mw*0.2027)
            # draw indicator
            insgrpalt.add(RoundedRectangle(size=(mw, mh),
                                           pos=(posi),
                                           radius=(rad, rad)))

            # mouseover stuff
            # main srp (square render position)
            # its a range of the x and then the y value
            xrs = self.x+self.width/2-mw/2  # x range start
            # yrs = self.y+self.height/2-mh/2 # y range start
            yrs = self.y+self.height/2 - oh/2
            # self.y + self.height/2 - oh/2)
            job.srp = ((xrs, xrs + mw), (yrs, yrs + mh))

            bw = self.width*.5  # so that the last cell does not overlap

            if (job.timeReq == 0):
                bw = 0

        elif (mswd.date() == self.arwin):
            frac = mswd.timestamp - mswd.floor('day').timestamp
            bw = (frac/86400.*self.width)
            xos = self.width - bw

        # clean = False
        if not (cleanvar):
            insgrp.add(Rectangle(size=(bw, bh),
                                 pos=(self.x + xos,
                                      self.y + bos +
                                      (job.line - 1) * jlos)))

            # mouseover stuff
            # line brp (bar render position
            xrs = self.x+xos  # x range start
            yrs = self.y + bos + (job.line - 1) * jlos  # y range start
            job.brp.append(((xrs, xrs+bw), (yrs, yrs + bh)))

    def drawnew(self, job, insgrp):
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
        # self.parent.cl.pop(ri)

        if (job.clr is None):
            # dont reroll colors if already have  color
            job.clr = self.parent.cl[ri][0],\
                self.parent.cl[ri][1],\
                self.parent.cl[ri][2]

        insgrp.add(Color(job.clr[0], job.clr[1], job.clr[2]))

        # roundedrect marker to indicate doBy
        if(checkl()):
            mw = int(self.height*0.8)
        else:
            mw = int(self.width*0.8)
        mh = mw
        rad = int(mw*0.2027)
        insgrp.add(RoundedRectangle(size=(mw, mh),
                                    pos=(self.x+self.width/2-mw/2,
                                         self.y+self.height/2-mh/2),
                                    radius=(rad, rad)))

        # calculate timereq indicator stuff...
        clean = False
        if not clean:
            secwidth = self.parent.width/7./86400.  # pixels each second
            # timeReq width, full length required to visualize timereq
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
            # whats going on? it works tho
            totalspacing = mw * 0.03
            spacing = totalspacing + totalspacing
            bh = (mw-spacing-spacing)/3.  # bar height

            ##################
            # h1 = self.y+self.height/2-mh/2 # make btm flush with main square
            jlos = bh + spacing  # job line offset
            bos = self.height/2-mh/2  # base offset

            if (trw >= maxtrw):
                # if can't fit
                btmbar = maxtrw
                remain = trw - maxtrw  # width of remain trw
                fullbars = int(remain/self.parent.width)  # number of full bars
                topbar = remain - fullbars*self.parent.width  # <--> of top bar

                iteration = fullbars + 1    # number of full bars + top bar
                # this is if can't fit.
                # handle btmbar later

                for x in range(1, iteration+1):
                    if (x == iteration):
                        # TODO: when bars extend across months
                        # dont draw full bars. draw last(top) bar.
                        insgrp.add(Color(job.clr[0],
                                         job.clr[1],
                                         job.clr[2],))
                        insgrp.add(Rectangle(size=(topbar, bh),
                                             pos=(self.parent.width - topbar,
                                                  self.y + bos +
                                                  (job.line - 1) * jlos +
                                                  self.parent.height / 5 * x)))
                    else:
                        # draw full bars
                        insgrp.add(Color(job.clr[0],
                                         job.clr[1],
                                         job.clr[2],))
                        insgrp.add(Rectangle(size=(self.parent.width, bh),
                                             pos=(0,
                                                  self.y + bos +
                                                  (job.line - 1) * jlos +
                                                  self.parent.height / 5 * x)))

            btmbar = trw
            if (btmbar > maxtrw):
                btmbar = maxtrw
            insgrp.add(Color(job.clr[0],
                             job.clr[1],
                             job.clr[2],))

            if (job.timeReq > 0):  # if job requires time
                # TODO: timeReq can be used for events? change this to
                #       use a var like jobType or something
                if (job.doBy.floor('day') <=
                        arrow.get(job.doBy.timestamp - job.timeReq)):
                    # TODO: figure out why I wrote this, too tired for now
                    fillx = 0
                    xpos = self.center_x-btmbar
                    # dont fill
                else:
                    xpos = self.x-btmbar

                insgrp.add(Rectangle(size=(btmbar+fillx, bh),
                                     pos=(xpos,
                                          self.y + bos +
                                          (job.line - 1) * jlos)))


class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    pass


class CalApp(App):
    # top info area
    date = arrow.get(tz.tzlocal())
    cy = date.year  # current year
    cm = date.month  # current month
    dayinfo = DayDisplay(size_hint=(1, 0.03))
    monthinfo = MonthDisplay(size_hint=(1, 0.08))

    # main window area
    calmain = CalGame(cols=7, size_hint=(1, .55), dater=date)
    ia = InfoArea(cols=3, size_hint=(1, .17))  # info area

    ms = 1.155  # max mouseover scale
    ss = 5.  # scale steps
    si = (ms - 1)/ss  # scale interval amount

    def delayed(self, dt):
        self.calmain.getspace(self.cy, self.cm)

    def checker(self, dt):
        # fps display, useful
        # fps = Clock.get_fps()
        # if (fps < 60):
        # print(fj is a variable in calmain/CalGame)

        foundsquare = False
        detected = None
        dj = None

        tx = Window.mouse_pos[0]
        ty = Window.mouse_pos[1]

        # reversed is [::-1] might break stuff later
        for job in joblist[::-1]:
            if (detected == 'square'):
                break
            if (dj is None):
                # for each job
                # if still havent found a square
                # search for square
                if (job.srp is not None):
                    if (tx >= job.srp[0][0] and tx <= job.srp[0][1]):
                        if (ty >= job.srp[1][0] and ty <= job.srp[1][1]):
                            # found a square within bounds
                            foundsquare = True
                            detected = 'square'
                            dj = job
                            break

            # if there is no square after searching
        if (foundsquare is not True):
            for job in joblist:
                if (dj is None):
                    # then only look for line.
                    if (foundsquare is not False):
                        if (len(job.brp) > 0):
                            for cell in job.brp:
                                if (tx >= cell[0][0] and tx <= cell[0][1]):
                                    if (ty >= cell[1][0] and ty <= cell[1][1]):
                                        detected = 'line'
                                        dj = job

        for job in joblist:
            if (dj == job):
                # expand if mouseovered
                if (dj.s < self.ms):
                    dj.s = dj.s + self.si  # expand variable

            else:
                # contract if not mouseovered
                if (job.s > 1):
                    job.s = job.s - self.si

        self.calmain.makemarks(self.cy, self.cm)  # only need once per check
        self.calmain.j = dj
        if (self.calmain.j is not None):
            self.ia.txt = '[color=' + hexc(self.calmain.j.clr) + ']'
            self.ia.txt += str(self.calmain.j.name) + '[/color]'
        else:
            self.ia.txt = '--'
        if (dj is not None):
            pass
            # print('detected ' + detected + ' on ' + str(dj.name))

    def build(self):
        sm = ScreenManager()
        fs = FirstScreen(name='1')
        ss = SecondScreen(name='2')

        flo = FloatLayout()
        blo = BoxLayout(orientation='vertical')
        blo.add_widget(self.monthinfo)
        blo.add_widget(self.dayinfo)
        blo.add_widget(self.calmain)
        curryr = arrow.get(tz.tzlocal()).year
        currmnth = arrow.get(tz.tzlocal()).month

        ewb = EWB(text='<<', sm=sm, shift=-1)
        ewb1 = RedrawBtn(text='toggle clean')
        ewb2 = EWB(text='>>', sm=sm, shift=1)
        eb = BtnArea(cols=3, size_hint=(1, .17))
        # ewb.size = (100,100) # why do i need this??
        blo.add_widget(eb)
        blo.add_widget(self.ia)
        eb.add_widget(ewb)
        eb.add_widget(ewb1)
        eb.add_widget(ewb2)

        flo.add_widget(blo)
        fs.add_widget(flo)

        sm.add_widget(fs)
        sm.add_widget(ss)
        sm.current = '1'

        with self.calmain.canvas:
            Rectangle(pos=(0, 0), size=Window.size)

        self.calmain.kivycalpop(curryr, currmnth)
        global delaymode
        if (delaymode):
            Clock.schedule_once(self.delayed, .1)  # TODO: refine delay
        else:
            self.delayed(0)
        Clock.schedule_interval(self.checker, 1/60)  # TODO: refine delay

        return sm


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
        self.clr = None

        self.brp = []  # bar render pos
        self.srp = None  # square render pos
        self.s = 1

        self.key = job_id

    # time left (calculated from current time)
    def timeLeft(self, date):

        dated = arrow.get(date.year, date.month, date.day,
                          0, 0, 0, 0, tz.tzlocal())
        return self.doBy.humanize(dated)

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

        trs = str(self.timeReq/86400.) + ' days'  # time req simplified

        self.outstr = self.name + " | Due on "
        self.outstr += str(self.doBy.year) + "-"
        self.outstr += str(self.doBy.month) + "-"
        self.outstr += str(self.doBy.day) + " "
        self.outstr += str(self.doBy.hour) + ":"
        self.outstr += str(self.doBy.minute) + " ("
        self.outstr += str(self.doBy.humanize()) + ") | "
        self.outstr += "Time required: "
        self.outstr += trs + ' | '
        self.outstr += str(self.key)
        # self.outstr += str(self.doBy.second) + " timeReq="
        # self.outstr += str(self.doBy.microsecond) + " "
        # self.outstr += str(self.doBy.tzinfo)

        return self.outstr

#####################################


def deldbitem(self, job):
    # CONTINUE
    q = 'DELETE FROM wt WHERE job_id = "' + str(job.key) + '";'
    db.query(q)
    db.cnx.commit()
    # unneeded because we remove the job directly from the joblist
    # refreshjoblist(joblist, doBylist, dodwj, daydict)
    # TODO: make it such that the db is only accessed on open and exit


def initdbclass():
    q = "DELETE FROM wt"  # clear table before doing anything
    db.query(q)

    # weird things happen when the time has weird numbers
    q = """
    INSERT INTO wt VALUES('laundry','86400',
                          STR_TO_DATE('2016/04/18 20:01:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('something new on same date','604800',
                          STR_TO_DATE('2016/04/27 23:46:43',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('paper','172800',
                          STR_TO_DATE('2016/04/08 14:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('csc club meeting','0',
                          STR_TO_DATE('2016/04/09 11:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('database project','604800',
                          STR_TO_DATE('2016/04/29 08:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('test new on 25th','86400',
                          STR_TO_DATE('2016/04/25 08:00:00',

                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)
    q = """
    INSERT INTO wt VALUES('new item in may','604800',
                          STR_TO_DATE('2016/05/02 08:00:00',
                                      '%Y/%m/%d %T'), NULL);
    """
    db.query(q)

    q = """
    INSERT INTO wt VALUES('second new item in may','86400',
                          STR_TO_DATE('2016/05/15 08:00:00',
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


def refreshjoblist(joblist, doBylist, dodwj, daydict):
    printdebug = False
    # pull data from sql db
    q = """
    SELECT * from wt;
    """
    dbdata = db.query(q)

    # delete all items in joblist
    del joblist[0:len(joblist)]
    del doBylist[0:len(doBylist)]
    dodwj.clear()
    daydict.clear()

    # add items from sql db to joblist
    for item in dbdata:
        if(printdebug):
            print(item)
        joblist.append(Job(item[0], arrow.get(item[2], tz.tzlocal()),
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

    if(printdebug):
        print("#########################")
        print("refreshed job DB. items: ")
        print("#########################")
        for item in joblist:
            print(item)

if __name__ == "__main__":
    db = Database()  # custom database class (mysql)
    reset = True
    # flag for rest/debug etc

    if (reset):
        initdbclass()
    # dictionary of days with jobs
    dodwj = defaultdict(dict)
    # dictionary of days with jobs
    daydict = defaultdict(dict)
    joblist = []
    doBylist = []
    refreshjoblist(joblist, doBylist, dodwj, daydict)

    # db.additem('wt', 'newdbitem', '3600')

    CalApp().run()
    sys.exit()
