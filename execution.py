from utils.functions import get_calls_311
from utils.functions import get_events
from utils.functions import get_dhs
from utils.functions import get_accidents

#311 Calls
data_311 = get_calls_311()
insert_calls_311(data_311)

#Events
events = get_events()
insert_events(events)

#DHS
dhs = get_dhs()
insert_dhs(dhs)

#Accidents
accidents = get_accidents()
insert_accidents(accidents)
