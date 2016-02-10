# deadline
todo app, goal is to have visualization of time/days left to an event's deadline or occurence.

I've always wanted a timeline style TODO app that can visualize the time left/required to the next thing I have to do.

For example, Today is Monday. I have a few tasks to complete: my laundry, a paper, and assembling a new PC.

I have enough clothes to last until friday before I absolutely have to do my laundry. The paper needs a minimum of two nights complete before the Thursday/Friday midnight deadline. The PC parts will arrive on Wednesday.

Thus, it should be visualized as something like this:

![example image](http://i.imgur.com/tQFLs6u.png)



Currently I am experimenting with tkinter for the GUI, but I am prioritizing writing code for the backend.

Written in Python3 with a MySQL database connection.

TODO/GENERAL GOALS:

* Bar style visualization for a specific time period (day, week, month, etc)
* Click a day to view tasks due on day
* Click a day to view tasks that I am able to work towards (for example, in the picture, on Tuesday I am able to work towards completing my laundry and my paper)
* Enter a time period (such as 5 hours) and generate a sublist of jobs that I can complete within that time. Useful if I have a time window during which I want to get smaller jobs out of the way.
* Group jobs into organizations (such as work, school, family, leisure) for easier viewing
