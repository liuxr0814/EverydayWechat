# coding=utf-8
"""
https://www.sojson.com/api/lunar.html
指定日期的节假日及万年历信息
"""
from datetime import datetime
import requests
from everyday_wechat.utils.common import (
    WEEK_DICT_NUM,
    SPIDER_HEADERS
)

__all__ = ['get_sojson_calendar']


def get_sojson_calendar(date=''):
    """
    获取指定日期的节假日及万年历信息
     https://www.sojson.com/api/lunar.html
    :param data: str 日期 格式 %Y-%m-%d
    :rtype str
    """
    date_ = date or datetime.now().strftime('%Y-%m-%d')
    # print('获取 {} 的日历...'.format(date_))
    try:
        params = {
            'ignoreHoliday': 'false',
            'app_id': 'yvqrrqnkipbhxroz',
            'app_secret': '2UHTMQLEUnxnyvkL1Roh10dxKs4jdNuY'
        }
        resp = requests.get('https://www.mxnzp.com/api/holiday/single/{}'.format(date_),
                            params=params,headers=SPIDER_HEADERS)

        if resp.status_code == 200:
            """
            {"code":1,"msg":"数据返回成功！","data":{"date":"2018-11-06","weekDay":2,"yearTips":"戊戌","type":0,"typeDes":"工作日","chineseZodiac":"狗","solarTerms":"霜降后","avoid":"移徙.入宅","lunarCalendar":"九月廿九","suit":"入殓.除服.成服.移柩.破土.启攒.安葬","dayOfYear":310,"weekOfYear":45,"constellation":"天蝎座","indexWorkDayOfMonth":4}}
            """
            content_dict = resp.json()
            if content_dict['code'] == 1:
                data_dict = content_dict['data']
                # 农历
                lunar_calendar = '{}'.format(data_dict['lunarCalendar'])
                # 二十四节气
                # solarTerms = data_dict['jieqi'].get(str(data_dict['day']), '')
                # print(data_dict['jieqi'])
                suit = data_dict['suit']
                suit = suit if suit else '无'
                avoid = data_dict['avoid']
                avoid = avoid if avoid else '无'
                return_text = '{date} {week} 农历{lunarCalendar}\n【宜】{suit}\n【忌】{avoid}'.format(
                    date=date,
                    week=WEEK_DICT_NUM[data_dict['weekDay']],
                    lunarCalendar=lunar_calendar,
                    suit=suit,
                    avoid=avoid,
                )
                return return_text
            else:
                print('获取日历失败:{}'.format(content_dict['message']))

        print('获取日历失败。')
    except Exception as exception:
        print(str(exception))
    return None


get_calendar = get_sojson_calendar

if __name__ == '__main__':
    date = datetime.now().strftime('%Y%m%d')
    date = '20181106'
    content = get_calendar(date)
    print(content)
    pass
