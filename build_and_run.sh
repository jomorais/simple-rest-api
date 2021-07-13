python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
coverage run --source=. -m pytest test/
coverage report
coverage html
python3 main.py