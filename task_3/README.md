This script performs:
- Basic functions verification of a currency converter with a help of Selenium WebDriver.

Usage:

```
# git clone https://github.com/AlexanderKoryagin/tasks.git
# cd task_3
# sudo pip install -U -r requirements.txt
# py.test --junit-xml reports/junit_report.xml --alluredir ./reports -k test_converter.py -v
```

To install `pip` on Ubuntu 14:
```
# sudo apt-get update
# sudo apt-get install python-pip python-dev build-essential
# sudo pip install -U pip
```

`JUnit` and `Yandex.Allure` reports will be placed here:
```
# ls -alph ./reports
```

Also you can add more variants for test customization in following file:
```
params.csv
```
