# BackgroundsForReddit
An OS x statusbar app that changes your background to pictures from your
favorite reddit subs!

## Installation
Run `./install-dependencies.sh` to install dependencies through
[homebrew](http://brew.sh/) and [pip](https://pip.pypa.io/en/stable/).

Run `./build-app.sh` to build the .app executable file to run the program.

## Requirements
Developer requirements
- python 2.7
- pip

Python pip dependencies:
praw
pyobjc-core
pyobjc
rumps
flufl.enum
pillow
urllib
py2app

## Running the app for developers

First add a secrets.py file to the src directory:

/src/secrets.py:
client_id='my client id from reddit'
client_secret='my client secret from reddit'

(this is needed to access the reddit API)

After this, simply run:

python ./src/app.py
