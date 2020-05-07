import time

import autoit
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Instagram:

    def __init__(self, driver):
        self._driver = driver
        self._posted_count = 0

    def login(self, username, password):
        self._driver.get('https://www.instagram.com/accounts/login/')
        input_username = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]'))
        )
        input_username.send_keys(username)
        input_password = self._driver.find_element_by_css_selector('input[name="password"]')
        input_password.send_keys(password)
        button_submit = self._driver.find_element_by_css_selector('button[type="submit"]')
        button_submit.click()

    def skip_initial_popups(self):
        # button_not_now = WebDriverWait(self._driver, 10).until(
        #     lambda x:
        #         EC.presence_of_element_located((By.XPATH, '//button[text()="Not Now"]')) or
        #         EC.presence_of_element_located((By.XPATH, '//button[text()="Cancel"]'))
        # )
        button_not_now = WebDriverWait(self._driver, 10).until(
            lambda x:
                x.find_element_by_xpath('//button[text()="Not Now"]') or
                x.find_element_by_xpath('//button[text()="Cancel"]')
        )
        button_not_now.click()

        cancel_not_now = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Cancel"]'))
        )
        cancel_not_now.click()

    def post(self, image_path, label):
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'svg[aria-label="New Post"]'))
        )
        ActionChains(self._driver).move_to_element(
            self._driver.find_element_by_css_selector('svg[aria-label="New Post"]')
        ).click().perform()
        handle = "[CLASS:#32770; TITLE:Open]"
        autoit.win_wait(handle, 60)
        autoit.control_set_text(handle, "Edit1", image_path)
        autoit.control_click(handle, "Button1")

        button_expand = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Expand"]'))
        )
        button_expand.click()

        button_next = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Next"]'))
        )
        button_next.click()

        textarea_caption = WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[aria-label="Write a caption…"]'))
        )
        textarea_caption.send_keys(label)

        button_share = self._driver.find_element_by_xpath('//button[text()="Share"]')
        button_share.click()

        self._posted_count += 1

        # button_not_now = WebDriverWait(self._driver, 10).until(
        #     lambda x:
        #         x.find_element_by_xpath('//button[text()="Not Now"]') or
        #         x.find_element_by_css_selector('svg[aria-label="New Post"]')
        # )
        if self._posted_count == 1:
            button_not_now = WebDriverWait(self._driver, 10).until(
                # lambda x: x.find_element_by_xpath('//button[text()="Not Now"] | //svg[@aria-label="New Post"]')
                lambda x: x.find_element_by_xpath('//button[text()="Not Now"]')
            )
            if button_not_now.text == 'Not Now':
                button_not_now.click()