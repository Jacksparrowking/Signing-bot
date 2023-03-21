from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import smtplib
from email.message import EmailMessage
from selenium.webdriver.common.keys import Keys
from twilio.rest import Client
import random

PASSWORD = "your_password"


def login(driver):
    id_ = driver.find_element(By.NAME, "edtUsername")
    id_.send_keys("your id")

    password_ = driver.find_element(By.NAME, "edtPassword")
    password_.send_keys(PASSWORD)

    btn = driver.find_element(By.NAME, "btnLogin")
    btn.click()


def registration(driver):
    sign_to_courses = driver.find_element(By.XPATH, '//*[@id="tvMainn11"]')
    sign_to_courses.click()

    btn_close = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$btnCloseThresholdRemark")
    btn_close.click()


sent_deep_learning_sms = False
sent_robotica_sms = False


def shibutz(driver):
    shibutz_from_list = driver.find_element(By.NAME, "ctl00$tbActions$ctl04$btnAddLessons")
    shibutz_from_list.click()

    after_shibutz_close = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$btnCloseThresholdRemark");
    after_shibutz_close.click()


def hashlama(driver):
    completion_65 = driver.find_element(By.ID, "ContentPlaceHolder1_gvBalance_lblBalanceName_9")
    completion_65.click()
    global sent_deep_learning_sms
    if sent_deep_learning_sms:
        return False

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    deep_learning = ''
    for course in soup.findAll(name="tr", id="ContentPlaceHolder1_gvLinkToLessons"):
        if "Deep" in course.text:
            # print(course)
            deep_learning = course
    if not deep_learning:
        return False

    array = deep_learning.findAll(name="td")
    check = array[0]
    print("test")
    if check.find(name="input"):
        print(type(check))
        inner_input = check.select(selector="td .ShortCutImage")[0]
        input_id = inner_input.get("id")

        if input_id:
            click_id = driver.find_element(By.ID, input_id)
            click_id.click()
            alert = driver.switch_to.alert
            alert.accept()
            update_sms()
            sent_deep_learning_sms = True
    return True


def refresh(driver):
    print("test_2")
    first_part_refresh = driver.find_element(By.ID, 'ContentPlaceHolder1_gvBalance_lblBalanceName_10')
    first_part_refresh.click()


def hascol_2(driver):
    hascol = driver.find_element(By.ID, 'ContentPlaceHolder1_gvBalance_lblBalanceName_11')
    hascol.click()
    global sent_robotica_sms
    if sent_robotica_sms:
        return False
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    deep_learning = ''
    for course in soup.findAll(name="tr", id="ContentPlaceHolder1_gvLinkToLessons"):
        if "רובוטיקה" in course.text:
            # print(course)
            deep_learning = course
    if not deep_learning:
        return False

    array = deep_learning.findAll(name="td")
    check = array[0]
    if check.find(name="input"):
        print(type(check))
        inner_input = check.select(selector="td .ShortCutImage")[0]
        input_id = inner_input.get("id")
        if input_id:
            click_id = driver.find_element(By.ID, input_id)
            click_id.click()
            alert = driver.switch_to.alert
            alert.accept()
            update_sms()
            sent_robotica_sms = True
    return True


def update_sms():
    account_sid = 'AC6833ee884586b24c4b99595b5ca2c254'
    auth_token = '42c5464d37b580557cb58d06a9c39ada'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="signed to course successfully.",
        from_="+15617695685",
        to="+your phone number"
    )


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-login-animations")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-default-apps")
    options.add_argument("--log-level=3")

    chrome_path = "/usr/bin/chromedriver"
    driver = webdriver.Chrome(executable_path=chrome_path, options=options)
    driver.get("https://inbar.biu.ac.il/live/Login.aspx")
    login(driver)
    registration(driver)
    shibutz(driver)
    while 1:
        register_to_deep = hashlama(driver)
        # register_to_robotics = hascol_2(driver)
        refresh(driver)
        # if not register_to_robotics and not register_to_deep:
        #     break
        if not register_to_deep:
            break
        time.sleep(random.randint(10, 20))

    driver.close()


if __name__ == "__main__":
    main()
