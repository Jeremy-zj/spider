# coding=utf8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


def chrome_do():
    """
    使用selenium打开控制chrome打开百度进行搜索并得到搜索结果
    :return:
    """
    # 使用selenium打开 Chrome浏览器
    browser = webdriver.Chrome()
    try:
        # 打开指定url
        browser.get('https://www.baidu.com')
        # time.sleep(3)
        # 再打开的页面中查找id=kw的单个元素
        input = browser.find_element_by_id('kw')
        # time.sleep(3)
        # 设置百度主页搜索文本框的值为Python
        input.send_keys('Python')
        time.sleep(3)
        # 触发回车事件#
        input.send_keys(Keys.ENTER)
        
        # 显示等待10秒。10秒内没有加载出指定控件则会抛出异常。若不指定监测的控件则此超时时间不起作用
        wait = WebDriverWait(browser, 10)
        # 设定若指定事件内未加载出id=content_left的控件则抛出异常并定位到这一行。
        # 百度搜索结果页面左侧的div容器.这个容器加载完之后。等待结束；
        wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
        # 这一行会因为页面不存在此id而在页面执行搜索10秒后抛出异常
        # wait.until(EC.presence_of_element_located((By.ID, 'content_left_333')))
        # 打印出当前页面的url
        print(browser.current_url)
        # 打印出当前页面的cookie
        print(browser.get_cookies())
        # 查看当前网页源代码
        print(browser.page_source)
        print('text index=', browser.page_source.find("廖雪峰"))
    finally:
        # 关闭浏览器
        browser.close()


def find_one_element():
    """
    查找淘宝网页面的搜索框元素
    :return:
    """
    browser = webdriver.Chrome()
    # 打开淘宝首页
    browser.get('https://www.taobao.com')
    # 搜索id=q的控件
    input_first = browser.find_element_by_id('q')
    # 使用css选择器。选中id=q的控件
    input_second = browser.find_element_by_css_selector('#q')
    # 使用xpath选择器。选中id=q的控件
    input_third = browser.find_element_by_xpath('//*[@id="q"]')
    
    # 使用By的方式来获取id=q的元素
    input_fourth = browser.find_element(By.ID, 'q')
    # 使用By的方式来获取name=q的元素
    input_fifth = browser.find_element(By.NAME, 'q')
    # 三个方式获取的结果是一致的
    print(input_first, input_second, input_third)
    # 用By的方式获取的元素与前三个一致
    print(input_fourth, input_fifth)
    browser.close()


def find_many_element():
    """
    查找指定条件的多个节点。
    :return:
    """
    browser = webdriver.Chrome()
    browser.get('https://www.taobao.com')
    # 查找淘宝首页使用了样式service-bd的元素内的所有li元素
    lis = browser.find_elements_by_css_selector('.service-bd li')
    print(lis)
    print(len(lis))
    print(lis[0].text, lis[0].id)
    # 使用By的方式指定按样式选择器,结果与上面的查询一致
    lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')
    print(lis)
    print(len(lis))
    print(lis[0].text, lis[0].id)
    browser.close()


def element_do():
    """
    元素交互
    :return:
    """
    browser = webdriver.Chrome()
    browser.get('https://www.taobao.com')
    # 获取淘宝首页的搜索框
    input = browser.find_element_by_id('q')
    # 输入iPhone
    input.send_keys('iPhone')
    time.sleep(3)
    # 清空文本框
    input.clear()
    time.sleep(3)
    # 输入iPad
    input.send_keys('iPad')
    time.sleep(3)
    # 获取class中包含btn-search的元素
    button = browser.find_element_by_class_name('btn-search')
    # 触发点击事件
    button.click()
    time.sleep(5)


def element_chains():
    """
    动作链演示
    :return:
    """
    # 导入动作链的类
    from selenium.webdriver import ActionChains

    browser = webdriver.Chrome()
    url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
    browser.get(url)
    # 把浏览器切换到指定id的iframe控件上
    browser.switch_to.frame('iframeResult')
    # 使用样式选择器查找iframe的页面中id=draggable的元素
    source = browser.find_element_by_css_selector('#draggable')
    # 使用样式选择器查找iframe的页面中id=droppable的元素
    target = browser.find_element_by_css_selector('#droppable')
    # 初始化动作链
    actions = ActionChains(browser)
    # 设定拖拽动作的起始位置和结束位置
    actions.drag_and_drop(source, target)
    # 执行动作链
    actions.perform()
    time.sleep(5)


def do_js():
    """
    selenium执行javascript
    :return:
    """
    browser = webdriver.Chrome()
    browser.get('https://www.zhihu.com/explore')
    # 执行js。把滚动条从顶拉到最底部
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    browser.execute_script('alert("To Bottom")')
    time.sleep(5)


