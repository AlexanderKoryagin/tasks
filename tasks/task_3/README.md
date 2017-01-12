This script performs:
- Basic functions verification of a currency converter with a help of Selenium WebDriver.
***

Usage:
1. Install local requirements in addition to [global requirements](../../README.md):
```bash
cd tasks/task_3
pip install -U -r t3_requirements.txt
```
2. Run tests:
```bash
py.test --junit-xml reports/junit_report.xml --alluredir ./reports/ -k test_converter.py -v
```

`JUnit` and `Yandex.Allure` reports will be placed here:
```bash
ls -alph ./reports
```

Also you can add more variants for test customization in following file:
```bash
params.csv
```
