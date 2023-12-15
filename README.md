# cfbscores_py

Simple FastAPI service that returns aggregations of live and scheduled sports data for [cfbscores_react](https://github.com/npoet/cfbscores_react). 
Links live games to FuboTV and other online providers for easy multi-boxing.
 
### Install

#### Prereqs:
* Python3.x
* python-pip
* uvicorn
* Requires local env variable CFBD_API_KEY containing personal key for CollegeFootballData.com, can be acquired for free through their site

From cfbscores dir: `pip install -r requirements.txt`

### Run
* From cfbscores dir: `uvicorn main:app`
* API listens at localhost:8000, changing this port/address locally requires changing spec in cfbscores_react

### Data Sources
* Current data sources include:
  * ESPN.com for live/scheduled scores
  * CollegeFootballData.com for ratings and season statistics
* Current supported sports/divisions include:
  * FBS/FCS Football
  * NFL Football
  * D1 NCAA Basketball