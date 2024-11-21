from selenium import webdriver  # web-browser protocol
from selenium.webdriver.common.keys import Keys # Keyboard keys instances container
from selenium.webdriver.common.by import By # different locatros types stored
from selenium.webdriver import ActionChains # Perform series of action
from selenium.webdriver.support.wait import WebDriverWait as wd # Allow to locate elemt until certain time by condition
from selenium.webdriver.support import expected_conditions as ec # Class with possible conditions
import time
from selenium.webdriver.common.action_chains import ActionChains
from pynput.keyboard import Key, Controller # Keyboard manipulations modules
import sqlite3 # Data base system controll



class spam():

    def __init__(self, text, groups, login, parol, head, bottm):
        """--------------------------------------Reading list of groups from groups.txt-----------------------------"""
        """---------------------------------------setting up data base for stroring group's users-----------------------"""
        self.text = text
        self.groupss = groups
        self.login = login
        self.parol = parol
        self.head = head
        self.botom = bottm

        with open(f'{self.text}', encoding='utf-8') as f:
            self.texty = f.read().split('\n')

        self.groups = []
        f = open(self.groupss)
        for group in f:
            if '\n' in group:
                group = group[:-1]
            self.groups.append(group)

        self.base = sqlite3.connect("dase.db")
        self.cursor = self.base.cursor()
        create_quary = """CREATE TABLE IF NOT EXISTS ids(
        id INT
        );"""
        self.cursor.execute(create_quary)
        self.base.commit()


    def sdelat(self, driver):
        """If user belongs to a certain range send him a message """                                                
        try:                                                                    
            text = wd(driver,6).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[3]/div/div[2]/section[2]/div[1]/div[2]/span"))).text.split()[4]
            dsms = wd(driver,10).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[3]/div/div[1]/div[3]/div"))).click()       
            if text <= self.head and text >= self.botom:                                         
                wd(driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, "a.vkuiButton--with-icon"))).click()
                vid = wd(driver, 5).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/div/div[2]/div/div[7]/div/span/div/a[2]"))).click()
                upl = wd(driver, 5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.video_choose_upload_area'))).click()
                keyboard = Controller()  # uploading video is possible only via controlle 
                keyboard.type(r"C:\Users\Admin\Documents\programming\projects\vk_bot\Готовый ролик.mp4")
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                time.sleep(10)
                line = wd(driver, 5).until(ec.presence_of_element_located((By.ID, "mail_box_editable")))
                for x in self.texty:
                    line.send_keys(x)
                    line.send_keys(Keys.RETURN)
                    time.sleep(0.5)
                time.sleep(5)
                wd(driver, 5).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mail_box_send"]'))).click()
        except Exception:
            pass
        finally:
            return 0
    
    def insertion(self, s):
    
        insert_quer = """INSERT INTO ids values(?)
        """ 
        self.cursor.execute(insert_quer, s)
        self.base.commit()
        #cursor.close()
        #base.close()
    def delete(self, id):
        delete_query = """Delete from ids where id=?"""
        self.cursor.execute(delete_query, (id,))
        self.base.commit() 
    def select(self):
        select_quer = """Select id from ids"""
        self.cursor.execute(select_quer)
        return self.cursor.fetchall()
    def download(self):
        driver = webdriver.Firefox()  # using Firefox's webdriver - best choice!!
        driver.maximize_window()
        driver.get("https://vk.com/") # get to 'Vkontakte' main page
        """" wait 10 second util the prence of the element by the given id bellow"""
        login_pol = wd(driver, 10).until(ec.presence_of_element_located((By.ID, "index_email"))) # web element login pol
        login_pol.clear(); login_pol.send_keys(self.login) #filling informating into the filed previously clearing it
        login_pol.send_keys(Keys.RETURN)  # Immitation of keyboard pressing
        time.sleep(10)
        ids = []
        group = wd(driver, 10).until(ec.element_to_be_clickable((By.ID, "l_gr"))).click()
        input = wd(driver, 5).until(ec.element_to_be_clickable((By.ID, "groups_list_search")))
        for g in self.groups:
            input = wd(driver, 5).until(ec.element_to_be_clickable((By.ID, "groups_list_search")))
            input.clear()
            input.send_keys(g); input.send_keys(Keys.RETURN)
            time.sleep(2)
            wd(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[11]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div[3]/div[1]/div[1]/div[3]/div[1]/a"))).click()
            time.sleep(2)
            driver.execute_script("window.scrollBy(0,500)")  # permorming window script to scrool down in browser
            chin = ActionChains(driver)  # Series of actions needed
            time.sleep(2)
            wd(driver, 10).until(ec.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Подписчики'))).click()
            time.sleep(2)                                                       
            for x in range(2500):  # Here, the solutio with 'execuct script' doesn't work pretty well
                chin.key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).perform()  # In pop-up filed I used acton chains
        
            time.sleep(5)
            users = driver.find_elements(By.CLASS_NAME, "fans_fan_ph") # cycling througn the elem of class name
            flag = 0
            for user in users:  
                id = user.get_attribute("href")
                if id == 'https://vk.com/id174447258':
                    flag = 1
                if flag ==0:
                    if (id,) not in ids:
                        ids.append((id,))
                flag == 0
            driver.back()   # Moving backwards in browsing history
            print(len(ids))  # some logs....
        for s in ids:   # Dealing with d/b (not interesting)
            self.insertion(s)
        driver.close()
        return 0
    def main_function(self):
        try:
            driver = webdriver.Firefox()
            driver.maximize_window()
            driver.get("https://vk.com/")
            
            login_pol = wd(driver, 10).until(ec.presence_of_element_located((By.ID, "index_email")))
            login_pol.clear(); login_pol.send_keys(self.login) # Filling email into located field
            login_pol.send_keys(Keys.RETURN)
            time.sleep(20)    # Time for entering code from the notify
            # self.select() getting ids from the database fetching them all as tuples...
            a = [x[0] for x in self.select()]  #... storing into a list
            for id in a:
                """Searching for users with the corresponding ids"""
                fr = wd(driver, 10).until(ec.presence_of_element_located((By.ID, "l_fr"))).click()
                time.sleep(1)
                input_line = wd(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="s_search"]')))
                input_line.clear()
                input_line.send_keys(id); input_line.send_keys(Keys.RETURN)
                time.sleep(2)    
                try:   #deleted users processing
                    wd(driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.friends_field:nth-child(1) > a:nth-child(1)'))).click()
                except Exception:
                    self.delete(id)
                    continue          
                try:            #users might be tagged by different ids                                                          
                    pod = wd(driver,5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'span.ActionsGroupItem-module__root--DoBWz:nth-child(5)'))).click()   
                    self.sdelat(driver=driver)
                except Exception:
                    try:                                                                        
                        pod = wd(driver,5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'span.ActionsGroupItem-module__root--DoBWz:nth-child(3)'))).click()   
                        self.sdelat(driver=driver)
                    except Exception:
                        pod = wd(driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.ActionsGroupItem-module__root--DoBWz'))).click()
                        self.sdelat(driver)
                finally:
                    driver.back()  # move back to friend's field
                self.delete(id)  # delete id after it was processed
                
        finally:
            self.cursor.close()
            self.base.close()
            driver.close()

def main():
    spamik = spam('texty.txt', 'groups.txt', '89212405502', 'parolparol', '1989', '1965')
    spamik.download()
    time.sleep(2)
    spamik.main_function()
if __name__ == '__main__':
    main()


