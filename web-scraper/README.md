## Web-scraper
1. Install chrome and chromedriver for linux under Dev from https://googlechromelabs.github.io/chrome-for-testing/
2. Unzip the folders into the web-scraper directory
3. Navigate to the web-scraper diretory
``` bash
cd web-scraper
```
4. Install the selenium bindings
``` bash
python -m venv .venv
source .venv/bin/activate
pip install selenium
```
5. Run the script 
``` bash
python main.py
```

You should only run the script when the web server is running, so do that first, you may need to change the URL that the driver gets from to wtv the URL is supposed to be. 

In the web server's console logs, you should see the alerts that it triggers. 
