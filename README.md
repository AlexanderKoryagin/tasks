### Different tasks.
***

Place to publish tasks execution.
- `other`  - Some random tasks.
- `task_1` - Script to calculate quality of work of a classifier.
- `task_2` - Test triangle.
- `task_3` - Verification of a web site with Selenium.

***

#### Preparations for Ubuntu 16:
```bash
sudo apt-get update
sudo apt-get install python-pip python-dev build-essential
sudo pip install -U pip setuptools virtualenv
virtualenv --clear .venv && source .venv/bin/activate
pip install -U -r requirements.txt
```
#### Preparations for Windows:
```
1. Download latest Python 2.x from www.python.org.
2. During installation enable action 'Add python.exe to Path'.
3. In CMD:
> python -m pip install -U pip setuptools virtualenv
> virtualenv --clear .venv
> .venv\Scripts\activate
> pip install -U -r requirements.txt

If you need proxy for CMD:
set http_proxy=http://<proxy_IP>:<proxy_port>
set https_proxy=http://<proxy_IP>:<proxy_port>
```
To run *only* Code Style checks:
```bash
flake8 tasks/
pylint tasks/
```
