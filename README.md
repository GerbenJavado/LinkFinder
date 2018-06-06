# LinkFinder Chrome Extension
This chrome extension feeds every JavaScript file loaded during browsing back to a Python script, which calls LinkFinder and outputs the results. The chrome extension allows for whitelisting domains making you able to only scan the domains you want results of. It uses the option `-o cli` in LinkFinder which makes the extension very fast and able to process multiple JavaScript files in a few seconds. This extension is made by [karel_origin](https://twitter.com/karel_origin)

# Setup
1. Clone this branch
2. Load the chrome extension (Extension folder) into chrome (chrome://extensions/) while being in `Developer Mode`
3. Edit the variable `path_linkfinder` in http-server.py to point to the directory where you installed LinkFinder.py or move LinkFinder.py to the Extension's root folder (the folder where `http-server.py` is located).
3. Run the Python script (`python http-server.py`), which will run a listener on port 8080
4. Enable the Extension by clicking on its icon and navigating to the settings tab, then click on the Extension's On/Off switch.
5. The found JavaScript files will appear in your terminal (http-server.py) and they will be run through LinkFinder

# Optional:
- You can change the Extension's scope, navigate to the settings tab and change the value in the 'Scope' field. This will only scan JS files inside the specified scope, the scope can be a regex (`.*` by default) or simply a domain name such as `example.com`.

- It's possible to save the endpoints found by LinkFinder, just set the `Save Urls` switch to On. You can download them as a text file by clicking on the `Download Urls` button on the home page.

- There's a graph on the third page that shows you how many unique urls it has found and when, this only works when the `Save Urls` option is enabled. This is still a bit buggy, so the graph might look a little weird but I'm working on it.

- You can receive notifications when certain keywords are found inside one of the endpoints returned by LinkFinder. This is useful when you want to find interesting endpoints but don't want to manually look/search through all of them. The keywords must be seperated by newlines (enter key).
  
  Example keywords:
  admin
  login
  php
  asp
  swf

# Troubleshooting
- ## I'm not receiving all my notifications
  Chrome only allows 3 notifications to be displayed at the same time, I'm looking for another way but there currently isn't. This means that you will have to limit your keywords to only the most crucial ones. Even though it's possible to add infinite keywords.
  
- ## There isn't any output in terminal when browsing websites
  This could be caused by two reasons, the first one is that you forgot to change your scope to the current target. The second one could be that the Extension is switched off because it couldn't connect to the HTTP server. You can turn on the Extension by clicking on the Extension icon in Chrome, navigating to the settings tab and clicking on the Extension switch. Make sure that `http_server.py` is running before doing this or it will simply switch off again after a couple of seconds.
  
- ## `http-server.py` can't find `linkfinder.py`
  `http-server.py` requires `linkfinder.py`, you can clone LinkFinder from the main branch. You also need to set the LinkFinder path variable in the `http-server.py` script. You can put `linkfinder.py` in the Extension's folder if you don't want to do this.

# Upcoming Features
- Listening on different ports than just `8080`

# Final Notes
- This is still in development stage and there might be some bugs or imperfections. Feel free to submit an issue whenever you find one.
