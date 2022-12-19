# vk_final_project

The final project for a VK QA Automation Python course.

## Contents

The project consists of tests and the system it runs at.
The system is rolled out by docker-compose described in system/docker_compose.yml.
The system consists of App for testing, FastAPI VK ID Mock & MySQL database.

## Tests

Tests are written for UI, API & SQL. UI tests are in the test_ui directory, and API & SQL tests are in the test_api directory.
UI tests could be run via selenoid (chrome & firefox) and via local browser instance (also in headless mode).
All tests are covered with an Allure report. Tests could be run in multiple threads with pytest-xdist.

## Test command examples

```python
pytest test_ui -v -n2 --selenoid --vnc --alluredir=DIRECTORY_NAME
```

```python
pytest test_api -v -n2 --alluredir=DIRECTORY_NAME
```

## DevOps

The project is developed to run via Jenkins.
Configuration includes system boot up, tests execution, and system shutdown.
Each build iteration is independent and has its own Allure reports.

## Report

Notion and Miro report could be found here:
[Link](https://tmlnv.notion.site/VK-QA-Automation-Python-Final-Project-b04aab27088e408eb4c5ba70dbe21840).
