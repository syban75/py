import json
import threading

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import logging
import config
from time import localtime, strftime

from urllib.request import urlopen
from bs4 import BeautifulSoup

#
# env info
#

# log
logging.basicConfig(filename='%s\\test.log' % config.CONFIG['home_dir'],
                    level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

logger = logging.getLogger("")


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
            options.add_argument("user-data-dir=C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data")

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

        # 잔여백신으로 이동

        time.sleep(1)

        #       목동
        #        driver.get('https://m.place.naver.com/rest/vaccine?vaccineFilter=used'
        #                   '&x=126.8920805&y=37.4941623&bounds=126.7565539%3B37.4477041%3B127.0276072%3B37.5405917')

        # driver.get('https://m.place.naver.com/rest/vaccine?vaccineFilter=used'
        #           '&x=129.0822045&y=35.176542&bounds=128.9889924%3B35.1441233%3B129.1754167%3B35.2089478')

        # driver.get('https://m.place.naver.com/rest/vaccine?vaccineFilter=used'
        #           '&x=%s&y=%s&bounds=%s' % (config.CONFIG['x'], config.CONFIG['y'], config.CONFIG['bounds']))

        driver.get('https://m.place.naver.com/rest/vaccine?vaccineFilter=used'
                   '&x=%s&y=%s&bounds=%s' % (config.CONFIG['x'], config.CONFIG['y'], config.CONFIG['bounds']))

        time.sleep(1)

        return driver

    except Exception as ex:
        logger.info("login_naver 실패: %s " % ex)


# 백신을 가지고 있는 병원을 네이버잔여백신에서 접종예약신청
def test(driver):
    logger = logging.getLogger("register_rest_vaccine")
    try:
        driver.get('https://v-search.nid.naver.com/reservation/info?key=MUXfiMKzcRkDcVW')

        # 개인정보 수집 동의
        agree_btn = driver.find_element_by_xpath("//label[@for='check_all']")

        if agree_btn is not None:
            # agree_btn.click()
            driver.execute_script("arguments[0].click();", agree_btn)
            logger.info("register_rest_vaccine: check agree all")
        else:
            logger.info("register_rest_vaccine: already agree all")

        # 백신 영역 display
        exist_container = driver.find_element_by_id("info_item_exist")
        driver.execute_script("arguments[0].setAttribute('style','display: true;')", exist_container)

        empty_container = driver.find_element_by_id("info_item_empty")
        driver.execute_script("arguments[0].setAttribute('style','display: none;')", empty_container)

        # 화이자 백선 수량 선택

        # change as it says
        infobox_div = driver.find_element_by_xpath("//div[contains(@class,'info_box on')]")
        driver.execute_script("arguments[0].setAttribute('class','info_box off')", infobox_div)

        # 예약신청

        # 예약신청
        confirm_btn = driver.find_element_by_id("reservation_confirm")

        driver.execute_script("arguments[0].setAttribute('class','link_confirm on')", confirm_btn)

        confirm_btn = driver.find_element_by_id("reservation_confirm")
        driver.execute_script("arguments[0].click();", confirm_btn)

        logger.info("register_rest_vaccine: confirm")

    except Exception as ex:
        logger.info("register_rest_vaccine 실패: %s " % ex)


def check_naver_alarm(driver):
    logger = logging.getLogger("check_naver_alarm")
    try:

        # 네이버 알림화면에서 새로운 알림 확인
        driver.get("https://talk.naver.com/ct/w4ocfa")

        for i in range(1, 5):
            items = driver.find_elements_by_xpath(
                "//ul[@class='group_message_balloon']//li[contains(@class,'new_message_balloon_area')]")

            if len(items) == 0:
                time.sleep(0.1)
            else:
                break;

        # 최신 메세지
        item = items[len(items) - 1]

        # 시간 구하기
        alarm_time = item.find_element_by_class_name("_time").text

        logging.info("item length = %s, config.last_alarm_time = %s, alarm_time = %s " % (
            len(items), config.last_alarm_time, alarm_time))

        logging.info(item.text)
        if alarm_time == '':
            return False

        if config.last_alarm_time == '':
            # 처음 시작으로 제외
            config.last_alarm_time = alarm_time
            return False
        elif alarm_time == config.last_alarm_time:
            # 새로운 알람 없음
            return False

        # 새로운 알람
        """ 클릭보다 바로 접근
        # 지금 신청하기 클릭
        btn_basic = item.find_element_by_class_name("btn_basic")
        btn_basic.click()
        """

        register_url = item.find_element_by_class_name("btn_basic").get_attribute("href")

        driver.get(register_url)

        # 예약신청
        # logger.info("register_rest_vaccine: find confirm button")
        confirm_btn = driver.find_element_by_id("reservation_confirm")

        # logger.info("register_rest_vaccine: click confirm button")
        # driver.execute_script("arguments[0].click();", confirm_btn)
        confirm_btn.click()

        time.sleep(1)

        logger.info("check_naver_alarm: confirm")

        for i in range(1, 100):
            response_url = "%s" % driver.current_url

            if response_url.find("progress") != -1:
                logger.info("check_naver_alarm: progress to reserve: %s" % driver.current_url)
                time.sleep(1)
                continue
            elif response_url.find("failure") != -1:
                logger.info("check_naver_alarm: fail to reserve: %s" % driver.current_url)
                break
            elif response_url.find("success") != -1:
                logger.info("check_naver_alarm: success to reserve: %s" % driver.current_url)
                time.sleep(3)
                return True
            else:
                logger.info("check_naver_alarm: unknown to reserve: %s" % driver.current_url)
                time.sleep(3)

        time.sleep(3)

        # 마지막 변경
        config.last_alarm_time = alarm_time

    except Exception as ex:
        logger.info("check_naver_alarm 실패: %s " % ex)

    return False


def check_naver_alarm2(driver):
    logger = logging.getLogger("check_naver_alarm")
    try:

        # 네이버 알림화면에서 새로운 알림 확인
        driver.get("https://talk.naver.com/ct/w4ocfa")

        ele = driver.find_element_by_id('__NEXT_DATA__')

        # logger.info(ele.get_attribute("innerHTML"))

        resp_json_data = json.loads(ele.get_attribute("innerHTML"))

        # logger.info(resp_json_data)

        messageList_json = resp_json_data.get("props").get('pageProps').get('userChatConfig').get('config').get(
            'messageList')

        item = messageList_json[len(messageList_json) - 1]

        logger.info(item)

        # 시간 구하기
        alarm_time = item.get('date')
        register_url = item.get('customContent').get('linkList')[0].get('url')

        logging.info(" config.last_alarm_time = %s, alarm_time = %s " % (config.last_alarm_time, alarm_time))

        if alarm_time == '':
            return False

        if config.last_alarm_time == '':
            # 처음 시작으로 제외
            config.last_alarm_time = alarm_time
            return False
        elif alarm_time == config.last_alarm_time:
            # 새로운 알람 없음
            return False

        # 새로운 알람
        """ 클릭보다 바로 접근
        # 지금 신청하기 클릭
        btn_basic = item.find_element_by_class_name("btn_basic")
        btn_basic.click()
        """

        driver.get(register_url)

        # 예약신청
        # logger.info("register_rest_vaccine: find confirm button")
        confirm_btn = driver.find_element_by_id("reservation_confirm")

        # logger.info("register_rest_vaccine: click confirm button")
        # driver.execute_script("arguments[0].click();", confirm_btn)
        confirm_btn.click()

        time.sleep(1)

        logger.info("check_naver_alarm: confirm")

        for i in range(1, 100):
            response_url = "%s" % driver.current_url

            if response_url.find("progress") != -1:
                logger.info("check_naver_alarm: progress to reserve: %s" % driver.current_url)
                time.sleep(1)
                continue
            elif response_url.find("failure") != -1:
                logger.info("check_naver_alarm: fail to reserve: %s" % driver.current_url)
                break
            elif response_url.find("success") != -1:
                logger.info("check_naver_alarm: success to reserve: %s" % driver.current_url)
                time.sleep(3)
                return True
            else:
                logger.info("check_naver_alarm: unknown to reserve: %s" % driver.current_url)
                time.sleep(1)

        time.sleep(3)

        # 마지막 변경
        config.last_alarm_time = alarm_time

    except Exception as ex:
        logger.info("check_naver_alarm 실패: %s " % ex)

    return False


def check_naver_alarm3(driver):
    logger = logging.getLogger("check_naver_alarm")
    try:

        url = "https://talk.naver.com/ct/w4ocfa"

        headers = {'cookie': '%s' % driver.get_cookies(),
                   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'}

        resp = requests.get(url, headers=headers)

        logger.info("response status: %d" % resp.status_code);
        logger.info("response body:\n%s" % resp.content);

        soup = BeautifulSoup(resp.text, "html5lib")

        ele = soup.find(id="__NEXT_DATA__")

        resp_json_data = json.loads(ele.decode_contents())

        # logger.info(resp_json_data)

        message_list_json = resp_json_data.get("props").get('pageProps').get('userChatConfig').get('config').get(
            'messageList')

        item = message_list_json[len(message_list_json) - 1]

        logger.info(item)

        # 시간 구하기
        alarm_time = item.get('date')
        register_url = item.get('customContent').get('linkList')[0].get('url')

        logging.info(" config.last_alarm_time = %s, alarm_time = %s " % (config.last_alarm_time, alarm_time))

        if alarm_time == '':
            return False

        if config.last_alarm_time == '':
            # 처음 시작으로 제외
            config.last_alarm_time = alarm_time
            return False
        elif alarm_time == config.last_alarm_time:
            # 새로운 알람 없음
            return False

        # 새로운 알람
        driver.get(register_url)

        # 예약신청
        # logger.info("register_rest_vaccine: find confirm button")
        confirm_btn = driver.find_element_by_id("reservation_confirm")

        # logger.info("register_rest_vaccine: click confirm button")
        # driver.execute_script("arguments[0].click();", confirm_btn)
        confirm_btn.click()

        time.sleep(1)

        logger.info("check_naver_alarm: confirm")

        for i in range(1, 100):
            response_url = "%s" % driver.current_url

            if response_url.find("progress") != -1:
                logger.info("check_naver_alarm: progress to reserve: %s" % driver.current_url)
                time.sleep(1)
                continue
            elif response_url.find("failure") != -1:
                logger.info("check_naver_alarm: fail to reserve: %s" % driver.current_url)
                break
            elif response_url.find("success") != -1:
                logger.info("check_naver_alarm: success to reserve: %s" % driver.current_url)
                time.sleep(3)
                return True
            else:
                logger.info("check_naver_alarm: unknown to reserve: %s" % driver.current_url)
                time.sleep(1)

        time.sleep(3)

        # 마지막 변경
        config.last_alarm_time = alarm_time

    except Exception as ex:
        logger.info("check_naver_alarm 실패: %s " % ex)

    return False


# 네이버 로그인
def login_naver_alarm():
    logger = logging.getLogger("login_naver")
    try:
        # alarm 브라우저 프로필 가져오기, 새 머신에서는 네이버 브라우저 등록, 인증서 등록할것

        if config.CONFIG['browser'] == 'chrome':

            #
            # naver에서 navigator.webdriver 채크함. 아래 옵션으로 navigator.webdriver 채크 피하기
            #

            options = webdriver.ChromeOptions()
            options.add_argument("user-data-dir=%s\\Chrome\\AlarmUser" % config.CONFIG['home_dir'])

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

        # 잔여백신으로 이동

        time.sleep(1)

        driver.get('https://talk.naver.com/ct/w4ocfa')

        time.sleep(1)

        return driver

    except Exception as ex:
        logger.info("login_naver 실패: %s " % ex)


def alarm_threading_main():
    # naver으로 login
    driver = login_naver_alarm()

    for i in range(1, 2):
        check_naver_alarm3(driver)
        time.sleep(2)


#
# main
#

logging.info('start sylvan')

# naver으로 login
# my_driver = login_naver()


# t = threading.Thread(target=alarm_threading_main)
# t.start()
