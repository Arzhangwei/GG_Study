from pickle import FALSE
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains


#***************************************变量定义********************************
isContinue =True
PageNo = 3

#***************************************函数定义********************************


    
#设置睡眠时间
def sleep(times):
    time.sleep(times)

#打印日志函数
def prt(msg):
    print(msg)

def  prit(msg,param):
    print(msg, param)





# 切换下面标签页
def Switch_next_Page(pageNum):
    #  /html/body/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/span/div
    prit("页数：",pageNum)
    try:
        # 使用JavaScript将页面滚动到底部
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 找到页数的输入框
        Page_num_input = driver.find_element(By.XPATH, "//*[@id='pane-NEWEST']/div[2]/div/span/div/input")
        # 使用js滚到要操作的位置
        driver.execute_script("arguments[0].scrollIntoView();", Page_num_input)
        # 清空输入框的值
        Page_num_input.clear()

        # 使用 send_keys 输入新的值
        Page_num_input.send_keys(pageNum)

        # 点击enter
        # pyautogui.press('enter')
        # 定位要点击的元素
        element_to_click = driver.find_element(By.XPATH,"//*[@id='pane-NEWEST']/div[2]/span")
        # 使用 ActionChains 模拟鼠标左键单击操作
        action = ActionChains(driver)
        action.click(element_to_click).perform()
        sleep(3)

    except Exception as e:
        print(f"函数Switch_next_Page:NoSuchElementException : {e}")


# 页面滚动函数
def Scroll_web(scroll_height):
    driver.execute_script(f"window.scrollBy(0, {scroll_height});")

# 点击按钮
def btnClick(xpath):
    driver.find_element(By.XPATH, xpath).click()


#***************************************主程序逻辑********************************
# 启动Chrome浏览器
op = webdriver.EdgeOptions()
op.add_experimental_option("detach" , True)
driver = webdriver.Edge(options=op)  # 实例化一个浏览器对象()

# 打开登录网页系统
driver.get('https://jypt.ahrcu.com/')
sleep(10)

# 登录系统
driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div[2]/div/div/div[2]/form/div[1]/div/div/input").send_keys("用户名")
driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[2]/div[2]/div/div/div[2]/form/div[2]/div/div/input").send_keys("密码")
driver.find_element(By.XPATH, "//*[@id='app']/div[1]/div/div[2]/div[2]/div/div/div[2]/form/div[4]/div/button").click()
# Continue with the rest of your script
# 等待5秒防止网络慢
sleep(10)

# 获取“首页”标签  登录后才有
person_data_str = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[1]/div/ul/li[1]/div/div[1]").text
if person_data_str == "首页":
    prt("登录成功")
else:
    prt("登陆失败")

# 切换到课程页面
driver.get('https://jypt.ahrcu.com/#/course/list')
sleep(10)
Scroll_web(1200)

while isContinue:
    
    for i in range(1, 21):
        if PageNo >= 2:
            Switch_next_Page(str(PageNo))
            sleep(15)
        try:
            # 点击图片进去课程detail
            # # //*[@id="pane-NEWEST"]/div[1]/div[2]/div/div/div[1]/div[3]/img
            xpath = f"//*[@id='pane-NEWEST']/div[1]/div[{i}]/div/div/div[1]/div[3]/img"
            prt(xpath)
            img_Course = driver.find_element(By.XPATH, xpath)
            # 使用JavaScript将页面滚动到要操作的控件可见的位置
            driver.execute_script("arguments[0].scrollIntoView();", img_Course)
            img_Course.click()
            sleep(10)
            
            # 判断课程状态是否开始学习
            is_finish_str = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/div[2]/div[2]/div[2]/div/button").text
            if is_finish_str == "已完成":
                print('已完成，换下一个')
                driver.back()
                sleep(8)
                continue
                
            elif is_finish_str == "取消学习":
                #获取所有的课程，然后循环学习每一课
                driver.back()
                sleep(8)
                continue
            else:
                #开始学习
                btnClick("/html/body/div[1]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/button")
                sleep(12)
                driver.back()
                sleep(8)
                continue
        except NoSuchElementException:
        # Handle the case when more_open_player_button is not found
        #single_open_player_button = driver.find_element(By.XPATH, "//*[@id='pane-course']/div/div/div/nav/div/div[1]/div[2]/i[2]")
        # Do something with single_open_player_button
            print("NoSuchElementException")
            time.sleep(5)
            continue
    
    PageNo += 1
    # 下一页的xpath /html/body/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/button[2]
    nextPage = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/button[2]")
    # 检查按钮是否可点击
    if nextPage.is_enabled():
         print("下一页可以点击")
        # nextPage.click()
        # Switch_next_Page(PageNo)
        # sleep(8)
    else:
        print("已经关注完所有课程，可以学习并获得积分。")
        break
