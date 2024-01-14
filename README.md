### Development
## How To Setup
```
git clone https://gitlab.com/f9602451/event-calendar.git
```
```
cd event-calendar
```
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r requirements.txt
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
```
python manage.py createsuperuser
```
```
python manage.py runserver
```

When DEBUG=False, use `--insecure` flag for getting the static files
```
python manage.py runserver --insecure
```

## Using Docker to Build and Run
build Docker image
```
docker compose build calendar-app
```
start Docker containers for application
```
docker compose up -d
```

### Deployment
## Developer: Using Docker to Build and Push Image to Repository
```
docker compose build calendar-app
```
```
docker images
```
```
docker image tag <image-id> <docker-repository>/<image>:<tag>
```
```
docker image push <docker-repository>/<image>:<tag>
```

## Client: Pulling Docker Image from Repository and Startup
1. Ensure Docker Desktop Application is running in Windows
2. Configurate the `startDockerCalendar.bat` file, 
    - replace `<path\to\event-calendar>` with the path of current folder  
    - set `<docker-repository>/<image>:<tag>` which provided by developer 
3. Double click `startDockerCalendar.bat` and wait until it finish (P.S. `startDockerCalendar.bat` can be put to Desktop or anywhere)
4. If browser does not open automatically, open browser and go to 127.0.0.1:8000 
