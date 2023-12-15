# cfbscores_py

 Simple FastAPI service that returns aggregations of live and scheduled sports data for [cfbscores_react](https://github.com/npoet/cfbscores_react).
 
### Install

#### Prereqs:
* Python3.x
* python-pip
* uvicorn

From cfbscores dir: `pip install -r requirements.txt`

### Run
* From cfbscores dir: `uvicorn main:app`
* API listens at localhost:8000, changing this port/address requires changing spec in cfbscores_react