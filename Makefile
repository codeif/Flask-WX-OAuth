build:
	docker build -t flask-wx-oauth .

run:
	docker run -v "$(pwd):/app" -p 5000:5000 flask-wx-oauth