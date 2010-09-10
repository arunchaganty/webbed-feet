curl "http://shaastra:\$#aastra@www.shaastra.org/2010/protected/dump.php?key=4sf1e2&tables=registration_team:events_teamevent:events_teamevent_teams" > judge.sql
sed -i "s/INSERT/REPLACE/" judge.sql
mysql -uroot -pteju judge < judge.sql
