c:\Python34\python34 c:\Python34\Tools\Scripts\pyvenv.py VENV
cd VENV
scripts\activate
pip install -r /path/to/requirements.txt
http://stackoverflow.com/questions/7225900/how-to-pip-install-packages-according-to-requirements-txt-from-a-local-directory
http://stackoverflow.com/a/22046133

makemigrations IT_FORUM
migrate --fake-initial
migrate
loaddata initial_data.json