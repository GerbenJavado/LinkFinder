## About LinkFinder
LinkFinder is a python script written to discover endpoints and their parameters in JavaScript files. This way penetration testers and bug hunters are able to gather new, hidden endpoints on the websites they are testing. Resulting in new testing ground, possibility containing new vulnerabilities. It does so by using [jsbeautifier](https://github.com/beautify-web/js-beautify) for python in combination with a fairly large regular expression. The regular expressions consists of four small regular expressions. These are responsible for finding: 
- Full URLs (https://example.com/*)
- Absolute URLs or dotted URLs (/\* or ../*)
- Relative URLs with atleast one slash (text/test.php) 
- Relative URLs without a slash (test.php)

The output is given in HTML. [Karel_origin](https://twitter.com/karel_origin) has written a chrome extension for LinkFinder which can be found [here](https://github.com/GerbenJavado/LinkFinder/tree/chrome_extension).

## Screenshots

![LinkFinder](https://i.imgur.com/JfcpYok.png "LinkFinder in action")


## Installation

LinkFinder supports **Python 2 & 3**.

```
$ git clone https://github.com/GerbenJavado/LinkFinder.git
$ cd LinkFinder
$ python setup.py install
```

## Dependencies

LinkFinder depends on the `requests`, `argparse`, `jsbeautifier` and `requests-file` python modules. These dependencies can all be installed using [pip](https://pypi.python.org/pypi/pip). 

## Usage

Short Form    | Long Form     | Description
------------- | ------------- |-------------
-i            | --input       | Input a: URL, file or folder. For folders a wildcard can be used (e.g. '/*.js').
-o            | --output      | Where to save the file, including file name or output to CLI. Default: output.html
-r            | --regex       | RegEx for filtering purposes against found endpoints (e.g. ^/api/)
-b            | --burp        | Toggle to use when inputting a Burp 'Save selected' file containing multiple JS files
-c            | --cookies     | Add cookies to the request
-h            | --help        | show the help message and exit

### Examples

* Most basic usage to find endpoints in an online JavaScript file and output the results to results.html:

``python linkfinder.py -i https://example.com/1.js -o results.html``

* CLI ouput (doesn't use jsbeautifier, which makes it very fast):

`python linkfinder.py -i https://example.com/1.js -o cli`

* Burp input (select in target the files you want to save, right click, `Save selected items`, feed that file as input):

`python linkfinder.py -i burpfile -b`

* Enumerating an entire folder for JavaScript files, while looking for endpoints starting with /api/ and finally saving the results to results.html:

``python linkfinder.py -i 'Desktop/*.js' -r ^/api/ -o results.html``

## Final remarks
- Due to the way python handles string concatenation the beautifying of the JavaScript can take ages.
- This is the first time I publicly release a tool. Contributions are much appreciated!
- LinkFinder is published under the [MIT License](https://github.com/GerbenJavado/LinkFinder/blob/master/LICENSE).
- Thanks to [@jackhcable](https://twitter.com/jackhcable) for providing me with feedback.
- Special thanks [@edoverflow](https://twitter.com/edoverflow) for making this project a lot cleaner and awesome.
