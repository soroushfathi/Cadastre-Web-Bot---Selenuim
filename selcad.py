
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
        TimeoutException,
        UnexpectedAlertPresentException,
        ElementClickInterceptedException
)
import subprocess
from time import sleep




from statics import username1 as username,password1 as password,province1 as province,area1 as area





# from tkinter import Tk,Label,Entry,Frame
# from PIL import Image,ImageTk
# def get_captcha_from_user_using_tk(img):
#     global user_input
#     ws = Tk()
#     ws.title('captcha')
#     img = Image.open(img)
#     resize_img = img.resize((400,140))
#     img = ImageTk.PhotoImage(resize_img)
#
#     frame = Frame(ws)
#     frame.pack()
#
#     Label(
#         frame,
#         image=img
#     ).pack()
#
#     entry = Entry(frame) 
#     entry.pack()
#     entry.focus_set()
#
#     def callback(event):
#         global user_input
#         user_input = entry.get()
#         ws.destroy()
#
#     ws.bind('<Return>', callback)
#
#     ws.mainloop()
#     return user_input

    
IMPORTANT_WAIT=50
IMPORTANT_TINY_WAIT=30
DONT_CARE_WAIT=850
TINY_WAIT=0.05

    
options = Options()
options.page_load_strategy = 'eager'
#TODO : chromium
driver = webdriver.Firefox(options=options,service=Service(executable_path='/home/gui/selcad/geckodriver'))


def find_with_wait(xpath):
    return WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_to_be_clickable((By.XPATH, xpath)))

def find_with_wait2(xpath):
    return WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.element_located_to_be_selected((By.XPATH, xpath)))

def find_with_wait3(xpath):
    return WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.presence_of_element_located((By.XPATH, xpath)))

def find_with_wait4(xpath):
    return WebDriverWait(driver, timeout=DONT_CARE_WAIT).until(EC.visibility_of_element_located((By.XPATH, xpath)))

# url
def get_cadastre_until_it_opens():
    driver.get("https://cadastre.mimt.gov.ir")
    # refresh until we find username box
    while True:
        try:
            WebDriverWait(driver, timeout=0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ULogin1_txt_Username"]')))
            break
        except (TimeoutException, UnexpectedAlertPresentException):
            # driver.get("https://cadastre.mimt.gov.ir/")
            driver.refresh()
# get_cadastre_until_it_opens()

def get_sms():
    return subprocess.Popen(['nc','-ln','0.0.0.0','38587'], stdout=subprocess.PIPE).communicate()[0].decode()
# login
def login():
    find_with_wait('//*[@id="ULogin1_txt_Username"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="ULogin1_txt_Pass"]').send_keys(password)
    #captcha
    captcha_element = find_with_wait4('//*[@id="ctl00_ULogin1_RadCaptcha1_CaptchaImageUP"]')
    captcha_element.screenshot(captcha_element.id+'.png')
    # captcha = get_captcha_from_user_using_tk(captcha_element.id+'.png')
    # driver.find_element(By.XPATH, '//*[@id="ctl00_ULogin1_RadCaptcha1_CaptchaTextBox"]').send_keys(captcha)

    driver.find_element(By.XPATH, '//*[@id="ULogin1_btnLogin1"]').click()

    # sms
    # sms=get_sms()
    # print(sms)
    # find_with_wait('//*[@id="ULogin1_txtSMSCode"]').send_keys(get_sms())
    # driver.find_element(By.XPATH, '//*[@id="ULogin1_txtSMSCode"]').send_keys(sms)
    # find_with_wait('//*[@id="ULogin1_btnSMSLogin"]').click()
    driver.find_element(By.XPATH, '//*[@id="ULogin1_btnSMSLogin"]').click()
login()
driver.get("https://cadastre.mimt.gov.ir/Map/RegMap.aspx")

def select_from_menu(xpath, item):
    find_with_wait(xpath).click()
    item_list=find_with_wait(xpath[:-7]+'DropDown"]/div/ul').find_elements(By.TAG_NAME,'li')
    for elem in item_list:
        if elem.get_attribute('innerHTML')==item:
            #  todo: advance wait
            sleep(TINY_WAIT)
            elem.click()
            # driver.execute_script("arguments[0].click();", elem)
            break

# step 1: select province
def select_province():
    select_from_menu('//*[@id="ctl00_ContentPlaceHolder1_CmbEstate_Input"]', province)
    # refresh if we stuck
    while True:
        try:
            WebDriverWait(driver, timeout=IMPORTANT_WAIT).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'raDiv')))
            break
        except TimeoutException:
            driver.refresh()
            select_from_menu('//*[@id="ctl00_ContentPlaceHolder1_CmbEstate_Input"]', province)
    sleep(TINY_WAIT)
