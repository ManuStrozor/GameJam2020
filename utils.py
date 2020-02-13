import datetime


def float_to_str(n, d=0):
    f = "{0:."+str(d)+"f}"
    return f.format(n)


def time_to_str(time):
    td = datetime.timedelta(seconds=time)
    minutes, seconds = divmod(td.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