def get_attr():
    """
    获取元素属性
    :return:
    """
    browser = webdriver.Chrome()
    url = 'https://www.zhihu.com/explore'
    browser.get(url)
    logo = browser.find_element_by_id('zh-top-link-logo')
    print(logo)
    # 获取class属性的值
    print(logo.get_attribute('class'))

    input = browser.find_element_by_class_name('zu-top-add-question')
    # 获取text属性的值
    print(input.text)
    
    # 获取id
    print(input.id)
    # 获取位置
    print(input.location)
    # 获取标签名
    print(input.tag_name)
    # 获取尺寸
    print(input.size)


def switch_iframe():
     """
     切换到指定的iframe中
     :return:
     """
     from selenium.common.exceptions import NoSuchElementException

     browser = webdriver.Chrome()
     url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
     browser.get(url)
     # 切换到id=iframeResult的iframe中
     browser.switch_to.frame('iframeResult')
     try:
         # 获取class中包含了logo的控件
         logo = browser.find_element_by_class_name('logo')
     except NoSuchElementException:
         print('NO LOGO')
     # 切换到父级iframe
     browser.switch_to.parent_frame()
     # 在上层iframe中查找logo为指定之
     logo = browser.find_element_by_class_name('logo')
     print(logo)
     print(logo.text)


def default_wait():
    """
    隐式等待
    :return:
    """
    browser = webdriver.Chrome()
    # 使用implicitly_wait实现隐式等待10秒
    browser.implicitly_wait(10)
    browser.get('https://www.zhihu.com/explore')
    input = browser.find_element_by_class_name('zu-top-add-question')
    print(input)


def default_wait_two():
    """
    显式等待。比隐式等待更易于控制
    :return:
    """
    browser = webdriver.Chrome()
    browser.get('https://www.taobao.com/')
    # 设定等待10秒。若设置的网页或接口超过10秒仍未返回结果则将抛出异常
    wait = WebDriverWait(browser, 10)
    input = wait.until(EC.presence_of_element_located((By.ID, 'q')))
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
    print(input, button)


def back_or_forward():
    """
    控制前进或后退
    :return:
    """
    browser = webdriver.Chrome()
    # 连续打开三个页面
    browser.get('https://www.baidu.com/')
    browser.get('https://www.taobao.com/')
    browser.get('https://www.python.org/')
    time.sleep(5)
    # 后退到第二个页面
    browser.back()
    # 休眠一秒
    time.sleep(5)
    # 前进到第三个页面
    browser.forward()
    time.sleep(5)
    browser.close()


def set_cookie():
    """
    通过selenium操作cookie
    :return:
    """
    browser = webdriver.Chrome()
    browser.get('https://www.zhihu.com/explore')
    # 获取cookie
    print(browser.get_cookies())
    # 添加新的cookie. 设置已存在的 cookie
    browser.add_cookie({'name': 'kamihati', 'domain': 'www.zhihu.com', 'value': 'germey'})
    print(browser.get_cookies())
    # 删除所有cookie
    browser.delete_all_cookies()
    print(browser.get_cookies())


def handle_option():
    """
    控制页面的选项卡
    :return:
    """
    browser = webdriver.Chrome()
    # 新建第一个选项卡打开百度首页
    browser.get('https://www.baidu.com')
    # 新建第二个选项卡
    browser.execute_script('window.open()')
    print(browser.window_handles)
    time.sleep(3)
    # 切换到第二个选项卡
    # browser.switch_to_window(browser.window_handles[1])
    browser.switch_to.window(browser.window_handles[1])
    # 第二个选项卡打开淘宝
    browser.get('https://www.taobao.com')
    time.sleep(3)
    # 切换到第一个选项卡
    # browser.switch_to_window(browser.window_handles[0])
    browser.switch_to.window(browser.window_handles[0])
    # 第一个选项卡打开python官网
    browser.get('https://python.org')


def handle_error():
    """
    异常处理
    :return:
    """
    from selenium.common.exceptions import TimeoutException, NoSuchElementException

    browser = webdriver.Chrome()
    browser.get('https://www.baidu.com')
    # 打开百度后查找一个并不存在的节点会抛出异常
    # browser.find_element_by_id('hello')
    
    # 添加异常处理
    try:
        browser.get('https://www.baidu.com')
    except TimeoutException:
        print('Time Out')
    try:
        browser.find_element_by_id('hello')
    except NoSuchElementException:
        print('No Element')
    finally:
        browser.close()


if __name__ == "__main__":
    handle_option()
