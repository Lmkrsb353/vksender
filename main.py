from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait as wd
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from selenium.webdriver.common.action_chains import ActionChains
from pynput.keyboard import Key, Controller
from selenium.common.exceptions import WebDriverException
from pynput.keyboard import Key, Controller
import sqlite3

with open('texty.txt', encoding='utf-8') as f:
    texty = f.read().split('\n')

print(texty)
for x in texty:
    print(x)
def sdelat(driver):
    print("В функции")                                                          
    try:                                                                    
        text = wd(driver,6).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[3]/div/div[2]/section[2]/div[1]/div[2]/span"))).text.split()[4]
        print(text)
        dsms = wd(driver,10).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[3]/div/div[1]/div[3]/div"))).click()     
        print("yes")      
        if text <= "1989" and text >= "1966":                                         
            wd(driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, "a.vkuiButton--with-icon"))).click()
            vid = wd(driver, 5).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[2]/div/div[7]/div/span/div/a[2]"))).click()
            upl = wd(driver, 5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.video_choose_upload_area'))).click()
            keyboard = Controller()
            keyboard.type(r"C:\Users\Admin\Documents\programming\projects\vk_bot\Готовый ролик.mp4")
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            time.sleep(10)
            line = wd(driver, 5).until(ec.presence_of_element_located((By.ID, "mail_box_editable")))
            for x in texty:
                line.send_keys(x)
                line.send_keys(Keys.RETURN)
                time.sleep(0.5)
            time.sleep(5)
            wd(driver, 5).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mail_box_send"]'))).click()
        return 0
    except Exception:
        return 0
    
groups = []
f = open('groups.txt')
for group in f:
    if '\n' in group:
        group = group[:-1]
    groups.append(group)
print(groups)
def download(groups):
    
    base = sqlite3.connect("dase.db")
    create_quary = """CREATE TABLE IF NOT EXISTS ids(
    id INT
    );"""
    cursor = base.cursor()
    cursor.execute(create_quary)
    base.commit()
    
    insert_quer = """INSERT INTO ids values(?)
""" 
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://vk.com/")

    login_pol = wd(driver, 10).until(ec.presence_of_element_located((By.ID, "index_email")))
    login_pol.clear(); login_pol.send_keys("89212405502")
    login_pol.send_keys(Keys.RETURN)
    time.sleep(10)
    #wd(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/form/div[3]/button"))).click()

    #wd(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[4]"))).click()

    #parol = wd(driver, 7).until(ec.presence_of_element_located((By.NAME, "password")))
    #parol.clear(); parol.send_keys("Velsk101")
    #parol.send_keys(Keys.RETURN)

    ids = []
    group = wd(driver, 10).until(ec.element_to_be_clickable((By.ID, "l_gr"))).click()
    input = wd(driver, 5).until(ec.element_to_be_clickable((By.ID, "groups_list_search")))
    for g in groups:
        input = wd(driver, 5).until(ec.element_to_be_clickable((By.ID, "groups_list_search")))
        print(g)
        input.clear()
        input.send_keys(g); input.send_keys(Keys.RETURN)
        time.sleep(2)
        wd(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[11]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div[3]/div[1]/div[1]/div[3]/div[1]/a"))).click()
        time.sleep(2)
        driver.execute_script("window.scrollBy(0,500)")
        chin = ActionChains(driver)
        #chin.move_by_offset(1300, 500).click().perform()
        time.sleep(2)
        wd(driver, 10).until(ec.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Подписчики'))).click()
        time.sleep(2)                                                       
        #origin = driver.find_element(By.CLASS_NAME, "fans_fan_ph ")
        for x in range(2500):
            chin.key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).perform()
    
        time.sleep(5)
        users = driver.find_elements(By.CLASS_NAME, "fans_fan_ph")
        flag = 0
        for user in users:  
            
                #driver.back()
                #driver.execute_script("window.scrollBy(0,500)")
                #time.sleep(2)
                #wd(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[11]/div/div/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[1]/div/div[3]/aside/div/a'))).click()
                #driver.implicitly_wait(5)
                #time.sleep(2)
            id = user.get_attribute("href")
            if id == 'https://vk.com/id174447258':
                flag = 1
            if flag ==1:
                if (id,) not in ids:
                    ids.append((id,))
        driver.back()
        print(len(ids))
    for s in ids:
        cursor.execute(insert_quer, s)
    base.commit()
    cursor.close()
    base.close()
    driver.close()
    return 0
def main_function():
    try:
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get("https://vk.com/")
        
        login_pol = wd(driver, 10).until(ec.presence_of_element_located((By.ID, "index_email")))
        login_pol.clear(); login_pol.send_keys("89212405502")
        login_pol.send_keys(Keys.RETURN)
        time.sleep(20)
        #wd(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/div[1]/div[1]/div/div/div/form/div[3]/button"))).click()

       # wd(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[4]"))).click()

       # parol = wd(driver, 7).until(ec.presence_of_element_located((By.NAME, "password")))
        #parol.clear(); parol.send_keys("w#y^6TQ4ir3AeG")
        #parol.send_keys(Keys.RETURN)

        base = sqlite3.connect("dase.db")
        create_quary = """CREATE TABLE IF NOT EXISTS ids(
        id INT
    );"""
        cursor = base.cursor()
        cursor.execute(create_quary)
        base.commit()
        ids2 = []
        select_quer = """Select id from ids"""
        cursor.execute(select_quer)
        a = [x[0] for x in cursor.fetchall()]
        #a = ['https://vk.com/id2125679']
        
        for id in a:
            ids2.append((id,))
            fr = wd(driver, 10).until(ec.presence_of_element_located((By.ID, "l_fr"))).click()
            time.sleep(1)
            input_line = wd(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="s_search"]')))
            input_line.clear()
            input_line.send_keys(id); input_line.send_keys(Keys.RETURN)
            time.sleep(2)    
            try:
                wd(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.friends_field:nth-child(1) > a:nth-child(1)'))).click()
            except Exception:
                delete_query = """Delete from ids where id=?"""
                cursor.execute(delete_query, (id,))
                base.commit()
                continue          
            try:                                                                      
                pod = wd(driver,5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'span.ActionsGroupItem-module__root--DoBWz:nth-child(5)'))).click()   
                sdelat(driver=driver)
            except Exception:
                try:                                                                        
                    pod = wd(driver,5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'span.ActionsGroupItem-module__root--DoBWz:nth-child(3)'))).click()   
                    sdelat(driver=driver)
                except Exception:
                    pod = wd(driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.ActionsGroupItem-module__root--DoBWz'))).click()
                    sdelat(driver)
            finally:
                driver.back()
            delete_query = """Delete from ids where id=?"""
            cursor.execute(delete_query, (id,))
            base.commit()
            
        #messages
        #mess = wd(driver, 10).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[11]/div/div/div[2]/div[2]/div[3]/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/a/span')))
        #mess.click()

        #chains1 = ActionChains(driver)
        #chains1.send_keys_to_element(input, "aqua_life29").key_up(Keys.RETURN)
    #except WebDriverException:
      #  print('process...')
      #  time.sleep(60)
    finally:
        driver.close()

def main():
    main_function()
if __name__ == '__main__':
    main()