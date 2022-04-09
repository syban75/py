import os

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import logging
import random
import config

#
# env info
#

# log
logging.basicConfig(filename='%s\\pawn.log' % os.getcwd(),
                    level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(message)s')

logging.Formatter(datefmt='%m-%d,%H:%M:%S.%f')


# 네이버 로그인
def login_naver():
    logger = logging.getLogger("login_naver")
    try:
        # 기본 브라우저 프로필 가져오기, 없으면 계속 브라우저 등록하라고 뜸.
        if config.CONFIG['browser'] == 'chrome':

            #
            # naver에서 navigator.webdriver 채크함. 아래 옵션으로 navigator.webdriver 채크 피하기
            #

            options = webdriver.ChromeOptions()
            options.add_argument("user-data-dir=C:\\Users\\syban\\AppData\\Local\\Google\\Chrome\\User Data")
            # options.add_argument("user-data-dir=D:\\py\\Pawn\\Chrome\\User Data")

            # options.add_argument("start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")
            # browser 표시 여부, browser 띄우면 병원페이지 0.5초 예약페이지 0.5초 걸림
            # options.add_argument("--headless");

            # naver 로그인
            driver = webdriver.Chrome(options=options)

            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.53 Safari/537.36'})
            logger.info(driver.execute_script("return navigator.userAgent;"))

        elif config.CONFIG['browser'] == 'firefox':
            fp = webdriver.FirefoxProfile('C:\\Users\\user\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles'
                                          '\\2cyrg3xs.default-release')
            driver = webdriver.Firefox(firefox_profile=fp)

        driver.get('https://nid.naver.com/nidlogin.login')

        # id, pw 입력할 곳을 찾습니다.
        tag_id = driver.find_element_by_name('id')
        tag_pw = driver.find_element_by_name('pw')
        tag_id.clear()
        time.sleep(1)

        # id 입력
        tag_id.click()
        tag_id.clear()
        pyperclip.copy(config.CONFIG['naver_id'])
        tag_id.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # pw 입력
        tag_pw.click()
        tag_pw.clear()
        pyperclip.copy(config.CONFIG['naver_pw'])
        tag_pw.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 로그인 버튼을 클릭합니다
        login_btn = driver.find_element_by_id('log.login')
        login_btn.click()

        # cgv 이동
        time.sleep(1)

        driver.get('http://naver.com')
        # driver.get('http://www.cgv.co.kr/movies/detail-view/?midx=85715')

        time.sleep(1)

        return driver

    except Exception as ex:
        logger.info("login_naver 실패: %s " % ex)


# cgv 로그인
def login_cgv():
    logger = logging.getLogger("login_cgv")
    try:
        # 기본 브라우저 프로필 가져오기, 없으면 계속 브라우저 등록하라고 뜸.
        if config.CONFIG['browser'] == 'chrome':

            #
            # naver에서 navigator.webdriver 채크함. 아래 옵션으로 navigator.webdriver 채크 피하기
            #

            options = webdriver.ChromeOptions()
            options.add_argument("user-data-dir=C:\\Users\\syban\\AppData\\Local\\Google\\Chrome\\User Data")

            # options.add_argument("start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")
            # browser 표시 여부, browser 띄우면 병원페이지 0.5초 예약페이지 0.5초 걸림
            # options.add_argument("--headless");

            # naver 로그인
            driver = webdriver.Chrome(options=options)

            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/83.0.4103.53 Safari/537.36'})
            logger.info(driver.execute_script("return navigator.userAgent;"))

        elif config.CONFIG['browser'] == 'firefox':
            fp = webdriver.FirefoxProfile('C:\\Users\\user\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles'
                                          '\\2cyrg3xs.default-release')
            driver = webdriver.Firefox(firefox_profile=fp)

        driver.get('https://www.cgv.co.kr/user/login/?returnURL=https%3a%2f%2fwww.cgv.co.kr%2fdefault.aspx')

        # id, pw 입력할 곳을 찾습니다.
        tag_id = driver.find_element_by_name('txtUserId')
        tag_pw = driver.find_element_by_name('txtPassword')
        tag_id.clear()
        time.sleep(1)

        # id 입력
        tag_id.click()
        tag_id.clear()
        pyperclip.copy(config.CONFIG['cgv_id'])
        tag_id.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # pw 입력
        tag_pw.click()
        tag_pw.clear()
        pyperclip.copy(config.CONFIG['cgv_pw'])
        tag_pw.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 로그인 버튼을 클릭합니다
        login_btn = driver.find_element_by_id('submit')
        login_btn.click()

        # cgv 이동
        time.sleep(1)

        #driver.get('https://www.cgv.co.kr/default.aspx')
        #driver.get('http://www.cgv.co.kr/movies/detail-view/?midx=85715')
        #time.sleep(1)

        return driver

    except Exception as ex:
        logger.info("login_cgv 실패: %s " % ex)


# line으로 메세지 보내기
def send_line_message(message):
    try:
        logger = logging.getLogger("send_line_message")

        target_url = 'https://notify-api.line.me/api/notify'

        token = config.CONFIG["line_token"]

        response = requests.post(
            target_url,
            headers={

                'Authorization': 'Bearer ' + token

            },
            data={

                'message': message
            }
        )

        logger.info(response)

    except Exception as ex:
        logger.info("send_line_message 실패: %s " % ex)


# 영화가 예약상태가 되었는지 확인하고 알람
def check_strange(driver, movie_url):
    logger = logging.getLogger("check_strange")
    try:
        driver.get(movie_url)

        btn_reservation = driver.find_element_by_class_name("link-reservation")

        print(btn_reservation)

        send_line_message("닥터스트레인지2 예약 버튼 활성화!!")

        return True

    except NoSuchElementException:
        logger.info("DrStrange Booking is not available")
        return False

    except Exception as ex:
        logger.info("check_strange 실패: %s " % ex)

    return False


#
# main
#

logger = logging.getLogger("main")
logging.info('start pawn in %s' % os.getcwd())

send_line_message("닥터스트레인지2 예매 확인 시작")

# naver으로 login
my_driver = login_cgv()

strange_url = 'http://www.cgv.co.kr/movies/detail-view/?midx=85715'
#strange_url = 'http://www.cgv.co.kr/movies/detail-view/?midx=85712'

# 확인 루프
for count in range(1, 100000):

    booking = check_strange(my_driver,strange_url)

    if booking is True:
        send_line_message("닥터스트레인지2 예매 가능!! \n %s" % strange_url)

        break

    # 가끔식 화면 refresh
    if count % 30 == 0:
        my_driver.switch_to.window(my_driver.window_handles[0])

        my_driver.get(strange_url)

    # 가끔식 메세지 보내기
    #if count % 30 == 0 and booking is False:
    #    send_line_message("닥터스트레인지2는 아직 예매 가능하지 않음.")

    # 매크로방지 피하기 위해서 1초~3초 랜덤하게 쉬기
    time.sleep(random.randrange(1, 3))
