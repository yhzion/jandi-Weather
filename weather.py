# coding=utf-8
import json
import urllib
import urllib2
import sys
import os

__author__ = 'jsuch2362'


def main():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid = %s and u='c'" % os.environ['woeid']
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json&u=c"
    print "yql_url : " + yql_url
    result = urllib2.urlopen(yql_url).read()

    data = json.loads(result)
    result = data['query']['results']
    channel = result['channel']
    item = channel['item']
    current = item['condition']
    forecast = item['forecast']
    current_forecast = forecast[0]

    webhook_data = {}
    webhook_data['body'] = '오늘의 날씨 중계 feat. [Yahoo 날씨 보기](' + channel['link'] + ')'
    webhook_data['connectInfo'] = ['','','']
    webhook_data['connectInfo'][0] = {
        'title': '오늘의 날씨는 최고 : ' + current_forecast['high'] + '\'C 최저 : ' + current_forecast['low'] + '\'C 입니다'}
    webhook_data['connectInfo'][1] = {'description': '현재 온도는 ' + current['temp'] + '\'C 입니다'}
    webhook_data['connectInfo'][2] = {'description': '현재 날씨는 ' + current['text'] + ' 입니다'}

    webhook_url = os.environ['webhook_url']

    req = urllib2.Request(webhook_url, json.dumps(webhook_data))
    req.add_header('Accept', 'application/vnd.tosslab.jandi-v2+json')
    req.add_header('Content-Type', 'application/json')
    urllib2.urlopen(req)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()
