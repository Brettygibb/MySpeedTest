Internet Speed Monitoring Script
This script is designed to perform regular internet speed tests and monitor connectivity to a specified website (Google by default). It logs the results, including download speed, upload speed, response time, and test timestamp, into a SQLite database. This allows for long-term monitoring of internet service performance.

Features
Speed Testing: Utilizes the speedtest library to measure internet download and upload speeds.
Connectivity Check: Tests connectivity to Google and measures the response time.
Data Logging: Stores test results in a SQLite database for analysis and long-term performance monitoring.
Automatic Re-testing: Performs tests at regular intervals (every 10 seconds by default).
Prerequisites
Before you start using this script, ensure you have Python installed on your system (Python 3.6 or later is recommended). Additionally, you will need to install the following Python packages:

speedtest-cli
requests
sqlite3 (usually included with Python)
You can install the required packages using pip:

bash
Copy code
pip install speedtest-cli requests
Usage
To use this script, simply run it from your command line:

bash
Copy code
python path/to/script.py
The script will start performing speed tests and connectivity checks, logging the results to a SQLite database named speed_tests.db. The database and its table will be created automatically if they do not exist.

How It Works
Speed Test: The script uses the speedtest library to measure the current internet connection's download and upload speeds.
Connectivity Check: It attempts to connect to http://www.google.com and calculates the response time.
Logging: Results from the speed test and connectivity check, along with the timestamp, are logged into the speed_tests table in the speed_tests.db SQLite database.
Loop: The script waits for 10 seconds before repeating the tests.
Stopping the Script
To stop the script, simply interrupt the execution by pressing CTRL+C. The script will safely close the database connection before exiting.

Customization
You can customize the script by changing the connectivity test URL, adjusting the re-test interval, or modifying the database schema to fit your needs.
