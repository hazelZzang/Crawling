from selenium import webdriver
import time
import ctypes

CF_TEXT = 1

kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

user32.OpenClipboard(0)


browser = webdriver.Chrome('C://Users//20143//Desktop//chromedriver.exe')
browser.get("https://basecamp.robolink.com/cwists/category#products=%5B1%5D&selected_sort_by=alphabetical")

time.sleep(5)
button = browser.find_element_by_xpath('//*[@id="activity-search-results"]/div/div[2]/button')
button.click()
time.sleep(5)

cards = browser.find_elements_by_class_name("card__img-wrap")
links = []
for card in cards:
    links.append(card.get_attribute('href'))
for link in links:
    browser.get(link)
    time.sleep(5)

    buttons = browser.find_elements_by_class_name('cpy-clip-txtarea')
    if len(buttons) == 0:
        continue

    title = browser.find_element_by_css_selector('.titlebar__title.u-flex')
    subtitle = browser.find_elements_by_css_selector('.step-content-h3.u-hide-print')
    title_name = title.get_attribute("textContent")

    try:
        wf = open(title_name[:2] + ".txt", "w", encoding='UTF-8')

        wf.write(title_name + "\n\n\n")
        for i in subtitle:
            wf.write(i.get_attribute("textContent")+"\n")
        wf.write("\n\n\n")
        for i in buttons:
            wf.write(i.get_attribute("textContent")+"\n\n\n\n\n")
        wf.write("\n\n\n")
        wf.close()
    except:
        print("FU"+title_name)

    time.sleep(1)
    print(link)

time.sleep(5)
browser.quit()
