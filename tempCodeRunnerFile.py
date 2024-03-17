import speedtest
import math
import time
from datetime import datetime
import requests
import sqlite3

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

    sql = ''' INSERT INTO speed_tests(download_speed, upload_speed, response_time, test_date)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (download_speed, upload_speed, response_time, test_date))
    conn.commit()
    return cur.lastrowid
    

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
    wifi = speedtest.Speedtest()
    while True:
        
        download_speed = wifi.download()
        upload_speed = wifi.upload()
        response_time = test_google_connection()
        
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Download: ", bytes_to_mb(download_speed))
        print("Upload: ", bytes_to_mb(upload_speed))
    
        insertTest(conn,download_speed, upload_speed, response_time)
        
        print("30 seconds till next test\n")
        time.sleep(30)
        
        
except KeyboardInterrupt:
    print("Exiting")
    
if conn:
    conn.close()
    print("Database connection closed")
    
    