from aiohttp_requests import requests
import aiohttp
import os
import xml.etree.ElementTree as et


login_url = "https://edoga.dogakoleji.com/login?ignorelivelesson=true"
join_class_url = "https://uygulama.sebitvcloud.com/VCloudFrontEndService/livelesson/instudytime/start"
join_url = "sbtzoom:o={0}&m={1}&t={2}"
class_list_url = "https://uygulama.sebitvcloud.com/VCloudFrontEndService/studytime/getstudentstudytime"
get_auth_url = "https://uygulama.sebitvcloud.com/VCloudFrontEndService/home/user/getuserinfo"


async def is_logged_in(sid):
    request = await requests.post(get_auth_url, cookies={'sid': sid})
    return request.status == 200


async def get_cookies(username, password):
    data = {
      "l_op": "tibeslogin",
      "l_un": username,
      "l_pw": password,
      "l_kmli": 'false',
      "l_ru": "undefined"
    }
    
    request = await requests.post(login_url, data=data)
    xml_root = et.fromstring(await request.content.read())
    sid_value = xml_root[2].text
    if not sid_value:
        return False
    if 'captcha' in sid_value:
        return False
    cookies = {'sid': sid_value}
    return cookies


async def get_latest_class_id(cookie, status, index):
    data = {
        "status": str(status),
        "type": "2"
    }
    request = await requests.get(class_list_url, params=data, cookies=cookie)
    class_list = dict(await request.json())
    total_records = class_list['totalRecords']
    if not total_records:
        return False
    if index > len(class_list['studyTimeList']):
        index = len(class_list['studyTimeList'])
    latest_class_id = class_list['studyTimeList'][index-1]['id']
    
    return latest_class_id


async def get_join_info(class_id, cookies):
    data = {
        "studytimeid": class_id
    }
    request = await requests.post(join_class_url, data=data, cookies=cookies)
    id_json = dict(await request.json())
    if not id_json:
        return None
    meeting_dict = id_json['meeting']
    if not meeting_dict:
        return None
    meeting_id = meeting_dict['meetingId']
    password = meeting_dict['token'][-32:]
    class_name = meeting_dict['topic']
    start_time = meeting_dict['startDate']
    return [meeting_id, password, class_name, start_time]


def launch_meeting(meeting_id, token, access='join'):
    link = join_url.format(access, meeting_id, token)
    os.startfile(link)


def get_credits():
    if not os.path.exists('../../edogaCreds.txt'):
        file = open('../../edogaCreds.txt', 'w+')
        file.close()
    with open('../../edogaCreds.txt', 'r+') as auth:
        auth_info = auth.readlines()
        if len(auth_info) == 2:
            creds = [int(auth_info[0]), int(auth_info[1])]
            print('Hesap bulundu. T.C.: {0}, Şifre: {1}'.format(int(auth_info[0]), int(auth_info[1])))
        else:
            creds = list(input("[T.C. No] [şifre]: ").split())
            auth.writelines([creds[0], '\n', creds[1]])
        auth.close()
    return creds


async def main():
    credits_ = get_credits()
    cookies = get_cookies(credits_[0], credits_[1])
    latest_class = await get_latest_class_id(cookies, 0)
    join_info = get_join_info(latest_class, cookies)
    print('Ders Bulundu: {}. Katılınıyor.'.format(join_info[2]))
    launch_meeting(join_info[0], join_info[1])
    

if __name__ == "__main__":
    main()
    input()
