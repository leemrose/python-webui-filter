# python-webui-filter
Requirement :

Automate tests for filters on product list page

Websites: www.aldoshoes.com, www.callitspring.com
Use case: As a user I would like to use filters to see the products as per the filters selected

Apply filters and validate selected filter(s) is applied in 2 ways, validate applied filters
count.

Write data driven tests for the filter combinations
Same test(s) should be able to run on both websites with proper parameterization

Language: Python
Test framework: Pytest
Add any dependencies required in the project

Required Installations:
=======================

********To install selenium for webdriver ui test********
python -m pip install selenium

download chromedriver from here based on your system's configuration
https://sites.google.com/a/chromium.org/chromedriver/

refer the driver path in your script to load url on the browser.

********To install pytest********
pip install -U pytest

********To read excel input data install openpxl********
pip install openpyxl

********To view report in html format********
pip install pytest-html 

Command to run the test:
C:\Users\<user>\python-webui-filter> pytest .\aldo_filter_validation_tool.py

Command to run the test in debug mode:
pytest -v .\aldo_filter_validation_tool.py

Comment to run test and get the html report:
pytest .\aldo_filter_validation_tool.py --html="./ALDO-FILTER-VALIDATION-TEST-REPORT.html"

Screen shot of command run results on console:
https://github.com/leemrose/python-webui-filter/blob/main/Aldo-filter-run-result-screen-shot.JPG

Sample test input Format in excel:
https://github.com/leemrose/python-webui-filter/blob/main/screen-shot-for-test-data-set-in-excel.JPG

HTLM REPORT for the test run : https://github.com/leemrose/python-webui-filter/blob/main/ALDO-FILTER-VALIDATION-TEST-REPORT.html

