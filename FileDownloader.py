"""
    This is a python-based program that can easily download files on piazza at one time

    Author: Zijian Su
    date: 7/17/2023

"""


import requests
import mimetypes
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import PySimpleGUI as sg
from threading import Thread


def find_index(string, my_list):
    for index, value in enumerate(my_list):
        if value == string:
            return index
    return -1


class PiazzaFileDownloader:
    """
    elements:
        window       : GUI window

        driver       : Webdriver

        data         : A variable for storing cookies

        resource_list: A list for storing resource titles

        email        : User's email

        password     : User's password
    """
    def __init__(self):
        self.window = None
        self.driver = None
        self.data = None
        self.resource_list = []
        self.email = ''
        self.password = ''

    #
    def CheckAccessibility(self):
        """
            Check resource accessibility

        :return:
            Returns True if the resource is accessible; otherwise returns False.

        """
        if self.data is None or self.driver is None:
            self.window['-OUTPUT-'].print("Access failed, please try to log in again")
            return False
        else:
            return True

    def create_window(self):
        """
            This function is used to create the GUI

        :return:
            N/A
        """
        # UI layout
        col1 = [[sg.Text('Edu email', size=(13, 1)),
                 sg.Input(size=(20, 1), key='-EMAIL-')],
                [sg.Text('Password', size=(13, 1)),
                 sg.Input(size=(20, 1), key='-PASSWORD-', password_char='*')]]
        col2 = [[sg.Text('Courses list', size=(13, 1), key='-COURSE_T-'),
                 sg.Combo(['N/A'], size=(35, 1), disabled=True, key='-COMBO1-', readonly=True)]]
        col3 = [[sg.Button('Get Resource Section', disabled=True, key='-R_S-'),
                 sg.Button('Download to Desktop', disabled=True, key='-DOWNLOAD-'),
                 sg.Button('     Quit     ', key='-QUIT-', pad=((20, 0), 0))]]
        col4 = [[sg.Text('Resource Section ', size=(13, 1), visible=False, key='-R_S_T-'),
                 sg.Combo(['N/A'], size=(35, 1), visible=False, key='-COMBO2-', readonly=True)]]

        layout = [
            [sg.Text('Piazza Files Downloader', font=('Arial', 14, 'bold'))],
            [sg.Column(col1), sg.Button('Login', size=(12, 2), key='-LOGIN-')],
            [sg.Column(col2)],
            [sg.Column(col3)],
            [sg.Column(col4)],
            [sg.Multiline(size=(53, 10), key='-OUTPUT-', disabled=True)]
        ]
        # Create a window
        self.window = sg.Window('Piazza Files Downloader',
                                layout,  grab_anywhere=True, no_titlebar=True, keep_on_top=True)

    def open_chrome(self):
        """
            Open browser

        :return:
            N/A
        """
        # set webdriver
        service = Service(executable_path="PATH_TO_DRIVER")

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--silent")
        self.driver = webdriver.Chrome(options=chrome_options, service=service)
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def LoginOperate(self):
        """
            Obtain email and password from UI to log in

        :return:
            N/A
        """
        self.window['-OUTPUT-'].print('Logging in...')
        self.window['-OUTPUT-'].print('■', end='')
        self.window['-OUTPUT-'].print('■', end='')
        self.driver.get('https://piazza.com/account/login')
        self.window['-OUTPUT-'].print('■', end='')
        self.window['-OUTPUT-'].print('■', end='')
        try:
            # Enter email and password
            email_field = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID,
                                                                                              'email_field')))
            password_field = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID,
                                                                                                 'password_field')))
            email_field.send_keys(self.email)
            password_field.send_keys(self.password)
            self.window['-OUTPUT-'].print('■', end='')

            # Click the login button
            login_button = self.driver.find_element(By.ID, "modal_login_button")
            login_button.click()
            self.window['-OUTPUT-'].print('■', end='')

            # Login judgment bool
            GetIn = 0
            self.window['-OUTPUT-'].print('■', end='')

            # try to log in
            try:
                # Use page elements to determine whether the login is successful
                self.window['-OUTPUT-'].print('■')
                GetIn = self.driver.find_element(By.ID, 'userAccountBlockId')
                self.window['-OUTPUT-'].print('login successful')

            except Exception:
                self.window['-OUTPUT-'].print('Login failed')
                self.window['-LOGIN-'].update(disabled=False)

            if GetIn == 0:
                self.window['-DOWNLOAD-'].update(disabled=True)
            else:
                # After successful login, get the course list and update it in the drop-down bar
                dropdown_menu = self.driver.find_element(By.ID, 'classDropdownMenuId')
                dropdown_menu.click()
                dropdown_button = self.driver.find_element(By.ID, 'toggleInactiveNetworksId')
                dropdown_button.click()

                elements = self.driver.find_elements(By.XPATH, "//span[@class='course_number']")
                courses_list = [element.text for element in elements]
                self.window['-COMBO1-'].update(disabled=False)
                self.window['-COMBO1-'].update(values=courses_list)
                self.window['-R_S-'].update(disabled=False)

                # Get session cookie for Selenium browser and save
                self.data = self.driver.get_cookies()
                dropdown_button.click()
                dropdown_menu.click()
        except Exception:
            self.window['-OUTPUT-'].print('■■■■\nLogin failed')
            self.window['-LOGIN-'].update(disabled=False)
        self.window['-QUIT-'].update(disabled=False)

    def GetResource(self):
        """
            Get the resources of the current course from the web page

        :return:
            N/A
        """

        self.window['-OUTPUT-'].print('Fetching resource list...')

        # Check whether the driver and cookie exist
        if self.CheckAccessibility():
            try:
                self.window['-OUTPUT-'].print('■', end='')
                dropdown_menu = self.driver.find_element(By.ID, 'classDropdownMenuId')
                dropdown_menu.click()
                self.window['-OUTPUT-'].print('■', end='')
                dropdown_button = self.driver.find_element(By.ID, 'toggleInactiveNetworksId')
                dropdown_button.click()

                # Import cookies into the session
                session = requests.Session()
                for cookie in self.data:
                    session.cookies.set(cookie['name'], cookie['value'])

                course_ = self.window['-COMBO1-'].get()
                element = self.driver.find_element(By.XPATH, f'//span[text()="{course_}"]')
                element.click()
                self.window['-OUTPUT-'].print('■', end='')
                element = self.driver.find_element(By.XPATH, f'//span[text()="Resources"]')
                element.click()

                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'section_name_idx0')))
                self.window['-OUTPUT-'].print('■', end='')
                resource_sections = self.driver.find_elements(By.XPATH, '//h2[contains(@id, "section_name_idx")]')
                self.window['-OUTPUT-'].print('■', end='')
                self.resource_list = [resource_section.text for resource_section in resource_sections]
                self.window['-OUTPUT-'].print('■', end='')
                self.window['-R_S_T-'].update(visible=True)
                self.window['-COMBO2-'].update(visible=True)
                self.window['-OUTPUT-'].print('■', end='')
                self.window['-COMBO2-'].update(values=self.resource_list)
                self.window['-OUTPUT-'].print('■')
                self.window['-DOWNLOAD-'].update(disabled=False)

                self.window['-OUTPUT-'].print('Fetch succeeded')
                self.window['-R_S-'].update(disabled=False)
            except Exception:
                self.window['-OUTPUT-'].print('■■■■■■■■')
                self.window['-OUTPUT-'].print('Fetch failed')
                self.window['-R_S-'].update(disabled=False)

        self.window['-QUIT-'].update(disabled=False)

    def DownLoadOperate(self, index, current_section):
        """
            Download the files for the currently selected resource

        :return:
            N/A
        """

        if self.CheckAccessibility():
            session = requests.Session()
            for cookie in self.data:
                session.cookies.set(cookie['name'], cookie['value'])

            self.window['-OUTPUT-'].print('Downloading...')
            try:
                buttons = self.driver.find_elements(By.XPATH, '//button[contains(text(), "See all")]')
                for button in buttons:
                    button.click()
            except Exception:
                pass

            try:
                files = self.driver.find_elements(By.XPATH, f'//a[contains(@id, "resourceLink_idx{index}_")]')
                if len(files) == 0:
                    raise ValueError('length is 0')
                for f in files:
                    # Get file download link
                    href = f.get_attribute('href')
                    response = session.get(href)
                    response.raise_for_status()

                    # Get file type
                    content_type = response.headers.get('Content-Type')
                    extension = mimetypes.guess_extension(content_type)

                    # Add the extension to the file name
                    filename = f.text.strip()
                    filename_lower = filename.lower()
                    extension_lower = extension.lower()
                    extension_index = filename_lower.rfind(extension_lower)
                    if extension_index != -1:
                        filename = filename[:extension_index]
                    filename = filename.strip() + extension

                    # Create a folder on the desktop
                    desktop_path = os.path.expanduser("~/Desktop")
                    course_name = self.driver.find_element("id", 'topbar_current_class_number').text
                    course_folder_path = os.path.join(desktop_path, course_name)
                    section_folder_path = os.path.join(course_folder_path, current_section)
                    if not os.path.exists(course_folder_path):
                        os.makedirs(course_folder_path)
                    if not os.path.exists(section_folder_path):
                        os.makedirs(section_folder_path)
                    filename_desktop = os.path.join(section_folder_path, filename)

                    # download files
                    with open(filename_desktop, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    self.window['-OUTPUT-'].print(f'file download complete: {filename}')
                    if f == files[-1]:
                        self.window['-OUTPUT-'].print('No more file')
            except Exception:
                self.window['-OUTPUT-'].print("No file exists or the target of the link is not a file")

            self.window['-QUIT-'].update(disabled=False)

    def start_login_thread(self):
        """
            Create a new thread for login operation to prevent UI from getting stuck

        :return:
            N/A
        """
        login_thread = Thread(target=self.LoginOperate)
        login_thread.start()

    def resource_thread(self):
        """
            Create a new thread for get resource operation to prevent UI from getting stuck

        :return:
            N/A
        """
        Resource_thread = Thread(target=self.GetResource)
        Resource_thread.start()

    def download_thread(self, index, current_section):
        """
            Create a new thread for get download operation to prevent UI from getting stuck

        :return:
            N/A
        """
        DownLoad_thread = Thread(target=self.DownLoadOperate,args=(index, current_section))
        DownLoad_thread.start()

    def run(self):
        """
            Run downloader

        :return:
            N/A
        """


        self.create_window()
        self.open_chrome()
        while True:
            event, values = self.window.read()

            if event == '-LOGIN-':
                self.email = values['-EMAIL-']
                self.password = values['-PASSWORD-']
                if self.email == '' or self.password == '':
                    sg.popup("email or password can't be empty", title=' ', keep_on_top=True)
                else:
                    self.window['-LOGIN-'].update(disabled=True)
                    self.window['-QUIT-'].update(disabled=True)
                    self.start_login_thread()

            elif event == '-QUIT-':
                break

            elif event == '-R_S-':
                try:
                    self.window['-R_S-'].update(disabled=True)
                    self.window['-QUIT-'].update(disabled=True)
                    course = self.window['-COMBO1-'].get()
                    if course == '':
                        raise ValueError('None')
                    self.resource_thread()
                except Exception:
                    sg.popup('You need to choose a course', title=' ', keep_on_top=True)
                    self.window['-R_S-'].update(disabled=False)
                    self.window['-QUIT-'].update(disabled=False)

            elif event == '-DOWNLOAD-':
                try:
                    self.window['-QUIT-'].update(disabled=True)
                    current_section = self.window['-COMBO2-'].get()
                    index = find_index(current_section, self.resource_list)
                    if index == -1:
                        raise ValueError('index = -1')
                    self.download_thread(index, current_section)
                except Exception:
                    self.window['-QUIT-'].update(disabled=False)
                    sg.popup('Section cannot be empty', title=' ', keep_on_top=True)

        self.window.close()
        self.driver.quit()


if __name__ == "__main__":

    downloader = PiazzaFileDownloader()
    downloader.run()
