# Global Energy Producers Database Application

This is a desktop application built with Python and Tkinter for managing a database of global energy producers. It allows for CRUD (Create, Read, Update, Delete) operations on producer records, search functionalities, data export (CSV, PDF), and integrates with the Google Gemini AI for intelligent suggestions, web searches, and natural language database queries.

## Features

* **Producer Management:** Add, update, delete, and view energy producer records.
* **Search & Filter:** Search producers by name or category.
* **Data Export:** Export current producer data to CSV or PDF files.
* **Data Import:** Import producer data from CSV or TXT files, with duplicate handling.
* **AI Integration (Google Gemini):**
    * **Smart Suggestions:** Get AI suggestions for producer categories and products when adding new records.
    * **AI Web Search:** Perform AI-powered web searches for company and product information.
    * **File Content Scan (AI-Powered):** Scan PDF, TXT, or CSV files to identify energy-related keywords and initiate AI-powered web searches for suppliers.
    * **Natural Language Database Query:** Ask questions about your database in plain English, and the AI will attempt to generate and execute SQL queries to provide answers.
* **Secure API Key Handling:** Your Gemini API key is encrypted and loaded securely at runtime, preventing it from being exposed directly in the code or repository.

## Screenshots

Example:
![Application Main Window]
![image](https://github.com/user-attachments/assets/4d452a36-a50a-48c2-8866-ba905096abd3)


## Setup and Installation
Follow these steps to get the application running on your Windows machine.

### 1. Prerequisites
* **Python 3.x:** Download and install Python from [python.org](https://www.python.org/downloads/windows/).
    * **IMPORTANT:** During installation, ensure you **check the "Add python.exe to PATH"** option.

### 2. Clone the Repository
First, clone this repository to your local machine:

```bash
git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
cd YourRepoName
(Replace YourUsername and YourRepoName with your actual GitHub username and repository name)

3. Install Python Dependencies
Navigate to your project directory in the Command Prompt and install the necessary libraries:

Bash

pip install google-generativeai pycryptodome reportlab PyPDF2
4. Configure and Encrypt Your Gemini API Key
For the AI features to work, you need a Google Gemini API key. This application encrypts your key for security.

Get Your Gemini API Key:

Visit Google AI for Developers.

Sign in with your Google account and generate a new API key. Copy this key.

Edit encrypt_key.py:

Open encrypt_key.py in a text editor.

Find the line:

Python

api_key = b'YOUR_GEMINI_API_KEY'  # must be in bytes
Replace YOUR_GEMINI_API_KEY with your actual API key. Ensure you keep the b' prefix and the single quotes.

Example: api_key = b'AIzaSyC...your_actual_key...'

The secret variable (secret = b'mysecretaeskey12') is the encryption key. For a real-world application, this should be a strong, randomly generated 16-byte key and kept highly secure (e.g., loaded from an environment variable). For this demonstration, ensure the secret in encrypt_key.py matches SECRET_KEY in app.py.

Save encrypt_key.py.

Generate Encrypted Key File:

In your Command Prompt, run the encrypt_key.py script:

Bash

python encrypt_key.py
This will create a file named encrypted_key.txt in your project directory. This file contains your encrypted API key, which app.py will use.

5. Run the Application
Now you can run the main application:

Bash

python app.py
The application GUI will appear, and you should see a confirmation in the console that the Gemini AI API was configured.

Creating a Standalone Executable (Windows)
You can package this application into a single executable file using PyInstaller, allowing others to run it without installing Python or its dependencies.

Install PyInstaller:

Bash

pip install pyinstaller
Generate and Edit the .spec file:
First, generate a basic spec file:

Bash

pyinstaller --onefile --windowed app.py
This creates app.spec in your project folder. Open app.spec in a text editor and make the following crucial modifications:

Hidden Imports: Add 'Crypto.Cipher._AES' to the hiddenimports list.

Data Files: Explicitly include your encrypted_key.txt and global_energy_db.sqlite files in the datas list.

Your Analysis section in app.spec should look similar to this (adjust pathex to your actual path):

Python

a = Analysis(
    ['app.py'],
    pathex=['C:\\Users\\YourUser\\Documents\\GlobalEnergyApp'], # Your project path
    binaries=[],
    datas=[
        ('encrypted_key.txt', '.'),      # Include encrypted key file
        ('global_energy_db.sqlite', '.') # Include database file
    ],
    hiddenimports=['Crypto.Cipher._AES'], # Essential for PyCryptodome
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
Save the app.spec file after editing.

Build the Executable:
In your Command Prompt, run PyInstaller using the spec file:

Bash

pyinstaller app.spec
Find the Executable:
The executable (app.exe) will be located in the dist folder within your project directory (e.g., YourRepoName/dist/app.exe).
