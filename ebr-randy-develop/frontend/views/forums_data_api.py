from django.conf import settings
import requests
import json
from datetime import datetime


def forums_data_api():
    days = 180
    url = settings.IFRAME_URL + \
        '/forums/api/threads?direction=desc&order=last_post_date&last_days={}'
    headers = {'XF-Api-Key': settings.IFRAME_API_KEY}
    response = requests.get(url.format(days), headers=headers)
    data_list = []
    if response.status_code == 200:
        forums_list = json.loads(response.text)
        for i in forums_list['threads'][:11]:
            data_dict = {}
            data_dict['title'] = i['title']
            data_dict['forum'] = i['Forum']['title']
            data_dict['forum_link'] = i['Forum']['view_url']
            data_dict['link'] = i['view_url']
            data_dict['post_date'] = datetime.fromtimestamp(i['post_date'])
            data_list.append(data_dict)
    return data_list
