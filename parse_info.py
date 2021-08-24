import time
from items import create_HotelBasicInfo,create_HotelRoomItem,create_HotelServices
from saveData import save2Mysql
def parseinfo(browser,brand_name,hotel_locate_city):
    tabs = browser.window_handles
    browser.switch_to.window(tabs[1])
    item1=create_HotelBasicInfo()
    item1=parse_hotel_basic_info(item1,brand_name,hotel_locate_city,browser)
    save2Mysql(item1,table='HotelBasicInfo')
    item2 = parse_hotel_services(browser, brand_name)
    save2Mysql(item2, table='HotelServices')
    roomlist=browser.find_elements_by_css_selector("div.roomlist-baseroom>div")#获取房型数量
    for i in roomlist:#解析房型
        time.sleep(1)
        parse_hotel_room_info(brand_name,browser,i,item1['hotel_name'])
    browser.close()
    browser.switch_to.window(tabs[0])
def parse_hotel_basic_info(item1,brand_name,hotel_locate_city,browser):
    item1['brand_name']=brand_name
    item1['hotel_name'] = str(browser.find_element_by_css_selector("h1.detail-headline_name ").text).strip()
    item1['city']=hotel_locate_city
    item1['location']=str(browser.find_element_by_css_selector("span.detail-headline_position_text").text).strip()
    eles=browser.find_elements_by_css_selector('div.m-hoteldesc_basic>ul>li')
    for ele in eles:
        name=(ele.text.strip())[:2]
        if name=='开业':
            item1['openning_hour']=(ele.text.strip())[3:]
            continue
        if name=="客房":
            item1['room_number']=(ele.text.strip())[4:]
            continue
    # item1['room_number']=str(browser.find_elements_by_css_selector("ul.basicInfo.clearfix>li")[2].text).strip()[4:]
    # item1['openning_hour']=int(str(browser.find_elements_by_css_selector("ul.basicInfo.clearfix>li")[0].text).strip()[3:])
    item1['brief_introduction']=str(browser.find_element_by_css_selector("div.m-h-d-eclips-ie.text-ellipsis-4>span").text).strip()
    browser.find_element_by_css_selector('span.detail-headtraffic_traffic_showmore').click()
    time.sleep(1)
    traffic_info=''
    loop=browser.find_elements_by_css_selector('div.detail-map-poilist_category')
    for i in loop:
        traffic_way=i.find_element_by_css_selector('h3.detail-map-poilist_category_title').text+':'#出行方式
        # traffic_clear1=i.find_element_by_css_selector('p.detail-map-poilist_item_title')[i].text+'#'
        num=i.find_elements_by_css_selector('div.detail-map-poilist_item_content')#每种交通方式具体距离
        traffic_all=''
        for j in num:
            traffic_1=j.find_element_by_css_selector('p.detail-map-poilist_item_title').text#具体交通方式
            traffic_2=j.find_element_by_css_selector('p.detail-map-poilist_item_poi').text#距离
            traffic_all=traffic_all+traffic_1+'#'+traffic_2+';'
        traffic_info=traffic_info+traffic_way+traffic_all+'\n'
    item1['traffic_info']=traffic_info
    if browser.find_elements_by_css_selector('b.detail-headreview_score_value')!=[]:
        item1['evaluate_score']=browser.find_element_by_css_selector('b.detail-headreview_score_value').text
    browser.find_element_by_css_selector('i.u-icon.u-icon-close.detail-map-list_close').click()
    print("item1{0}\n".format(item1))
    return item1

