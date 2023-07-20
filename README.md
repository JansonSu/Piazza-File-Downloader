Piazza Files Downloader 
======
This is a python-based program that can easily download files on piazza at one time

![image](https://github.com/JansonSu/Piazza-Files-Downloader/assets/137122140/02b266f4-9abc-4bdf-b8a3-7b8ca269e058)

******
|Author|Zijian Su|
|---|---
|Date|07/17/2023
******
## Contents <br>
* [Required environment](#required-environment)
* [User guide](#user-guide)
  
********
## Required environment 

**Python version**：3.7 
* Download Python: https://www.python.org/

**IDE**：pycharm  
* Download Pycharm: https://www.jetbrains.com/pycharm/

**Platform**: window 10  

**Python library used**:  
* requests
* mimetypes
* os
* sys
* selenium
* PySimpleGUI
* threading

**browser driver**: chromedriver
* Download chromedriver: https://chromedriver.chromium.org/downloads
* Download Google chrome: https://www.google.com/chrome/  
Note: please download the chromedriver with the same version as Google Chrome  
If it doesn't work, try putting chromedriver.exe in the Scripts folder where your python is installed
********
## User guide  
If you can't log in, or experience other problems, check your network. Another possible reason is that piazza modified their webpage.

### Method 1 Run the exe file directly 
Download PaizzaFileDownloader.zip to your computer and unzip it.   
Find FileDownloader.exe and double-click it to run it.  
I use pyinstaller to package my program. You should be able to run directly.
If you can't run it, it may be because the version of chromedriver is different from your Google chrome version, try to download the same version of chromedriver, put it in the same directory as the exe file, and overwrite the old chromedriver.  

### Method 2 Use python to run  
Please put chromedriver in the same directory as FileDownloader.py

After you have successfully installed the libraries required to run，  
Open your IDE, or use python to run FileDownloader.py  
Then you will see this interface：   
![image](https://github.com/JansonSu/Piazza-Files-Downloader/assets/137122140/02b266f4-9abc-4bdf-b8a3-7b8ca269e058)  
  
Enter the edu email address and password used when registering piazza, and press the login button to log in.   
When you log in successfully, you will see a prompt like follow：  
![image](https://github.com/JansonSu/Piazza-Files-Downloader/assets/137122140/09adb36a-f7b3-4437-a604-0f8a5c91b801)  
  
Then, you can select a course and click the Get Resource Section button:  
![image](https://github.com/JansonSu/Piazza-Files-Downloader/assets/137122140/70d67a12-ce93-40dc-b426-34b6e99f1a78)  
  
![image](https://github.com/JansonSu/Piazza-Files-Downloader/assets/137122140/ddc4dfd6-2027-4e96-893a-b9c1e515d691)
  
Now, select the section you need to download.  
![image](https://github.com/JansonSu/Piazza-Files-Downloader/assets/137122140/3f08f24c-1b89-4f11-be7d-dc431bde664c)  
  
Click the download button and your file will be downloaded to a folder named after your course, which can be found on the desktop.  
![image](https://github.com/JansonSu/Piazza-Files-Downloader/assets/137122140/008191a7-dce8-463e-9b35-3ba41c45003c)
  
When you need to exit the program, click the quit button to exit.



