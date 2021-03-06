# MindSphere autologin script

### This script automates the process of (re)logging into MindSphere, keeping the session active, checks for errors and MindSphere content on the page and refreshes accordingly. This script runs at 30 seconds intervals. I use this script to keep a MindSphere application open 24/7.
### NOTE: This project is not endorsed by Siemens and may be breaching MindSphere's terms and conditions. It is given to you as is.

On first run, this script will step you through a wizard to automatically download the latest web engine for either Firefox (recommended) or Chrome, as well as to get your login details. (NOTE: Your MindSphere password is not stored in plaintext, but base64 is not far off)


#### Supported Systems:
 - Windows, Linux
 - AMD64, x86, ARM7+(Only supports Firefox)
 - Firefox (recommended), Chrome

#### Prerequsites:
 - Python 3 installed: [https://realpython.com/installing-python/](https://realpython.com/installing-python/)
 - Internet Connection
 - MindSphere account
 - Firefox or Chrome installed

#### Install Required Python packages:

Navigate to the folder containing the script, then run the following:

**Windows, Mac and Linux**
```sh
pip3 install -r requirements.txt
```
#### Additional step for Mac users (first time only):
Go to:
- Applications
- Python 3.X
- Run "Install Certificates.command"

Once this is complete you can run the script.

#### Running Script:

Navigate to the folder containing the script, then run the following:

**Windows**
```cmd
py autologin.py
```

**Linux**
```sh
python3 autologin.py
```

**Mac**
```sh
python3 autologin.py
```


#### Running on startup:

**Windows**

The setup wizard can optionally place a windows batch file in your C:\Users\\$(USER)\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup that will automatically launch this script on boot. This batch file relies on the script remaining in the directory it was when you ran the wizard, so if you move this script's folder, please re-run the wizard.

#### Running the Wizard again

If the setup Wizard needs to be run again, like in the case of choosing a different page to keep logged in, you will need to navigate to the script folder and run the command:

**Windows**
```cmd
py wizard.py
```

**Linux**
```sh
python3 wizard.py
```

**Mac**
```sh
python3 wizard.py
```
