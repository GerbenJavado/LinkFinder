<img src="https://user-images.githubusercontent.com/18099289/62728809-f98b0900-ba1c-11e9-8dd8-67111263a21f.png" width=650px>

## About LinkFinder

LinkFinder is a python script written to discover endpoints and their parameters in JavaScript files. This way penetration testers and bug hunters are able to gather new, hidden endpoints on the websites they are testing. Resulting in new testing ground, possibility containing new vulnerabilities. It does so by using [jsbeautifier](https://github.com/beautify-web/js-beautify) for python in combination with a fairly large regular expression. The regular expressions consists of four small regular expressions. These are responsible for finding:

- Full URLs (`https://example.com/*`)
- Absolute URLs or dotted URLs (`/\*` or `../*`)
- Relative URLs with at least one slash (`text/test.php`)
- Relative URLs without a slash (`test.php`)

The output is given in HTML or plaintext. [@karel_origin](https://twitter.com/karel_origin) has written a Chrome extension for LinkFinder which can be found [here](https://github.com/GerbenJavado/LinkFinder/tree/chrome_extension).

## Screenshots

![LinkFinder](https://i.imgur.com/JfcpYok.png "LinkFinder in action")

## Installation

LinkFinder supports **Python 3**.

```
$ git clone https://github.com/GerbenJavado/LinkFinder.git
$ cd LinkFinder
$ python setup.py install
```

## Dependencies

LinkFinder depends on the `argparse` and `jsbeautifier` Python modules. These dependencies can all be installed using [pip](https://pypi.python.org/pypi/pip).

```
$ pip3 install -r requirements.txt
```

## Usage

Short Form    | Long Form     | Description
------------- | ------------- |-------------
-i            | --input       | Input a: URL, file or folder. For folders a wildcard can be used (e.g. '/*.js').
-o            | --output      | "cli" to print to STDOUT, otherwise where to save the HTML file Default: output.html
-r            | --regex       | RegEx for filtering purposes against found endpoints (e.g. ^/api/)
-d            | --domain      | Toggle to use when analyzing an entire domain. Enumerates over all found JS files.
-b            | --burp        | Toggle to use when inputting a Burp 'Save selected' file containing multiple JS files
-c            | --cookies     | Add cookies to the request
-h            | --help        | show the help message and exit

### Examples

* Most basic usage to find endpoints in an online JavaScript file and output the HTML results to results.html:

`python linkfinder.py -i https://example.com/1.js -o results.html`

* CLI/STDOUT output (doesn't use jsbeautifier, which makes it very fast):

`python linkfinder.py -i https://example.com/1.js -o cli`

* Analyzing an entire domain and its JS files:

`python linkfinder.py -i https://example.com -d`

* Burp input (select in target the files you want to save, right click, `Save selected items`, feed that file as input):

`python linkfinder.py -i burpfile -b`

* Enumerating an entire folder for JavaScript files, while looking for endpoints starting with /api/ and finally saving the results to results.html:

`python linkfinder.py -i 'Desktop/*.js' -r ^/api/ -o results.html`

## Docker

* Build the Docker image:

  ``` docker build -t linkfinder```

* Run with Docker

  ` docker run --rm -v $(pwd):/linkfinder/output linkfinder -i http://example.com/1.js -o /linkfinder/output/output.html`

  Make sure to use the path `/linkfinder/output` in your output path, or the output will be lost when the container exits.

## Unit-test

* Require pytest

`pytest test_parser.py`

## Final remarks
- This is the first time I publicly release a tool. Contributions are much appreciated!
- LinkFinder is published under the [MIT License](https://github.com/GerbenJavado/LinkFinder/blob/master/LICENSE).
- Thanks to [@jackhcable](https://twitter.com/jackhcable) for providing me with feedback.
- Special thanks [@edoverflow](https://twitter.com/edoverflow) for making this project a lot cleaner and awesome.
