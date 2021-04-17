from selenium import webdriver
import time #used for sleep
import os #log out to file
import io #back support
 
def get_profile():
    profile = webdriver.FirefoxProfile();
    profile.set_preference("browser.privatebrowsing.autostart", True)
    profile.update_preferences()
    return profile

def get_options():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.set_preference("dom.webnotifications.serviceworker.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    return options

def write_out(file):
    if os.path.exists("Scapper4.log"):
        os.remove("Scapper4.log")
    
    fwrite = io.open("Scapper4.log", "x", encoding="utf-8")
    fwrite.write(file)
    fwrite.close()

def listToString(list):
    str1 = " "
    return (str1.join(list))

def scroolDown(driver):
    time.sleep(2)
    scroll_pause_Time = 1;
    screen_height = driver.execute_script("return window.screen.height;")  # Size of Page Used

    i = 1
    while True:

        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i)) 
        # ^ Execute js scrolling From 0 position to (screen height * i) I.E {1, 1080, 2, 2160, etc}

        i += 1;
        print("Pages scrolled so far " + str(i) + "\n") 
        
        time.sleep(scroll_pause_Time)

        #some webpages have inconsisent height definition below is a short-stick solution *fix-later
        scroll_height = driver.execute_script("return document.documentElement.scrollHeight;")  #redefine scrolling height 
        if scroll_height == 0:
            scroll_height = driver.execute_script("return document.body.scrollHeight;")
            if scroll_height == 0:
                scroll_height = driver.execute_script("return document.scrollHeight;") 
                if scroll_height == 0:
                    scroll_height = driver.execute_script("return document.scrollHeight;")
                else:
                    break

        if (screen_height) * i > scroll_height: 
            # Breaks once the screen scroll has passed the scroll height only possible if no more scrolling on page
            break

def main():
    path = 'geckodriver.exe'
    #url = 'https://www.youtube.com/c/TED/videos' #1
    #url = 'https://www.youtube.com/c/MOVIECLIPS/videos' #2
    #url = 'https://www.youtube.com/c/MoeShopMusic/videos' #3
    url = 'https://www.youtube.com/user/CEGNetwork/videos' #4

    # c equals channel | user is for individuals

    driver = webdriver.Firefox(executable_path=path, firefox_profile=get_profile(), options=get_options() )
    driver.get(url)
    time.sleep(10)
    
    scroolDown(driver)

    data = driver.find_elements_by_id(id_="video-title")
    #data = driver.find_element_by_tag_name('body')

    def clear(): os.system('cls') #on Windows System
    clear()
    
    strn = ""
    strn += (driver.title + "\n")
    for item in data:
        print(item.text)
        strn += item.text + '\n'
        #print(item)
        #strn += item

    #print(items[0].text) data is a list object
    print("\nNumber of items in data " + str(len(data)))

    write_out(strn) #log outfile

    #driver.find_element_by_xpath('//*[@id="thumbnail"]').click()
    time.sleep(20)
    driver.quit()

main()