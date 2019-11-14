*******
The set-up for the events table is below. Note the following:
1. The primary key is the event_id and the start_date_time. The event_id is not unique because there are multiple entries in the database for events that span multiple days (one entry per day)
2. event_name needs to be configured in utf8 format in order to handle strange characters (e.g., "/") in the event name
*******



DB_NAME = 'test'

TABLES = {}
TABLES['events'] = (
   "CREATE TABLE `events` ("
   "  `event_id` int(10) NOT NULL,"
   "  `event_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,"
   "  `start_date_time` datetime NOT NULL,"
   "  `end_date_time` datetime NOT NULL,"
   "  `event_agency` varchar(255),"
   "  `event_type` varchar(255),"
   "  `event_borough` varchar(255),"
   " `event_location` varchar (500),"
   "  PRIMARY KEY (`event_id`,`start_date_time`)"
   ") ENGINE=InnoDB")