cd D:\english\path\to\project-folder\event-calendar
docker compose down
docker image pull <docker-repository>/<image>:<tag>
docker compose up -d
timeout 10
docker restart django_container
timeout 15
start "firefox.exe" http://127.0.0.1:8000
