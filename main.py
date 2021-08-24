from selenium import webdriver
from scrapy import Request,Spider
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from parse_info import parseinfo
from items import create_HotelBasicInfo,create_HotelRoomItem
from items import create_HotelBasicInfo,create_HotelRoomItem
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from .parse_info import parseinfo,parse_hotel_basic_info,parse_hotel_room_info
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
if __name__ == '__main__':
    waittime=5
    login_url = "https://passport.ctrip.com/user/login?BackUrl=https%3A%2F%2Fhotels.ctrip.com%2F#ctm_ref=c_ph_login_buttom"
    hotel_aceess_baseurl = "https://hotels.ctrip.com/hotels/list?countryId=1&city={0}&checkin=2021/03/25&checkout=2021/03/26&optionId={0}&optionType=City&directSearch=1&optionName={1}&display={1}&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1"
    browser = webdriver.Firefox()
    browser.set_window_size(1200, 600)
    browser.get(login_url)
    browser.find_element_by_id("nloginname").send_keys("*********")
    browser.find_element_by_id("npwd").send_keys("********")
    browser.find_element_by_xpath("//input[@id='nsubmit']").click()
    time.sleep(waittime)
    # cookies = browser.get_cookies()  # selenium获得的浏览器cookie
    # cookies_req = {}  # Request格式的cookies
    # # for cookie in cookies:
    #     cookies_req[cookie['name']] = cookie['value']
    cityID = [i for i in range(1,23)]
    hotelnames = ['7天', '汉庭','如家', '锦江之星', '尚客优', '格林豪泰', '易佰', '城市便捷酒店' ]
    for i in cityID:
        for j in hotelnames:
            hotel_access_url = hotel_aceess_baseurl.format(i, j)
            browser.get(hotel_access_url)
            brand_name = j
            hotel_locate_city = browser.find_element_by_xpath("//input[@id='hotels-destination']").get_attribute("value")
            for i in range(2):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(waittime)
            time.sleep(waittime)
            while browser.find_elements_by_class_name("list-btn-more") !=[]:
                browser.find_element_by_css_selector("div.btn-box>span").click()
                time.sleep(waittime)
            hotels = browser.find_elements_by_css_selector("span.name.font-bold")
            for hotel in hotels:  # 遍历检索到的全部酒店
                hotel.click()
                time.sleep(waittime)
                tabs = browser.window_handles
                browser.switch_to.window(tabs[1])
                browser.close()
                browser.switch_to.window(tabs[0])
                # parseinfo(browser,brand_name,hotel_locate_city)


