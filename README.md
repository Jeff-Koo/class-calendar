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

## Maybe using Docker
```
docker compose build
```
```
docker compose up -d
```
