# HOW TO RUN

## Clone the repository

`git clone https://github.com/dariemp/back-end-take-home.git`

## Change to src directory

`cd src`

## Run the main app specifying the listening port

`PORT=8000 python main.py`

## Test the app

`curl 'http://127.0.0.1:8000/route?origin=YYZ&destination=MEL'`

or using any other HTTP client. You can also use it hosted at **<https://route-flights.herokuapp.com/route>**:

`curl 'https://route-flights.herokuapp.com/route?origin=YYZ&destination=MEL'`

IMPORTANT NOTICE: the hosted app is using Heroku free tier which may take some time to "warm up" the container before being able to serve HTTP requests.
