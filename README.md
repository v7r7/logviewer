# LogViewer

LogViewer is a simple Django web application for on-demand monitoring of Unix-based servers' log files. It allows users to retrieve log lines from specified log files and directories without having to log into individual machines manually. LogViewer is built with Python 3.9 and Django.

## Requirements

- Python 3.9
- [pip](https://pip.pypa.io/en/stable/installation/) (Python package manager)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/v7r7/logviewer.git
   cd logviewer
   ```

2. Initialize your virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **On Unix or MacOS:**

     ```bash
     source venv/bin/activate
     ```

4. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the development server:

   ```bash
   python manage.py runserver
   ```

2. Access the local server in your web browser at [http://127.0.0.1:8000](http://127.0.0.1:8000). The API endpoint for retrieving log files is [http://127.0.0.1:8000/api/logs/](http://127.0.0.1:8000/api/logs/).

## Running Tests

To run the tests for the LogViewer application, use the following command:

```bash
python manage.py test tests.logapi_test
```

To run a single test specify the path of the test, such as in the following command

```bash
python manage.py test tests.logapi_test.LogApiTestCase.test_log_api_case_insensitive
```

## API Documentation

### `GET /api/log/`

This endpoint allows you to retrieve log lines from a specified log file. The log file can be selected based on the provided parameters.  Empty lines are omitted.

#### Parameters

- **`filename`**: The name of the log file to read.
- **`keyword` (optional)**: A keyword to filter log lines. The filter is case insensitive by default.  Only lines containing this keyword will be returned. If not provided, all lines will be returned.
- **`c` (optional)**: Specify any value (such as 1) to enable case sensitive keyword search.  Defaults to case insensitive search.
- **`n` (optional)**: The number of log lines to retrieve. Defaults to 100 if not provided.  Maximum of 50000 lines.

#### Example Request

```
GET /api/log/?filename=mylog.log&keyword=ERROR&n=50
```

#### Example Response

```json
{
  "lines": 50,
  "logs": [
    "2023-10-20 14:30:12 - ERROR: Something went wrong",
    "2023-10-20 14:31:05 - ERROR: Another error occurred"
    // ... 48 more lines
  ]
}
```

---

### `GET /api/logs/`

This endpoint allows you to retrieve a list of log files with .txt and .log extensions available in /var/log directory

#### Example Request

```
GET /api/logs/
```

#### Example Response

```json
{
  "files": [
    "access.log",
    "error.log",
    "system.log",
    "custom.log"
  ]
}
```

---

**Note**: 
- For the `/api/log/` endpoint, the response contains the specified number of log lines (`n`) from the selected log file that match the provided keyword. If no keyword is provided, all lines are returned. If the file is empty or does not exist, an empty response is returned.
- For the `/api/logs/` endpoint, the response contains a list of log files available in the system with .txt or .log extensions. If no log files are found, an empty list is returned.
- We assume all files being read are encoded in UTF-8.