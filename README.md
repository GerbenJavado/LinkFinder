# LinkFinder Chrome Extension
This chrome extension feeds every JavaScript file loaded during browsing back to a Python script, which calls LinkFinder and outputs the results. The chrome extension allows for whitelisting domains making you able to only scan the domains you want results of. It uses the option `-o cli` in LinkFinder which makes the extension very fast and able to process multiple JavaScript files in a few seconds. This extension is made by [karel_origin](https://twitter.com/karel_origin)

# Setup
1. Clone this branch
2. Load the chrome extension (Extension folder) into chrome (chrome://extensions/) while being in `Developer Mode`
3. Edit the variable `path_linkfinder` in http-server.py to point to the directory where you installed LinkFinder.py
3. Run the Python script (`python http-server.py`), which will run a listener on port 8080
4. Open `Inspect` in Chrome and browse to a page
5. The found JavaScript files will appear in your terminal (http-server.py) and they will be run through LinkFinder

Optional:
Clicking the extension icon in Chrome allows you to add domains to the whitelist. You can remove domains from the whitelist by clicking on the title (LinkFinder) in the extension.

# Final Notes
- This is still in development stage and there might be some bugs or imperfections. Feel free to submit an issue whenever you find one.
