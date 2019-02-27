import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import configparser
from collections import defaultdict
import csv
import traceback
import os

def main():
    
    config = import_config()

    driver = setup_selenium(config)

    login_to_powerschool(driver,config)

    close_selenium(driver)

def import_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config = config["DEFAULT"]
    return config

def setup_selenium(config):
    driver = webdriver.Chrome(config["CHROME_DRIVER"]) 
    return driver

def login_to_powerschool(driver,config):
    driver.get(config["HOST"] + '/teachers')
    time.sleep(1) # Let the user actually see something!
    username_box = driver.find_element_by_name('username')
    password_box = driver.find_element_by_name('password')
    username_box.send_keys(config["USERNAME"])
    password_box.send_keys(config["PASSWORD"])
    password_box.submit()

def close_selenium(driver):
    time.sleep(5) # Let the user actually see something!
    driver.quit()

if __name__ == "__main__":
    main()