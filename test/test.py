from datetime import datetime, timedelta

# print datetime(19900112)
from dateutil.parser import parse
 
a=20170825
b=str(a)
c=parse(b)
print c