<div align="center">

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/) ![Python](https://img.shields.io/badge/Python-3.10-blue.svg) [![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-3.14-blue.svg)](https://www.django-rest-framework.org/) ![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

</div>

# Easy Charge

Easy Charge is a credit management service for SIM card resellers, where resellers submit requests for credit top-up. After approval by the system administrator, their account balance is increased. They can then sell the required credit to their customers.

This project implementation uses [CookieCutter](https://github.com/cookiecutter/cookiecutter-django).

**It is also worth mentioning that this project has been designed and implemented for educational purposes.**


## Installation

After downloading the project, simply run the following commands in the project folder.

```bash
$ docker compose -f docker-compose.local.yml build
$ docker compose -f docker-compose.local.yml up
```
