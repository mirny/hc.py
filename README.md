# hc.py
HandyCache cache browser.

It uses http://webpy.org/

You can install it by running:
```
easy_install web.py
```

Also add the following rules to Redirect list:
```
#5#~#True#~#http://(?>([^/:]+):\d+)?(.+)\?.+--$#~#http://127.0.0.1:8080/\1\2%3F#~#False#~#True
#5#~#True#~#http://(?>([^/:]+):\d+)?(.+/)+.*--$#~#http://127.0.0.1:8080/\1\2#~#False#~#True
```

Run hc.py.cmd

Now you can see what's inside your HC cache by adding -- to the adress field in your web-browser and hitting enter.