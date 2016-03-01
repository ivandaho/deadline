# deadline
todo app, goal is to have visualization of time/days left to an event's deadline or occurence.

I've always wanted a timeline style TODO app that can visualize the time left/required to the next thing I have to do.

For example, Today is Monday. I have a few tasks to complete: my laundry, a paper, and assembling a new PC.

I have enough clothes to last until friday before I absolutely have to do my laundry. The paper needs a minimum of two nights complete before the Thursday/Friday midnight deadline. The PC parts will arrive on Wednesday.

Thus, it should be visualized as something like this:

![example image](http://i.imgur.com/tQFLs6u.png)

Current progress (sorry about the giant button. I'm testing how it would look like on a phone display):<br><br>
![example image](http://i.imgur.com/NJyBl4d.png)<br>
![example image](http://i.imgur.com/WTu2a4g.png)



Written in Python3.<br>
requirements: [kivy](https://kivy.org/#home), [ics.py](https://github.com/C4ptainCrunch/ics.py), [mysql.connector](http://dev.mysql.com/downloads/connector/python/), [arrow](http://crsmithdev.com/arrow/)

TODO/GENERAL GOALS:

* Bar style visualization for a specific time period (day, week, month, etc)
* Click a day to view tasks due on day
* Click a day to view tasks that I should work on 
* Enter a time period (such as 5 hours) and generate a sublist of jobs that I can complete within that time. Useful if I have a time window during which I want to get smaller jobs out of the way.
* Group jobs into organizations (such as work, school, family, leisure) for easier viewing
