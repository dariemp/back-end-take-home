# HOW TO RUN

## Clone the repository

`git clone https://github.com/dariemp/back-end-take-home.git`

## Create a Python 3 virtual environment with Conda or Virtualenv

- With Conda: `conda create -n venv python=3.7`

- With Virtualenv:  `virtualenv venv -p <path/to/python3.7/interpreter>`

## Activate your virtual environment

- With Conda: `conda activate venv`

- With Virtualenv: `source venv/bin/activate`

## Install dependencies in your virtualenv

`cd back-end-take-home`

`pip install -r requirements.txt`

## Change to src directory

`cd src`

## Run the main app specifying the listening port

`PORT=8000 python main.py`

## Test the app

`curl 'http://127.0.0.1:8000/route?origin=YYZ&destination=MEL'`

or using any other HTTP client. You can also use it hosted at **<https://route-flights.herokuapp.com/route>**:

`curl 'https://route-flights.herokuapp.com/route?origin=YYZ&destination=MEL'`

IMPORTANT NOTICE: the hosted app is using Heroku free tier which may take some time to "warm up" the container before being able to serve HTTP requests.
