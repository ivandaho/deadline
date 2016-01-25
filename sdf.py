import datetime
import calendar
import tkinter as tk


class Job:
    def __init__(self, name):
        self.name = name
        self.timeTillStart = 1
#                                     year  m  d   h   m   s   mics  tz
        self.doBy = datetime.datetime(2016, 1, 20, 20, 46, 43, 0, None)

#   time left from current time
    def timeLeft(self):
        self.timeUntil = self.doBy - datetime.datetime.today()
        return self.timeUntil

    def timeLeftFromTime(self, year, month, day, hr, min, sec, ms, tz):
        self.timeUntil = self.doBy - \
                datetime.datetime.today(year, month, day, hr, min, sec, ms, tz)
        return self.timeUntil

    def __str__(self):
        self.outstr = "job name: " + self.name + " "
        self.outstr += str(self.doBy.year) + "-"
        self.outstr += str(self.doBy.month) + "-"
        self.outstr += str(self.doBy.day) + "-"
        self.outstr += str(self.doBy.hour) + "-"
        self.outstr += str(self.doBy.minute) + "-"
        self.outstr += str(self.doBy.second) + "-"
        self.outstr += str(self.doBy.microsecond) + "-"
        self.outstr += str(self.doBy.tzinfo)

        return self.outstr

#####################################
j = Job("this new job")
todaysdate = datetime.datetime.today()
# print(d)
print("time until " + str(j.doBy) + ": " + str(j.timeLeft()))
# print(j.timeLeft())
c = calendar

year = 2016
month = 1
# print(c.month(year, month))

str1 = c.prmonth(year, month)

root = tk.Tk()
root.title("cal")

label1 = tk.Label(root, text=str1, font=('courier', 14, 'bold'), bg='yellow')
label1.pack(padx=3, pady=5)

root.mainloop()
