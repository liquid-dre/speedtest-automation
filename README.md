# Speed Test Automation Script

This project automates the process of running a network speed test, extracting results, and storing them in an MSSQL database. The script is implemented in Python using Selenium for browser automation, BeautifulSoup for parsing HTML, and pyodbc for database connectivity.

------------------------------------------------------------------------------------------------------------

### **Summary of the README:**
- **Project Title:** Provides the name and purpose of the project.
- **Prerequisites:** Lists the software and accounts required before installation.
- **Installation:** Provides step-by-step instructions on how to set up the project.
- **Usage:** Describes how to run the script and what it does.
- **Troubleshooting:** Offers solutions to common issues that might be encountered.
- **Contributing:** Invites others to contribute to the project.
- **License:** Specifies the project’s licensing terms.

------------------------------------------------------------------------------------------------------------

## Prerequisites

- Python 3.x
- Google Chrome and ChromeDriver installed
- MSSQL Server with an existing database named `Nitro`
- A GitHub account (for cloning the repository)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/speedtest-automation.git
   cd speedtest-automation

2. **Install Dependencies:**

Install the required Python packages using pip and the requirements.txt file:

    ```bash
    pip install -r requirements.txt

3. **Set Up ChromeDriver:**

- Download the ChromeDriver matching your version of Google Chrome from here : https://developer.chrome.com/docs/chromedriver/downloads.
- Ensure the chromedriver.exe is in your PATH or in the same directory as the script.

4. **Update the Script:**

- Replace the following placeholders in speedtest_script.py with your actual values:
    - URL of the speed test: http://your-given-servers-ip:your-given-port/
    - Database connection details:

    ```python
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=YourServerName;'
        'DATABASE=Nitro;'
        'UID=YourUsername;'
        'PWD=YourPassword;'
    )

## Usage

1. **Run the Script:**

- Execute the script using Python:

    ```bash
    python main.py

- The script will:

    - Open the specified speed test URL in headless mode.
    - Start the speed test and wait for it to complete.
    - Extract the download speed, upload speed, ping, and jitter results.
    - Insert the results into the speedtest table of the MSSQL Nitro database.

2. **Check Results:**

- Verify that the data has been correctly inserted into the speedtest table in your MSSQL database.

## Troubleshooting
    - WebDriver Issues:

        - Ensure ChromeDriver is compatible with your Chrome browser version.
        - If the script fails to find the start button or other elements, verify the element IDs and update them as needed.

    - Database Connection Errors:

        - Check your MSSQL connection details (server name, database name, username, password).
        - Ensure that the MSSQL server is running and accessible.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.