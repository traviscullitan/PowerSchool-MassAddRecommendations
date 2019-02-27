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

class Recommendation():

    def __init__(self,dcid,course):
        self.dcid = dcid
        self.course = course

def main():

    config = import_config()

    driver = setup_selenium(config)

    recommendations = load_recommendations(config)

    if recommendations:
        login_to_powerschool(driver,config)

        for rec in recommendations:
            try:
                add_recommendation(driver,config,rec)
            except:
                traceback.print_exc()
                driver.save_screenshot(rec.dcid + "-" + rec.course)

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

def load_recommendations(config):
    recommendations = []
    with open(config["INPUT_PATH"]+config["INPUT_FILENAME"],'r') as f:
        next(f) # skip headings
        reader=csv.reader(f,delimiter=',')
        row = 1
        for dcid,course in reader:
            if dcid and course:
                rec = Recommendation(dcid,course)
                recommendations.append(rec)
            else:
                print("WARNING: Record on row {} missing data.".format(row))
            row += 1 
    
    return recommendations

def add_recommendation(driver,config,rec):
    #TODO
    pass

def close_selenium(driver):
    time.sleep(5) # Let the user actually see something!
    driver.quit()

if __name__ == "__main__":
    main()