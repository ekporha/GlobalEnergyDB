
GlobalEnergyDB - Windows Application
====================================

Description:
-------------
This is a standalone Windows application that allows you to manage a database of global electrical, turbine, and thermal producers.

Features:
---------
- Add new producers
- Edit existing records
- Delete producers
- View all producers in a searchable table
- Filter by category (Electrical, Turbine, Thermal)

Files Included:
---------------
1. GlobalEnergyDB.exe           - The main application (Windows executable)
2. global_energy_db.sqlite      - The local database file
3. README.txt                   - This instruction manual

Usage:
------
1. Double-click "GlobalEnergyDB.exe" to launch the application.
2. Use the interface to add, edit, delete, or search producer data.
3. All data is saved automatically to "global_energy_db.sqlite".

Requirements:
-------------
- No installation needed.
- Works on Windows 10 or later.

To run the provided app.py on Windows and bundle it into a standalone .exe app, follow these steps:

✅ Step 1: Install Python (if not already installed)
Download Python for Windows from https://www.python.org/downloads/windows/

During installation:
✅ Check the box for "Add Python to PATH"

Proceed with installation
✅ Step 2: Set Up Project Environment
Create a new folder, e.g.:

makefile
Copy
Edit
C:\Projects\GlobalEnergyApp
Place app.py in that folder.

Open Command Prompt or PowerShell, and navigate to that folder:

sh
Copy
Edit
cd C:\Projects\GlobalEnergyApp
✅ Step 3: Install Required Packages
The script uses:

reportlab (for PDF export)

PyPDF2 (for reading PDF)

google-generativeai (optional: Gemini AI)

Install them with:

sh
Copy
Edit
pip install reportlab PyPDF2 google-generativeai
✅ Step 4: Run the App for Testing
From the same directory:

sh
Copy
Edit
python app.py
The GUI should launch. Verify everything works before building the .exe.

✅ Step 5: Bundle as Standalone .exe with PyInstaller
Install PyInstaller:

sh
Copy
Edit
pip install pyinstaller
Bundle the app:

sh
Copy
Edit
pyinstaller --onefile --noconsole --icon=your_icon.ico app.py
🔹 --onefile: single .exe file
🔹 --noconsole: hides terminal window (for GUI apps)
🔹 --icon=your_icon.ico: (optional) adds a custom icon (must be .ico format)

After build completes, find the .exe here:

makefile
Copy
Edit
C:\Projects\GlobalEnergyApp\dist\app.exe
✅ Step 6: Test the .exe
Double-click the app.exe from the dist folder. It should run exactly like the Python version.



