c:\Python34\python34 c:\Python34\Tools\Scripts\pyvenv.py VENV
cd VENV
scripts\activate
pip install -r /path/to/requirements.txt

makemigrations IT_FORUM
migrate --fake-initial
migrate
loaddata initial_data.json