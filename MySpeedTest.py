import speedtest
import math
import time
from datetime import datetime
import requests
import sqlite3

def preform_Speed_Test():
    try:
        wifi = speedtest.Speedtest()
        download_speed = wifi.download()
        upload_speed = wifi.upload()
        download_speed_mbps = bytes_to_mb(download_speed)
        upload_speed_mbps = bytes_to_mb(upload_speed)
        return download_speed, upload_speed
    except Exception as e:
        print(f"Speed test failed: {e}")
        return None, None

def create_table(conn):
    """Create the table if it doesn't already exist."""
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS speed_tests (
                id INTEGER PRIMARY KEY,
                download_speed REAL,
                upload_speed REAL,
                response_time REAL,
                test_date TEXT
            );
        ''')
    except sqlite3.Error as e:
        print(e)
        
def createConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def insertTest(conn, download_speed, upload_speed, response_time):
    test_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if response_time is not None:
        response_time = round(response_time, 2)  # Round to the nearest two decimal places
    try:
        sql = ''' INSERT INTO speed_tests(download_speed, upload_speed, response_time, test_date)
                VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (download_speed, upload_speed, response_time, test_date))
        conn.commit()
        print(f"Test results inserted successfully: {cur.lastrowid}")
    except sqlite3.Error as e:
        print(f"Error inserting test results: {e}")
    

def bytes_to_mb(size_bytes):
    i = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, i)
    size = round(size_bytes / power, 2)
    return f"{size} {['B', 'KB', 'MB', 'GB', 'TB'][i]}"
    
def test_google_connection():
    try:
        start_time = time.time()
        response = requests.get("http://www.google.com", timeout=5)
        elapsed_time = time.time() - start_time
        if response.status_code == 200:
            print("Google is connected")
            print("Response time: ", elapsed_time)
            return elapsed_time
        else:
            print("Failed to connect to Google, but response received.")
            return None
    except requests.RequestException as e:
        print("Google is not connected")
        print("Error: ", e)
        return None   

database = "speed_tests.db"
conn = createConnection(database)
if conn:
    create_table(conn)


try:
    while True:
        # Initialize default values for speeds
        download_speed_mbps = 0  # Default value indicating test failure or not performed
        upload_speed_mbps = 0    # Default value indicating test failure or not performed

        # Attempt to perform the speed test
        download_speed, upload_speed = preform_Speed_Test()
        
        # Check if speed test was successful
        if download_speed is not None and upload_speed is not None:
            download_speed_mbps = bytes_to_mb(download_speed) # Assuming this is already in Mbps
            upload_speed_mbps = bytes_to_mb(upload_speed)      # Assuming this is already in Mbps
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(f"Download speed: {download_speed_mbps} Mbps")
            print(f"Upload speed: {upload_speed_mbps} Mbps")
        else:
            print("Speed test failed, using default values for speeds.")
        
        # Perform Google connectivity test
        response_time = test_google_connection()
        if response_time is not None:
            response_time = round(response_time, 2)

        # Insert the results into the database
        insertTest(conn, download_speed_mbps, upload_speed_mbps, response_time if response_time is not None else 0)
        
        print("10 seconds till next test\n")
        time.sleep(10)
        
        
except KeyboardInterrupt:
    print("Exiting")
    
if conn:
    conn.close()
    print("Database connection closed")
    
    