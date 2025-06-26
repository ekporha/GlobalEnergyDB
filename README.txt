Guide: Global Energy Producers Database App on Windows
This guide covers installing prerequisites, setting up your Gemini API key with encryption, running the Python application, and creating a standalone executable for distribution.

1. Prerequisites: Install Python
If you don't have Python installed, follow these steps:

Download Python: Go to the official Python website: https://www.python.org/downloads/windows/

Run the Installer:

Download the latest stable version of Python for Windows (e.g., "Windows installer (64-bit)").

Run the downloaded .exe file.

IMPORTANT: On the first screen of the installer, check the box that says "Add python.exe to PATH". This is crucial for easily running Python from the Command Prompt.

Click "Install Now" and follow the on-screen prompts to complete the installation.

Verify Installation:

Open Command Prompt (search for cmd in the Start menu).

Type python --version and press Enter. You should see the installed Python version (e.g., Python 3.10.x).

Type pip --version and press Enter. You should see the pip version, confirming it's installed.

2. Set Up Your Project Folder
Create a new folder on your computer for your project (e.g., C:\Users\YourUser\Documents\GlobalEnergyApp).

Place your app.py and encrypt_key.py files into this folder.

3. Install Python Dependencies (Libraries)
Your application relies on several external Python libraries. You need to install these using pip.

Open Command Prompt: Navigate to your project folder using the cd command. For example:

DOS

cd C:\Users\YourUser\Documents\GlobalEnergyApp
Install Libraries: Run the following commands one by one:

DOS

pip install google-generativeai
pip install pycryptodome
pip install reportlab
pip install PyPDF2
google-generativeai: For interacting with the Gemini AI.

pycryptodome: For encrypting your Gemini API key.

reportlab: For PDF export functionality.

PyPDF2: For PDF reading/scanning functionality.

Note: If you encounter pip not found, ensure Python is added to your PATH as described in step 1.

4. Configure and Encrypt Your Gemini API Key
For security, your Gemini API key is encrypted and loaded from a file.

Get Your Gemini API Key:

Go to the Google AI for Developers website: https://ai.google.dev/

Sign in with your Google account.

Follow the instructions to generate a new API key. Copy this key.

Edit encrypt_key.py:

Open the encrypt_key.py file in a text editor (like Notepad, VS Code, or Sublime Text).

Find the line:

Python

api_key = b'YOUR_GEMINI_API_KEY'  # must be in bytes
Replace YOUR_GEMINI_API_KEY with your actual Gemini API key. Make sure to keep the b' prefix and the single quotes (') around your key.

Example: If your key is AIzaSyB-........XYZ, the line should look like:

Python

api_key = b'AIzaSyB-........XYZ'
Keep the secret variable secure: The line secret = b'mysecretaeskey12' defines the encryption key. While mysecretaeskey12 is used for this demonstration, in a real application, you should use a strong, randomly generated 16-byte key and keep it extremely secure (e.g., load it from an environment variable). For this app, ensure secret in encrypt_key.py matches SECRET_KEY in app.py.

Save the encrypt_key.py file.

Run encrypt_key.py:

Open Command Prompt and navigate to your project folder (if not already there).

Run the script:

DOS

python encrypt_key.py
This will create a new file named encrypted_key.txt in your project folder. This file contains your encrypted API key.

5. Run the Application
Now you can run your app.py.

Open Command Prompt: Navigate to your project folder.

Run app.py:

DOS

python app.py
The application GUI should appear.

You should see a message in the console indicating that the Gemini AI API was configured securely.

6. Create a Standalone Executable for Windows (for GitHub Distribution)
To distribute your application as a standalone executable (so others don't need Python installed), you can use PyInstaller.

Install PyInstaller:
Open Command Prompt and navigate to your project folder.

DOS

pip install pyinstaller
Create a .spec file (Recommended for complex apps):
A .spec file gives you more control over the build process, especially when dealing with hidden imports or data files.
First, generate a basic spec file:

DOS

pyinstaller --onefile --windowed app.py
This command will:

--onefile: Create a single executable file.

--windowed: Prevent a console window from opening when the app runs (suitable for GUI apps).

app.py: Your main script.

After running this, PyInstaller will create an app.spec file in your project directory.

Edit the .spec file for Crypto modules and data files:
Open app.spec in a text editor. You need to ensure PyInstaller correctly bundles Crypto modules and your encrypted_key.txt file.

Find the a = Analysis(...) section.

Hidden Imports: Add hiddenimports=['Crypto.Cipher._AES'] to ensure the AES module is included.

Data Files: You need to explicitly include encrypted_key.txt and global_energy_db.sqlite (your database file).

Modify the datas list within the Analysis object. It might look like this initially:

Python

a = Analysis(
    ['app.py'],
    pathex=['C:\\Users\\YourUser\\Documents\\GlobalEnergyApp'], # Your path here
    binaries=[],
    datas=[], # Add your data files here
    hiddenimports=[], # Add hidden imports here
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
Change it to something like this (adjusting your actual paths):

Python

a = Analysis(
    ['app.py'],
    pathex=['C:\\Users\\YourUser\\Documents\\GlobalEnergyApp'], # Your path here
    binaries=[],
    # Add your data files here. Format: (source_path, destination_folder_in_dist)
    datas=[
        ('encrypted_key.txt', '.'),
        ('global_energy_db.sqlite', '.')
    ],
    # Add hidden imports for Crypto modules
    hiddenimports=['Crypto.Cipher._AES'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
Save the app.spec file.

Build the Executable using the .spec file:
Open Command Prompt in your project folder.

DOS

pyinstaller app.spec
This command will build your executable based on the configurations in app.spec.

Find Your Executable:
After the build process completes, you'll find your standalone executable (app.exe) in the dist folder within your project directory (e.g., C:\Users\YourUser\Documents\GlobalEnergyApp\dist\app.exe).

7. Preparing for GitHub
When pushing your project to GitHub, you should NEVER upload your API key or the encrypted_key.txt file directly, as it contains sensitive information (even if encrypted, the encryption key is also in your code).

Here's how to structure your GitHub repository:

Create a .gitignore file:
In your project root directory, create a file named .gitignore (note the leading dot).
Open this file in a text editor and add the following lines:

Code snippet

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python/
env/
venv/
*.env

# PyInstaller
/build/
/dist/
*.spec

# Database
*.sqlite

# Encrypted API Key
encrypted_key.txt

# Local API Key (if you ever hardcode it for testing)
*.api_key
Save this file. This tells Git to ignore these files and folders, preventing them from being uploaded to your repository.

Initialize Git and Commit:
Open Command Prompt and navigate to your project folder.

DOS

git init
git add .
git commit -m "Initial commit of Global Energy Producers App"
Create GitHub Repository:

Go to https://github.com/new.

Create a new public or private repository.

Link Local to Remote and Push:
Follow the instructions provided by GitHub after creating your repository to link your local repository and push your code. It will typically involve commands like:

DOS

git remote add origin https://github.com/YourUsername/YourRepoName.git
git branch -M main
git push -u origin main
Provide Instructions for Users:
In your GitHub repository's README.md file, you must include clear instructions for other users on how to:

Clone your repository.

Install Python.

Install the required pip dependencies.

Crucially, how to obtain their own Gemini API key and run encrypt_key.py (which they will need to modify with their key).

How to run app.py.

How to build the executable themselves if they wish (they will need pyinstaller and your .spec file, but not your encrypted_key.txt or global_energy_db.sqlite).
