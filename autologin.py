import time
import json
import platform
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import wizard
import base64
import sys
import os

from datetime import datetime

def now():
    return datetime.now()

file_path = os.path.dirname(os.path.realpath(__file__))

print('You are here:' + file_path)

runWizardFlag = False
if (len(sys.argv) > 1):
    if ((sys.argv[1].startswith('-h')) or (sys.argv[1].startswith('--h'))):
        print("This script automates the process of (re)logging into MindSphere, keeping the session active, checks for errors and MindSphere content on the page (using the MS OSbar) and refreshes accordingly."
        +"\nThis script runs at 30 seconds intervals."
        +"\nOn first run, this script will step you through a wizard to automatically download the latest web engine for either Firefox (recommended) or Chrome, as well as to get your login details. (NOTE: Your MindSphere password is not stored in plaintext, but base64 is not far off)"
        +"\nYou may run the wizard again or alter settings by modifying the entries in config.json (ie. setting 'wizardRan': false), or by launching 'autologin.py --wizard'"
        +"\nSupported OSes: Windows, Linux"
        +"\nSupported architectures: AMD64, x86"
        +"\nNOTE: This project is not endorsed by Siemens and may be breaching MindSphere's terms and conditions. It is given to you as is."
        +"\n\n-h, --help                 Show help again"
        +"\n-w, --wizard               Run setup wizard again")
        exit()
    elif ((sys.argv[1].startswith('-w')) or (sys.argv[1].startswith('--w'))):
        runWizardFlag = True
    else:
        print("'{0}' is not a registered command. See 'autologin.py -h'".format(sys.argv[1]))
        exit()

wizard.validateSystem()

settings = {}
with open("config.json") as json_data_file:
    settings = json.load(json_data_file)

if (('wizardRan' not in settings) or not (settings['wizardRan']) or (runWizardFlag)):
    settings = wizard.settingsQuestions()
    wizard.installBrowserEngine(settings)

rootURL = settings['url']

#Selenium driver setup
executablePath = (file_path + "/chromedriver" if (settings['browser'] == 'chrome') else file_path + "/geckodriver") + (".exe" if platform.system() == 'Windows' else "")
print("executablePath: " + executablePath)
options = (webdriver.ChromeOptions() if (settings['browser'] == 'chrome') else webdriver.FirefoxOptions())
options.add_argument("--start-maximized" if (platform.system() == "Windows") else "--kiosk")
driver = (webdriver.Chrome(executablePath, chrome_options=options) if (settings['browser'] == 'chrome') else webdriver.Firefox(executable_path=executablePath,firefox_options=options))


def currentURL():
    return driver.current_url

def statusCode(URL): ## need to keep an eye on the js that we inject
    print(URL)
    js = '''
    let callback = arguments[0];
    let xhr = new XMLHttpRequest();
    xhr.open('GET',"'''+ URL +'''", true);
    xhr.timeout = 30000;
    xhr.onload = function () {
        if (this.readyState === 4) {
            callback(this.status);
        }
    };
    xhr.onerror = function () {
        callback('error');
    };
    xhr.send(null);
    '''
    print('js script status code',driver.execute_async_script(js))
    return driver.execute_async_script(js)

def site_login():
    driver.get(rootURL)

    try:
        print("looking for login box")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "username")))
        print("Found login box")
        driver.find_element_by_id('username').send_keys(settings['email'])
        driver.find_element_by_id ('password').send_keys((base64.b64decode(settings['password'])).decode('ascii'))
        driver.find_element_by_id('submit').click()
        WebDriverWait(driver, 5)
    except:
        print("not on login page")

    try:    
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "_mdspcontent")))
        #print(driver)
        status_code = statusCode(currentURL())
        print(status_code)
        if status_code != 200:
            retry()
    except:
        status_code = statusCode(currentURL())
        print("exception reached", status_code)
        retry()

def checkLogin():
    try:
        driver.find_element_by_id('username')
        print("login page detected")
        return True
    except:
        print("not on login page")
        return False

def retry():
    print("Time to retry")
    try:
        driver.get(rootURL)
        if checkLogin():
            print('retry check login true')
            site_login()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "_mdspcontent")))
        status_code = statusCode(currentURL())
        print(status_code)
        if status_code != 200:
            retry()
    except:
        retry()

def checkElement(): # looks for mindsphere ID on page as an additional check incase of sneaky 503s
    try:
        driver.find_element_by_id('_mdspcontent')
        print('we have mindsphere content showing')
        return True
    except:
        driver.refresh()
        print('no mindsphere content detected - time for refresh')
        return False

def checkMSError(): # looking for error class on MindSphere error pages
    try:
        driver.find_element_by_class_name('mindsphere-error-page')
        driver.refresh()
        print('error class found')        
    except:
        print('no error class found')

def mainloop():
    try:
        while True:
            time.sleep(30)
            print(currentURL())
            print('status code', statusCode(currentURL()))
            print('check login page',checkLogin())
            print("Current Time =", now().strftime("%H:%M:%S"))
            checkElement()
            checkMSError()
            if checkLogin() == True or statusCode(currentURL()) !=200:
                site_login()
    except (KeyboardInterrupt, SystemExit):
        driver.stop_client()
        driver.close()
        driver.quit()
        exit()
        #raise
    except:
        print("Main failed - retrying Main")
        mainloop()


########################################################################################################

site_login()
if platform.system() == 'Windows':
    driver.fullscreen_window()
mainloop()
