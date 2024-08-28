from flask import Flask, jsonify, request
import pyodbc
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import uuid
from datetime import datetime

app = Flask(__name__)

def log_message(message):
    print(f"[LOG] {message}")

@app.route('/run-speedtest', methods=['GET'])
def run_speedtest():
    try:
        # Set up Selenium WebDriver
        log_message("Setting up Selenium WebDriver...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://172.34.0.4:3000/")  # Replace with your OpenSpeedTest URL

        # Start the speed test
        log_message("Starting the speed test...")
        start_button = driver.find_element(By.ID, "startButtonDesk")
        start_button.click()

        # Wait for the test to complete
        time.sleep(60)

        # Get the page source
        log_message("Retrieving the page source...")
        page_source = driver.page_source

        # Parse the page source using BeautifulSoup
        log_message("Parsing the page source...")
        soup = BeautifulSoup(page_source, 'html.parser')

        download_speed = soup.find('symbol', {'id': 'downResultC1'}).find('text', {'class': 'rtextnum'}).text
        upload_speed = soup.find('symbol', {'id': 'upResultC2'}).find('text', {'class': 'rtextnum'}).text
        ping = soup.find('symbol', {'id': 'pingResultC3'}).find('text', {'class': 'rtextnum'}).text
        jitter = soup.find('symbol', {'id': 'jitterResultC3'}).find('text', {'class': 'rtextnum'}).text

        unique_id = str(uuid.uuid4())
        process_date = datetime.now().strftime('%Y-%m-%d')
        process_time = datetime.now().strftime('%H:%M:%S')

        log_message(f"Generated Unique ID: {unique_id}")
        log_message(f"Process Date: {process_date}, Process Time: {process_time}")

        # Close the WebDriver
        log_message("Closing the WebDriver...")
        driver.quit()

        # Connect to the MSSQL database and insert the data
        try:
            log_message("Connecting to the MSSQL database...")
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=ZW-SQL\MSSQLSERVERSYB;'
                'DATABASE=Nitro;'
                'UID=sa;'
                'PWD=Password01;'
            )
            cursor = conn.cursor()
            log_message("Inserting data into the speedtest table...")
            cursor.execute("""
                INSERT INTO speedtest (id, download_speed, upload_speed, ping, jitter, processdate, processtime)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, unique_id, download_speed, upload_speed, ping, jitter, process_date, process_time)

            conn.commit()

        except pyodbc.Error as db_err:
            log_message(f"Database error: {db_err}")
            return jsonify({"status": "error", "message": str(db_err)}), 500

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            log_message("Database connection closed.")

        return jsonify({
            "status": "success",
            "download_speed": download_speed,
            "upload_speed": upload_speed,
            "ping": ping,
            "jitter": jitter,
            "id": unique_id,
            "process_date": process_date,
            "process_time": process_time
        })

    except Exception as e:
        log_message(f"An error occurred: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        try:
            driver.quit()
        except Exception as e:
            log_message(f"Error closing WebDriver: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
