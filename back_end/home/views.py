from django.shortcuts import render
from common.models import CveInfo, DatabaseIndicator,CveInfoPlus
from common.views import getMenu
from django.http import HttpResponse
import json
import urllib.request
import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# Create your views here.
from common.Post_loader import *

reverse_stem_map = PostLoader().load_pickle('/output/stemmed_aspect_map_single.pkl')

def clean_aspects(i):
    for one_aspect in ['product']:
        if i.get(one_aspect) is not None:
            aspect_list = i[one_aspect].split(';')
            clean_list = ['('.join(one_ele.strip().split('(')[:-1]) if '(' in one_ele else one_ele.strip() for one_ele in aspect_list]
            postfix_list = ['('+one_ele.strip().split('(')[-1] if '(' in one_ele else '' for one_ele in aspect_list]
            clean_list = [reverse_stem_map[one_ele] if reverse_stem_map.get(one_ele) is not None else one_ele for one_ele in clean_list]
            clean_list = [clean_list[i] + postfix_list[i] for i in range(len(clean_list))]
            i[one_aspect] = ';'.join(clean_list)

def getLatestCve(request):
    try:
        qs = CveInfoPlus.objects.values()
        # qs=CveInfoPlus.objects.values()
        # 将QuerySet对象转化为list类型
        # 否则不能被转化为Json字符串
        cvelist = list(qs)
        latestcves=cvelist[-51:-1]
        # print('最新的cves', latestcves)

        for cve_idx, cve in enumerate(latestcves):
            urlsObj = DatabaseIndicator.objects.get(cveid=cve['cveid'])
            urls=object_to_json(urlsObj)
            del urls['_state']
            print('urls:', urls)
            cve['urls']=urls
            # clean_aspects(latestcves[cve_idx])


        menu = getMenu(latestcves)

        returndata = {'latestcves':latestcves, 'menu':menu}
        # return JsonResponse({'ret': 0,'latestcve': retlist[-1]})
        return HttpResponse(json.dumps(returndata), status=200)
    except Exception as e:
        print(e)
        # return JsonResponse()
        return HttpResponse("error", status=400)



# objects.get()结果转换
def object_to_json(obj):
    ans={}
    # obj.__dict__ 可将django对象转化为字典
    for key, value in obj.__dict__.items():
        # 将字典转化为JSON格式
        ans[key]=value
    return ans


# 根据url获取网页html
def getHtmlByUrl(response):
    try:
        url = r'https://exchange.xforce.ibmcloud.com/vulnerabilities/192897'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        print(html)
        return HttpResponse(html, status=200)

    except Exception as e:
        print(e)
        # return JsonResponse()
        return HttpResponse("error", status=400)
