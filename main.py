import pyodbc
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import uuid
from datetime import datetime

def log_message(message):
    print(f"[LOG] {message}")

try:
    # Set up Selenium WebDriver
    log_message("Setting up Selenium WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    driver = webdriver.Chrome(options=chrome_options)  # Ensure you have the appropriate WebDriver installed
    driver.get("http://172.34.0.4:3000/")  # Replace with your OpenSpeedTest URL

    # Start the speed test
    log_message("Starting the speed test...")
    start_button = driver.find_element(By.ID, "startButtonDesk")  # Replace with the actual element ID
    start_button.click()

    # Wait for the test to complete
    time.sleep(60)  # Adjust the time according to the test duration

    # Get the page source
    log_message("Retrieving the page source...")
    page_source = driver.page_source

    # Parse the page source using BeautifulSoup
    log_message("Parsing the page source...")
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract the download speed
    download_speed = soup.find('symbol', {'id': 'downResultC1'}).find('text', {'class': 'rtextnum'}).text
    log_message(f"Download Speed: {download_speed} Mbps")

    # Extract the upload speed
    upload_speed = soup.find('symbol', {'id': 'upResultC2'}).find('text', {'class': 'rtextnum'}).text
    log_message(f"Upload Speed: {upload_speed} Mbps")

    # Extract the ping
    ping = soup.find('symbol', {'id': 'pingResultC3'}).find('text', {'class': 'rtextnum'}).text
    log_message(f"Ping: {ping} ms")

    # Extract the jitter
    jitter = soup.find('symbol', {'id': 'jitterResultC3'}).find('text', {'class': 'rtextnum'}).text
    log_message(f"Jitter: {jitter} ms")

    # Generate a unique ID and get the current date and time
    unique_id = str(uuid.uuid4())
    process_date = datetime.now().strftime('%Y-%m-%d')
    process_time = datetime.now().strftime('%H:%M:%S')

    log_message(f"Generated Unique ID: {unique_id}")
    log_message(f"Process Date: {process_date}, Process Time: {process_time}")

    # Close the WebDriver
    log_message("Closing the WebDriver...")
    driver.quit()

    try:
        # Connect to the MSSQL database
        log_message("Connecting to the MSSQL database...")
        conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=ZW-SQL\MSSQLSERVERSYB;'
        'DATABASE=Nitro;'
        'UID=sa;'
        'PWD=Password01;'
        )
        cursor = conn.cursor()

        # Insert the data into the speedtest table
        log_message("Inserting data into the speedtest table...")
        cursor.execute("""
            INSERT INTO speedtest (id, download_speed, upload_speed, ping, jitter, processdate, processtime)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, unique_id, download_speed, upload_speed, ping, jitter, process_date, process_time)

        # Commit the transaction
        log_message("Committing the transaction...")
        conn.commit()

    except pyodbc.Error as db_err:
        log_message(f"Database error: {db_err}")

    finally:
        # Close the database connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        log_message("Database connection closed.")

except Exception as e:
    log_message(f"An error occurred: {e}")

finally:
    try:
        driver.quit()
    except Exception as e:
        log_message(f"Error closing WebDriver: {e}")
