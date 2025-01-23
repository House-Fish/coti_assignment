# coti_assignment

## Set-up
``` bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0 'app:app' --log-file logs/gunicorn.log
flask run --host 0.0.0.0 #to run main application for when segregating testing w the vms
```
