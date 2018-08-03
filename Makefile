start:
	env/bin/python main.py
prepare:
	python3.6 -m venv env
	env/bin/python -m pip install -r requirements.txt
freeze:
	env/bin/python -m pip freeze | grep -v "pkg-resources" > requirements.txt
