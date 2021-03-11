# Django REST API with a cars database
API is publicly available at http://safe-river-29530.herokuapp.com/.

To deploy it locally, follow these steps:
* clone the repo and cd into its folder:
```
git clone https://github.com/BryanNemesis/cars_api.git
cd cars_api
```
* build and run the container using the included dockerfile. Use a randomly generated string for the key value (you can use http://www.unit-conversion.info/texttools/random-string-generator/):
```
docker build -t web:latest .
docker run -d --name cars_api -e "PORT=8765" -e "DEBUG=0" -e "SECRET_KEY=<key>" -p 8007:8765 web:latest gunicorn netguru_task.wsgi:application --bind 0.0.0.0:8765
```
The API will be accessible under http://localhost:8007/.