select_province()

# step 2: mineral matrial
# select group6
def select_mineral_material():
    select_from_menu('//*[@id="ctl00_ContentPlaceHolder1_CmbGroup_Input"]','گروه 6')
    # refresh if we stuck
    while True:
        try:
            WebDriverWait(driver, timeout=IMPORTANT_WAIT).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'raDiv')))
            break
        except TimeoutException:
            driver.refresh()
            # TODO: idk this is needed or not
            select_province()
            select_from_menu('//*[@id="ctl00_ContentPlaceHolder1_CmbGroup_Input"]','گروه 6')
    sleep(TINY_WAIT)
select_mineral_material()
    
def select_metal():
    while True:
        try:
            # ... button
            find_with_wait('//*[@id="ctl00_ContentPlaceHolder1_RadButton1_input"]').click()
            break
        except ElementClickInterceptedException:
            sleep(TINY_WAIT)
            # TODO: idk this is needed or not

    # select kansar felezi (but refresh if we stuck)
    while True:
        try:
            driver.switch_to.frame(WebDriverWait(driver,timeout=IMPORTANT_WAIT).until(EC.visibility_of_element_located((By.TAG_NAME,"iframe"))))
            break
        except TimeoutException:
            driver.refresh()
            # TODO: idk this is needed or not
            select_province()
            select_mineral_material()
    # driver.switch_to.frame(driver.find_element(By.TAG_NAME,"iframe"))
    find_with_wait('/html/body/form/div[4]/div/div[2]/table/tbody/tr[3]/td[3]').click()
    # taeed
    find_with_wait('//*[@id="RadButton1_input"]').click()
    driver.switch_to.default_content()
    sleep(TINY_WAIT)
select_metal()

# step 3: insert points
def insert_points(points):
    for point in points:
        xd = find_with_wait3('//*[@id="ctl00_ContentPlaceHolder1_LngD"]')
        xm = find_with_wait3('//*[@id="ctl00_ContentPlaceHolder1_LngM"]')
        xs = find_with_wait3('//*[@id="ctl00_ContentPlaceHolder1_LngS"]')
        yd = find_with_wait3('//*[@id="ctl00_ContentPlaceHolder1_LatD"]')
        ym = find_with_wait3('//*[@id="ctl00_ContentPlaceHolder1_LatM"]')
        ys = find_with_wait3('//*[@id="ctl00_ContentPlaceHolder1_LatS"]')
        xd.clear()
        xm.clear()
        xs.clear()
        yd.clear()
        ym.clear()
        ys.clear()
        
        xd.send_keys(point[0])
        xm.send_keys(point[1])
        xs.send_keys(point[2])
        yd.send_keys(point[3])
        ym.send_keys(point[4])
        ys.send_keys(point[5])
        
        #darj button
        driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Btn_AddPoint_input"]').click()
        # find_with_wait2('//*[@id="ctl00_ContentPlaceHolder1_Btn_AddPoint_input"]').click()
        sleep(TINY_WAIT)
        WebDriverWait(driver, timeout=IMPORTANT_WAIT).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'raDiv')))
        
    driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_BtnCalc_input"]').click()

def insert_area():
    for points in area:
        insert_points(points)
        try:
            sleep(TINY_WAIT)
            # captcha
            captcha_element = WebDriverWait(driver, timeout=IMPORTANT_TINY_WAIT).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_RadCaptcha1_CaptchaImage"]')))
            # captcha_element = find_with_wait4('//*[@id="ctl00_ContentPlaceHolder1_RadCaptcha1_CaptchaImage"]')
            captcha_element.screenshot(captcha_element.id+'.png')
            captcha = get_captcha_from_user_using_tk(captcha_element.id+'.png')
            driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_RadCaptcha1_CaptchaTextBox"]').send_keys(captcha)
            driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_BtnSaveMine_input"]').click()
            break
        except:
            driver.refresh()
            select_province()
            select_mineral_material()
            select_metal()
insert_area()


# tarsim again (delete old points using refresh)
# tarsim_mahdoode = '//*[@id="ctl00_ContentPlaceHolder1_BtnA3_input"]'

