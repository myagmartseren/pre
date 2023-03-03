web:
	cd ./backend && python manage.py runserver 8080
ui:
	cd ./frontend && yarn dev -o
install:
	python3 -m venv env && source ./env/bin/activate && \
	pip install -r ./requirements.txt && \
	cd frontend && \
	yarn install
