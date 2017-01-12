#### Description:
This script performs basic functions verification of a currency converter with a help of Selenium WebDriver.
***

#### Usage:
* Install local requirements in addition to [global requirements](../../README.md):
```bash
cd tasks/task_3
pip install -U -r t3_requirements.txt
```
* Run tests:
```bash
py.test --junit-xml reports/junit_report.xml --alluredir ./reports/ -k test_converter.py -v
```
#### Reports: 
`JUnit` and `Yandex.Allure` reports will be placed here:
```bash
ls -alph ./reports
```
#### Customization:
Also you can add more variants for test customization in following file:
```bash
params.csv
```