def parse_hotel_services(browser, brand_name):
    parking_lot=''
    net_service=''
    front_service=''
    food_service=''
    common_facility=''
    public_facility= ''
    # button=browser.find_elements_by_css_selector('button.u-btn.u-btn-outline.u-btn-xs.u-btn-radiuslg.u-btn-iconRight')
    # if button!=[]:
    #     button[0].click()
    item2=create_HotelServices()
    item2['brand_name']=brand_name
    item2['hotel_name']=browser.find_element_by_css_selector("h1.detail-headline_name ").text.strip()
    time.sleep(2)

    policies=browser.find_elements_by_css_selector('div.m-policy_main>div')
    for i in policies:
        limit = i.find_element_by_css_selector('div.m-hp-left').text.strip()
        if limit == '停车场':
            eles=i.find_elements_by_css_selector('li.itemTxt')
            for ele in eles:
               parking_lot+=ele.text.strip()+'#'
            item2['parking_lot']=parking_lot
            continue
        if limit == '宠物':
            item2['pets_limit']=i.find_element_by_css_selector('p.itemTxt').text.strip()
            continue
    services=browser.find_elements_by_css_selector('div.m-hotelfacility_con')
    for service in services:
        service_name=str(service.find_element_by_css_selector('div.itemTit.m-hf-left').text.strip())
        if service_name=="网络":
            service_net=service.find_elements_by_css_selector('li.icon-item')
            for i in service_net:
                net_service=net_service+i.find_element_by_css_selector('span.facilityDesc').text.strip()+'#'
            item2['net_service']=net_service
            continue
        elif service_name=='前台服务':
            service_front = service.find_elements_by_css_selector('li.icon-item')
            for i in service_front:
                front_service=front_service+i.find_element_by_css_selector('span.facilityDesc').text.strip()+'#'
            item2['front_service']=front_service
            continue
        elif service_name=='餐饮服务':
            service_food = service.find_elements_by_css_selector('li.icon-item')
            for i in service_food:
                food_service = food_service + i.find_element_by_css_selector('span.facilityDesc').text.strip()+'#'
            item2['food_service'] = food_service
            continue
        elif service_name=='通用设施':
            facility_common = service.find_elements_by_css_selector('li.icon-item')
            for i in facility_common:
                common_facility = common_facility + i.find_element_by_css_selector('span.facilityDesc').text.strip()+'#'
            item2['common_facility'] = common_facility
            continue
        elif  service_name=='公共设施':
            facility_public = service.find_elements_by_css_selector('li.icon-item')
            for i in facility_public:
                public_facility = public_facility + i.find_element_by_css_selector('span.facilityDesc').text.strip()
            item2['public_service'] = public_facility
            continue
        print("item2{0}\n".format(item2))
    return item2

def parse_hotel_room_info(brand_name,browser,room,hotel_name):
    specific_rooms=room.find_elements_by_css_selector("div.ubt-salecard.salecard")
    bathroom_facility=''
    convenient_facility=''
    toiletries_facility=''
    media_facility=''
    edible_drinks=''
    for i in specific_rooms:
        item3=create_HotelRoomItem()
        room.find_element_by_css_selector('div.seeroom').click()
        item3['brand_name'] = brand_name
        item3['hotel_name'] = hotel_name
        item3['room_window'] =i.find_elements_by_css_selector('div.salecard-otherfacility>div')[1].find_element_by_css_selector('span.desc-text').text.strip()
        item3['room_price']=i.find_element_by_css_selector('div#detail-real-price').text.strip()
        item3['room_breakfast']=i.find_element_by_css_selector('div.bedfacility>div.facility>div>span').text.strip()
        item3['beds']=i.find_element_by_css_selector('div.bed span').text.strip()
        item3['room_name']=browser.find_element_by_css_selector('div.m-title.room').text.strip()
        item3['room_square']=browser.find_element_by_css_selector('div.icon-with-text-fullLine>span').text.strip()
        all_facility=browser.find_elements_by_css_selector('div.m-room-facility>ul>li')
        for facility in all_facility:
            facility_name=facility.find_element_by_css_selector('div.m-facility>h3').text.strip()
            if facility_name=='浴室':
                eles=facility.find_elements_by_css_selector('div.icon-with-text')
                for j in eles:
                    bathroom_facility += '#'+j.find_element_by_css_selector("span").text.strip()
                item3['bathroom_facility']=bathroom_facility
                continue
            if facility_name=='洗浴用品':
                eles = facility.find_elements_by_css_selector('div.icon-with-text')
                for j in eles:
                    toiletries_facility += '#'+j.find_element_by_css_selector("span").text.strip()
                item3['toiletries_facility']=toiletries_facility
                continue
            if facility_name=='便利设施':
                eles = facility.find_elements_by_css_selector('div.icon-with-text')
                for j in eles:
                    convenient_facility += '#'+j.find_element_by_css_selector("span").text.strip()
                item3['convenient_facility']=convenient_facility
                continue
            if facility_name=='媒体科技':
                eles = facility.find_elements_by_css_selector('div.icon-with-text')
                for j in eles:
                    media_facility += '#'+j.find_element_by_css_selector("span").text.strip()
                item3['media_facility']=media_facility
                continue
            if facility_name=='食品饮品':
                eles = facility.find_elements_by_css_selector('div.icon-with-text')
                for j in eles:
                    edible_drinks += '#'+j.find_element_by_css_selector("span").text.strip()
                item3['edible_drinks']=edible_drinks
                continue
        browser.find_element_by_css_selector('i.u-icon.u-icon-ic_new_close_line').click()
        time.sleep(1)
        print("item3{0}\n".format(item3))
        save2Mysql(item3,'HotelRoomInfo')
