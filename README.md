# Open Meteo - WagaLabs Test Assignment

# Table of Contents
- [Installation and Running](#installation-and-running)
  - [For development](#for-development)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running](#running)
  - [For production](#for-production)
    - [Prerequisites](#prerequisites-1)
    - [Installation](#installation-1)
    - [Running](#running-1)
- [CLI Usage](#cli-usage)
  - [Weather](#weather)
    - [Help](#help)
    - [Example](#example)
- [API Documentation](#api-documentation)
- [Test Assignment Description](#test-assignment-description)

# Installation and Running
## For development
### Prerequisites
- Python 3.11
- Poetry

### Installation
```zsh
poetry install
pre-commit install
cat env_sample > .env
echo "DJANGO_SETTINGS_MODULE=app.settings.local" >> .env
dj migrate
```

### Running
```zsh
dj runserver
```

## For production
### Prerequisites
- Docker
- Docker Compose

### Installation
```bash
cat env_sample > .env  # change the values
```

### Running
```bash
docker-compose up -d
```

# CLI Usage
## Weather
### Help
```bash
dj weather --help
```
| Argument    | Description                      | Required |
|-------------|----------------------------------|----------|
| city_name   | City name.                       | True     |
| start_date  | Start date in format YYYY-MM-DD. | True     |
| end_date    | End date in format YYYY-MM-DD.   | True     |
| {json,csv}  | Output format                    | False    |

### Example
```bash
# by default it will output in csv format
dj weather "New York" 2021-01-01 2021-01-02
```
```bash
# you can specify the output format
dj weather "New York" 2021-01-01 2021-01-02 json
```

# API Documentation
You can check the API documentation at [`api/v1/docs/`](https://open-meteo.shaggy-dev.com/api/v1/docs/) endpoints.
## Weather
### List - [`api/v1/meteo/weather/`](https://open-meteo.shaggy-dev.com/api/v1/meteo/weather/)
list of weather data for a place specified as a parameter (if city not found, it will return 404, it's not a cli command)
- **Method:** `GET`
- **Query Params:**
  - `city` - City name. *(required)*
  - `startDate` - Start date in format YYYY-MM-DD.
  - `endDate` - End date in format YYYY-MM-DD.
#### Request
```zsh
curl -X 'GET' \
  'https://open-meteo.shaggy-dev.com/api/v1/meteo/weather/?city=New%20York&startDate=2021-01-01&endDate=2021-01-02' \
  -H 'accept: application/json'
```
#### Response
```json
[
  {
    "city": "New York",
    "date": "2023-05-08",
    "measured": {
      "temperature2mMax": "20.30",
      "temperature2mMin": "11.20",
      "precipitationSum": "0.60",
      "windspeed10mMax": "12.20"
    },
    "forecast": null
  },
  {
    "city": "New York",
    "date": "2023-05-11",
    "measured": {
      "temperature2mMax": "20.30",
      "temperature2mMin": "11.20",
      "precipitationSum": "0.60",
      "windspeed10mMax": "12.20"
    },
    "forecast": {
      "temperature2mMax": "20.30",
      "temperature2mMin": "11.20",
      "precipitationSum": "0.60",
      "windspeed10mMax": "12.20"
    }
  }
]
```

### Differences - [`api/v1/meteo/weather/differences/`](https://open-meteo.shaggy-dev.com/api/v1/meteo/weather/differences/)
differences between the forecast and measured values for this place
- **Method:** `GET`
- **Query Params:**
  - `city` - City name. *(required)*
  - `startDate` - Start date in format YYYY-MM-DD.
  - `endDate` - End date in format YYYY-MM-DD.
#### Request
```zsh
curl -X 'GET' \
  'https://open-meteo.shaggy-dev.com/api/v1/meteo/weather/differences/?city=New%20York&startDate=2021-01-01&endDate=2021-01-02' \
  -H 'accept: application/json'
```
#### Response
```json
[
  {
    "city": "New York",
    "date": "2023-05-11",
    "temperature_2m_max_diff": "0.00",
    "temperature_2m_min_diff": "0.00",
    "precipitation_sum_diff": "0.00",
    "windspeed_10m_max_diff": "0.00"
  }
]
```


# Test Assignment Description
A CLI command for weather data from https://open-meteo.com/en/docs for a place specified as a parameter (as a place name, not longitude/latitude), with starting date and ending date. The command should return the data in the CSV format: place name, date, min temperature, max temperature, max wind speed, precipitation sum, measured/forecast. That last column should indicate whether the entry was measured or it is a forecast (it is up to you to decide how to determine this). Note that the code should be structured in a way that allows relatively easy switching to a new weather data provider in the future.


Given a large CSV dataset from the above task (stored locally as a file), provide a (locally-run) REST web service that accepts the place name as a query parameter and returns differences between the forecast and measured values for this place, in a JSON format of your choice. The service should return the differences for any date that in the CSV dataset has both the forecast and measured values, the other dates can be skipped/ignored.


The code should be reasonably covered by automatic tests. Also, all the inputs (both from the user and the external web services) should be validated. You can use any frameworks and tools from the Python ecosystem you feel comfortable with. The code/solution should be documented well enough for the interviewers to be able to build it and use the provided components without additional feedback from you.

Bonus points for:
- Using SQLite instead of CSV file in both tasks
- A build script that can be run from the command line and runs the tests