from appium import webdriver
import time

'''
appium实现ios真机自动下滑 但传给手机指令的时候真他妈卡
'''

# 上次到了数据库415

# # 模拟器
# desired_caps=dict()
# desired_caps["platformName"] = 'iOS'
# desired_caps["platformVersion"] = '13.5'
# desired_caps["deviceName"] = 'iPhone 11 Pro Max'
# desired_caps["app"] = 'barney.testSimulator'

# 真机
desired_caps=dict()
desired_caps["platformName"] = 'iOS'
desired_caps["platformVersion"] = '13.5.1'
desired_caps["deviceName"] = "Barney's iPhone"
# desired_caps["app"] = 'barney.testSimulator'
desired_caps["app"] = 'com.ss.iphone.ugc.Aweme'     # 抖音的bundleID
desired_caps["udid"] = '20f108541bf3da481621938d9250006ae0e31100'

quit=1
while True:
    try:
        # 得先开appium
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        print("Start Sleep")
        time.sleep(10)
        print("End Sleep")

        # 点击关注那栏
        driver.tap([(140, 67)], 500)
        print("点完了")
        time.sleep(5)

        # driver.find_element_by_id("com.ss.android.ugc.aweme:id").click()
        # print("搜完了")
        # time.sleep(10)

        # 先小滑一下 防止有直播的
        driver.swipe(150, 700, 150, 500)
        print("先滑一次")
        time.sleep(5)

        count=1
        while True:
            time.sleep(10)
            print("滑第"+str(count)+"次")
            driver.swipe(180,600,180,150,800)   # 注意最后一个参数如果不加 会过快变成点击 而不是滑动
            print("滑完了")
            count+=1
    except:
        quit+=1
        driver.quit()
        print("脑瘫软件appium")
        if(quit==10):
            break
        time.sleep(10)
        continue



# swipe用不了就用下面这个
# driver.execute_script("mobile: swipe",{"direction":"up"})


