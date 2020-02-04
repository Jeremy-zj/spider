from selenium import webdriver
from time import sleep

#PhantomJS
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')

url ='https://www.baidu.com/'
bro = webdriver.Chrome(executable_path=r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe')

bro.get(url)
sleep(2)

#写入web脚本操作
# bro.execute_script('')

#定位到一个具体的iframe
# bro.switch_to_frame('')

text_input = bro.find_element_by_id('kw')

text_input.send_keys('天气预报')
sleep(2)

bro.find_element_by_id('su').click()
sleep(10)

bro.quit()
