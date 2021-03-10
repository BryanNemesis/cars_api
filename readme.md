# Django REST API with a cars database
To deploy the API locally, use commands:
```
docker build -t web:latest .
docker run -d --name cars_api -e "PORT=8765" -e "DEBUG=0" -e "SECRET_KEY=<key>" -p 8007:8765 web:latest gunicorn netguru_task.wsgi:application --bind 0.0.0.0:8765
```
For the key in the second command, use a randomly generated string, for example using http://www.unit-conversion.info/texttools/random-string-generator/.