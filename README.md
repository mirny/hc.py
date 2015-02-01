# hc.py
HandyCache cache browser.

Uses http://webpy.org/


#5#~#True#~#http://(?>([^/:]+):\d+)?(.+)\?.+--$#~#http://127.0.0.1:8080/\1\2%3F#~#False#~#True
#5#~#True#~#http://(?>([^/:]+):\d+)?(.+/)+.*--$#~#http://127.0.0.1:8080/\1\2#~#False#~#True
