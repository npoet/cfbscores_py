# cfbscores_py

 Simple FastAPI service that returns aggregations of College Football data.
 
### Install

#### MacOS
* Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
* `brew install python`
* `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
* `python3 get-pip.py`
* From cfbscores dir: `pip install -r requirements.txt`
### Run
* From cfbscores dir: `uvicorn main:app --reload`
runs app and updates on changes