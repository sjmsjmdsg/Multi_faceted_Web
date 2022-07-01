from django.core import serializers
from django.core.serializers import serialize
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.db.models import Q

from .TextPreprocess import *
import tqdm
import time

from functools import reduce
import operator
# Create your views here.


from common.models import CveInfo, AspectCvssInfo, AspectCompare, CveInfoPlus, DatabaseIndicator, AspectMultiInfoNew
from home.models import Aspect2Table, Aspect2Year, Aspect2CvssYear, WebClickNums, Phrase2Cve, WordThesaurus, WordType2, Word2Cve

# 全局变量
searchQS=[]


new_type2th = PostLoader().load_pickle('/output/type_thesaurus_new.pkl')
new_type = PostLoader().load_pickle('/output/word_type_new.pkl')
new_phrase = PostLoader().load_pickle('/output/phrase2cve_new.pkl')
new_w2cve = PostLoader().load_pickle('/output/word2cve_new.pkl')
new_cve2w = PostLoader().load_pickle('/output/cve2word_new.pkl')
new_th2type = PostLoader().load_pickle('/output/thesaurus_type_new.pkl')
reverse_stem_map = PostLoader().load_pickle('/output/stemmed_aspect_map_single.pkl')

# 教学：返回网站访问次数，该数据表只有一条记录
def returnClickNums(requset):
  try:
      # 网站访问次数
      obj = WebClickNums.objects.get(id=1)
      obj.clickNums += 1
      num = obj.clickNums
      obj.save()
      return JsonResponse({'clicknums':num}, status=200)
  except Exception as e:
        print(e)
        # return JsonResponse()
        return HttpResponse("error", status=400)

# 定义全局变量，存储最新的CVE List
cveList=[]


# 获取最新的CVE List，这里设定为最近的50条数据
# def getLatestCve(request):
#     try:
#         print("*****getLatestCve*****")
#         qs = CveInfo.objects.values()
#         # 将QuerySet对象转化为list类型
#         # 否则不能被转化为Json字符串
#         cvelist = list(qs)
#         latestcves=cvelist[-5:-1]
#
#         for cve in latestcves:
#             print('cve:',cve)
#             urls=DatabaseIndicator.objects.get(cveid=cve['cveid'])
#             print('urls:',urls)
#             print('cve type:', type(cve))
#             # cve['urls']=urls
#
#
#         # 为全局变量赋值
#         # global cveList
#         # # cveList = latestcves
#         # cveList.clear()
#         # for cve in latestcves:
#         #     cveList.append(cve)
#
#         return HttpResponse(json.dumps(latestcves), status=200)
#     except Exception as e:
#         print(e)
#         # return JsonResponse()
#         return HttpResponse("error", status=400)


# 返回菜单，传入CveInfo的list
def getMenu(cvelist):
    # try:
    print("*****getMenu*****")
    # qs = CveInfo.objects.values()
    # cvelist = list(qs)
    # latestcves = cvelist[-51:-1]

    # 为全局变量赋值
    # global cveList
    # cveList.clear()
    # for cve in latestcves:
    #     cveList.append(cve)

    newAnsData = []
    for i in cvelist:
        if isinstance(i, dict):
            newAnsData.append(i)
            continue
        # 将ansData中的每一个model object转化为JSON，然后删除其中不可序列化的字段
        i = object_to_json(i)
        del i['_state']
        if i.get('id') is not None:
            del i['id']
        newAnsData.append(i)

    # 生成菜单
    productMenu = []
    vulTypeMenu = []
    vulCompMenu = []
    rootMenu = []
    vectorMenu = []
    impactMenu = []
    cveMenu = []
    cweMenu = []
    capecMenu = []

    menuDict = {'product':{}, 'type':{},'component':{}, 'root':{},'vector':{}, 'impact':{},'cveid':{}, 'cwe':{},'capec':{}, 'severity':{},
                'access':{}, 'interaction':{},'auth':{}, 'attack_complex':{},'impact_confidence':{}, 'impact_integer':{},'impact_available':{}}
    for cve in newAnsData:  # 遍历latestcves数组，数组中的每一个元素为一个字典
        splitStr(cve['product'], productMenu)
        splitStr(cve['type'], vulTypeMenu)
        splitStr(cve['component'], vulCompMenu)
        splitStr(cve['root'], rootMenu)
        splitStr(cve['vector'], vectorMenu)
        splitStr(cve['impact'], impactMenu)
        splitStr(cve['cveid'], cveMenu)
        splitStr(cve['cwe'], cweMenu)
        splitStr(cve['capec'], capecMenu)

        # for one_ele in productMenu:
        #     if menuDict['product'].get(one_ele) is None:
        #         menuDict['product'][one_ele] = []
        #     menuDict['product'][one_ele].append(cve['cveid'])
        # for one_ele in vulTypeMenu:
        #     if menuDict['type'].get(one_ele) is None:
        #         menuDict['type'][one_ele] = []
        #     menuDict['type'][one_ele].append(cve['cveid'])
        # for one_ele in vulCompMenu:
        #     if menuDict['component'].get(one_ele) is None:
        #         menuDict['component'][one_ele] = []
        #     menuDict['component'][one_ele].append(cve['cveid'])
        # for one_ele in rootMenu:
        #     if menuDict['root'].get(one_ele) is None:
        #         menuDict['root'][one_ele] = []
        #     menuDict['root'][one_ele].append(cve['cveid'])
        # for one_ele in vectorMenu:
        #     if menuDict['vector'].get(one_ele) is None:
        #         menuDict['vector'][one_ele] = []
        #     menuDict['vector'][one_ele].append(cve['cveid'])
        # for one_ele in impactMenu:
        #     if menuDict['impact'].get(one_ele) is None:
        #         menuDict['impact'][one_ele] = []
        #     menuDict['impact'][one_ele].append(cve['cveid'])
        # for one_ele in cveMenu:
        #     if menuDict['cveid'].get(one_ele) is None:
        #         menuDict['cveid'][one_ele] = []
        #     menuDict['cveid'][one_ele].append(cve['cveid'])
        # for one_ele in cweMenu:
        #     if menuDict['cwe'].get(one_ele) is None:
        #         menuDict['cwe'][one_ele] = []
        #     menuDict['cwe'][one_ele].append(cve['cveid'])
        # for one_ele in capecMenu:
        #     if menuDict['capec'].get(one_ele) is None:
        #         menuDict['capec'][one_ele] = []
        #     menuDict['capec'][one_ele].append(cve['cveid'])
        #
        # for keys in ['severity', 'access', 'interaction', 'auth', 'attack_complex', 'impact_confidence', 'impact_integer', 'impact_available',]:
        #     menuDict[keys].append(cve['cveid'])

    # 去重
    productMenu = list(set(productMenu))
    vulTypeMenu = list(set(vulTypeMenu))
    vulCompMenu = list(set(vulCompMenu))
    rootMenu = list(set(rootMenu))
    vectorMenu = list(set(vectorMenu))
    impactMenu = list(set(impactMenu))
    cveMenu = list(set(cveMenu))
    cweMenu = list(set(cweMenu))
    capecMenu = list(set(capecMenu))

    # 排序
    productMenu.sort()
    vulTypeMenu.sort()
    vulCompMenu.sort()
    rootMenu.sort()
    vectorMenu.sort()
    impactMenu.sort()
    cveMenu.sort()
    cweMenu.sort()
    capecMenu.sort()

    # 当菜单以选择框的形式出现时，需要进行下列处理
    productMenu=list2diclist(productMenu)
    vulTypeMenu = list2diclist(vulTypeMenu)
    vulCompMenu = list2diclist(vulCompMenu)
    rootMenu = list2diclist(rootMenu)
    vectorMenu = list2diclist(vectorMenu)
    impactMenu = list2diclist(impactMenu)
    cveMenu = list2diclist(cveMenu)
    cweMenu = list2diclist(cweMenu)
    capecMenu = list2diclist(capecMenu)

    # 构造json返回内容
    menu_info = {}
    data = json.loads(json.dumps(menu_info))

    data['productMenu'] = productMenu
    data['vulTypeMenu'] = vulTypeMenu
    data['vulCompMenu'] = vulCompMenu
    data['rootMenu'] = rootMenu
    data['vectorMenu'] = vectorMenu
    data['impactMenu'] = impactMenu
    data['cveMenu'] = cveMenu
    data['cweMenu'] = cweMenu
    data['capecMenu'] = capecMenu
    data['menuDict'] = menuDict

    # ret = json.dumps(data, ensure_ascii=False)

    # print('data menu为：',data)
    return data

    #     return HttpResponse(ret, status=200)
    # except Exception as e:
    #     print(e)

# 将单纯的数组，e.g.[a,b,c...]变成[{value:a,label:a},{value:b,label:b}...]
def list2diclist(list):
    ret=[]
    for i in list:
        ret.append({'value': i,'label': i})
    return ret

# 字符串切割,将字符串按照 ; 分割，返回一个数组
def splitStr2List(str) :
        splchar = ';'
        tmpList = []
        retList = []
        if str:
          if str.find(splchar) == -1:   #字符串不存在分隔符且字符串不为空
            return str
          else:
            tmpList = str.split(splchar)
            for i in tmpList:
              retList.append(i)

        return retList

# 将字符串按照;分割，并生成menu list，此时的menu list还没有经过去重和排序，因为需要遍历完全部的latestcves
# 获取完所有latest cves的aspects后，再去重和排序
def splitStr(str, metaList):
    if(str):
        if str.find(';')==-1: # 当字符串存在且没有分隔符
            metaList.append(str)
        else:
            tmpList=str.split(';')
            for tmp in tmpList:
                if tmp not in metaList:#去重
                    metaList.append(tmp)

# 根据关键词进行搜索
def searchKey(request):
    try:
        print("*****searchKey*****")
        assert request.method=='POST'
        # 取到搜索关键字key
        key=request.POST.get("key")
        print("搜索key:", key)
        if key == None:
            return HttpResponse("后端获取到的key为空")
        else:
            # 假设/测试情况
            # ans=CveInfo.objects.get(cveid=key)
            # print('ans类型',type(ans))
            # # 定义ansData，存储object.get()后的JSON数据
            # ansData={}
            # ansData=object_to_json(ans)
            # # 删除以下字段，否则将无法进行JSON序列化
            # del ansData['_state']
            # del ansData['id']
            # print('***ansData为***：', ansData)
            # return HttpResponse(json.dumps(ansData),status=200)

            # 真实搜索状况，不指定是cveid还是desc等
            # filter多条件查询
            # ans=CveInfo.objects.filter(Q(cveid__icontains=key) | Q(product__icontains=key) | Q(type__icontains=key) | Q(title__icontains=key) | Q(component__icontains=key))
            ans = CveInfo.objects.filter(
                Q(cveid__icontains=key) | Q(product__icontains=key) | Q(type__icontains=key) | Q(
                    title__icontains=key) | Q(component__icontains=key))
            # print('ans结果：', ans)
            if ans:
                ansData=list(ans)

                menu=getMenu(ansData)

                # 定义一个新的List以存放处理后的CVE List
                newAnsData=[]
                for i in ansData:
                    # 将ansData中的每一个model object转化为JSON，然后删除其中不可序列化的字段
                    i=object_to_json(i)
                    del i['_state']
                    del i['id']
                    urlsObj = DatabaseIndicator.objects.get(cveid=i['cveid'])
                    urls = object_to_json(urlsObj)
                    del urls['_state']
                    del urls['id']
                    i['urls']=urls
                    newAnsData.append(i)

                # 构造json返回内容
                tmp = {}
                data = json.loads(json.dumps(tmp))
                data['searchcves'] = newAnsData
                data['menu'] = menu
                ret = json.dumps(data, ensure_ascii=False)

                return HttpResponse(ret, status=200)
                # return HttpResponse(json.dumps(newAnsData), status=200)
            else:
                return HttpResponse("暂未找到匹配的数据")
    except Exception as e:
        print(e)
        return HttpResponse("error", status=400)


# 根据关键词搜索 version2
def searchByStr(request):
    try:
        print("*****searchByStr*****")
        assert request.method == 'POST'
        # 取到搜索关键字key
        # searchStr = request.POST.get("searchStr")
        searchStr='php, buffer overflow'
        searchStrBackup=searchStr
        print("搜索Str:", searchStr)
        if searchStr == None:
            return HttpResponse("后端获取到的searchStr为空")
        else:
            # 第一步：筛选出candidates，根据优先级
            # 优先级：product name>vul component>vul type>impact>vector>root>version

            if searchStr.find(',')!=-1:  # 字符串中由,切割开，说明搜索条件有多个
                typelist=[]
                searchStr=searchStr.replace(", ", ",")  # 避免词组开头的空格符号对数据库匹配造成影响
                strlist=searchStr.split(',')
                strlistBackup=strlist
                # 1、从home Aspect2Table中找出每个词组的aspect类型
                for str in strlist:
                    # tmp=Aspect2Table.objects.get(aspect=str)  # 因为aspect=str的有多条记录，因此不能用get方法，否则会报错
                    tmp0=Aspect2Table.objects.filter(aspect=str)  # 精准搜索，得到一个qs集合
                    tmp0=list(tmp0)
                    strType = ''  # 找出该词组所有的type，取优先级最高的为确定type
                    for t in tmp0:
                        strType=strType+t.aspect_id
                    if strType.find('product')!=-1:
                        typelist.append({'type': 'product', 'str': str, 'id': '1'})
                    elif strType.find('vulcomp')!=-1:
                        typelist.append({'type': 'component', 'str': str, 'id': '2'})
                    elif strType.find('vultype')!=-1:
                        typelist.append({'type': 'type', 'str': str, 'id': '3'})
                    elif strType.find('impact')!=-1:
                        typelist.append({'type': 'impact', 'str': str, 'id': '4'})
                    elif strType.find('vector')!=-1:
                        typelist.append({'type': 'vector', 'str': str, 'id': '5'})
                    elif strType.find('root')!=-1:
                        typelist.append({'type': 'root', 'str': str, 'id': '6'})
                    else:
                        print('搜索的词组为其他类型')
                # 2、将typelist按照type的优先级排序，优先级为product name>vul component>vul type>impact>vector>root>version
                typelist.sort(key=lambda obj:(obj.get('id')), reverse=False)  # 按照升序排列，默认升序
                priority=[]  # 存放了按照优先级排序的关键词
                # 将关键词按照优先级排序
                for i in typelist:
                    priority.append(i['str'])
                # print('typelist：', typelist)
                # 3、根据优先级筛选出candidates
                cvesOfEachType=[]
                # 创建对象，把优先级最高的type对应的cve找出来，剩下的全扔掉
                # qs0=Phrase2Cve.objects.values()
                for item in typelist:
                    cves=[]
                    phrase=item['str']
                    qs=Phrase2Cve.objects.filter(word=phrase)
                    # qs0=qs0.filter(word=phrase)
                    qs=list(qs)
                    for q in qs:
                        cves.append(q.type)
                    cves=set(cves)
                    for cve in cves:
                        cvesOfEachType.append({'cve': cve, 'score': 0})
                    # item['cves']=cves
                    break  # 只按照优先级最高的进行一次过滤


                # 第二步：打分，分高的在前面
                # 1、单词打分：提取出搜索字符串中的单词，strlist中为切分的词组
                print('*****单词打分*****')
                # firstStr=typelist[0]['str'] # 因为根据firstStr过滤得到的cve中肯定含有firstStr，因此在单词打分和词组打分时先删掉此条件
                # strlistBackup.remove(firstStr)
                typelist0 = list(typelist)
                typelist0.pop(0)
                wordlist=[]
                priority0=list(priority)
                priority0.pop(0)  # 改变原有列表
                for i in priority0:
                    if i.find(' ')==-1:
                        wordlist.append(i)
                    else:
                        tmp=i.split(' ')
                        for j in tmp:
                            wordlist.append(j)
                print('wordlist', wordlist)
                # test=CveInfo.objects.filter(product__icontains='php').filter(type__icontains='buffer')
                # print('test', test)
                for cve in cvesOfEachType[5:10]:
                    cveid=cve['cve']
                    # print('cveid:', cveid)
                    q0=CveInfo.objects.filter(cveid=cveid)
                    for word in wordlist:  # get()时，当记录不存在会报错，使用filter时，当记录不存在返回[]
                        q=q0.filter(Q(product__icontains=word) | Q(type__icontains=word) | Q(component__icontains=word)| Q(root__icontains=word) | Q(vector__icontains=word)| Q(impact__icontains=word) | Q(version__icontains=word))
                        # print('q:',q)
                        if q:
                            cve['score']=cve['score']+1
                        else:
                            pass
                            # print('单词不加分')
                    print('cvesOfEachType cve：', cve)

                # 2、词组打分
                print('\n*****词组打分*****')
                # print('typelist:',typelist)
                for cve in cvesOfEachType[5:10]:
                    cveid = cve['cve']
                    # print('cveid:', cveid)
                    q0 = CveInfo.objects.filter(cveid=cveid)
                    for i in typelist0:
                        # print('i:', i)
                        # q = q0.filter(
                        #     Q(product__icontains=word) | Q(type__icontains=word) | Q(component__icontains=word) | Q(
                        #         root__icontains=word) | Q(vector__icontains=word) | Q(impact__icontains=word) | Q(
                        #         version__icontains=word))
                        type=i['type']
                        str=i['str']
                        if type=='product':
                            q= q0.filter(product__icontains=str)
                        elif type=='vulcomp':
                            q= q0.filter(component__icontains=str)
                        elif type=='type':
                            q = q0.filter(type__icontains=str)
                        elif type=='impact':
                            q= q0.filter(impact__icontains=str)
                        elif type=='vector':
                            q = q0.filter(vector__icontains=str)
                        elif type=='root':
                            q= q0.filter(root__icontains=str)
                        else:
                            # print('词组不加分')
                            pass
                        # print('q:', q)
                        if q:
                            cve['score'] = cve['score'] + 1
                    print('cvesOfEachType cve：', cve)

                # 3、同义词打分
                print('\n*****同义词打分*****')
                thesauruslist=[]
                for words in priority0:
                    print('words:',words)
                    # 在WordThesaurus表中查找其同义词
                    qs=WordThesaurus.objects.filter(thesaurus=words)
                    # print('qs:',qs)
                    if qs:  # 存在同义词
                        thesaurus = []  # 存储该词所有的近义词
                        allType=[]  # 该词的类型可能不只一种，取优先级最高的，否则数量会过大
                        realtype=''  # 该词优先级最高的type
                        keyType=''  # 用于检索的type，如type:0
                        for one in typelist:
                            if one['str']==words:
                                realtype=one['type']  # 该词优先级最高的type
                                print('realtype:',realtype)
                        qs = list(qs)
                        for q in qs:  # 一个词可能存在多种类型
                            t=q.type
                            if t.find(realtype)!=-1:
                                keyType=t
                                break
                            else:
                                continue
                        print('keyType:',keyType)
                        qqs = WordThesaurus.objects.filter(type=keyType)
                        qqs=list(qqs)
                        for qq in qqs:
                            thesaurus.append(qq.thesaurus)
                        print('thesaurus length:', len(thesaurus))
                        thesaurus.remove(words)
                        print('thesaurus length 1:', len(thesaurus))
                        thesaurus=list(set(thesaurus))
                        thesauruslist.append({'words': words, 'thesaurus': thesaurus, 'type':realtype})
                    else:
                        pass
                if thesauruslist:  # 当同义词存在才会进行第三次打分
                    for cve in cvesOfEachType[5:10]:
                        cveid = cve['cve']
                        q0 = CveInfo.objects.filter(cveid=cveid)
                        for one in thesauruslist:
                            thesaurus=one['thesaurus']  # 同义词列表，已经去除同义词本身
                            type=one['type']
                            for i in thesaurus:
                                if type=='type':
                                    q=q0.filter(type__icontains=i)
                                elif type=='impact':
                                    q = q0.filter(impact__icontains=i)
                                elif type=='root':
                                    q = q0.filter(root__icontains=i)
                                else:
                                    pass
                                # print('q:', q)
                                if q:
                                    cve['score'] = cve['score'] + 1
                                else:
                                    # print('同义词不加分')
                                    pass
                        print('cvesOfEachType cve：', cve)


                # 2.2、将cvesOfEachType按照score的高低排序，按照降序排列，分数高的在前
                cvesOfEachType.sort(key=lambda obj: (obj.get('score')), reverse=False)

                for i in cvesOfEachType[0:10]:
                    print(i)

            # else:  # 只有一个搜索条件，模糊搜索
            #     ans = CveInfo.objects.filter(
            #         Q(cveid__icontains=searchStr) | Q(product__icontains=searchStr) | Q(type__icontains=searchStr) | Q(
            #             title__icontains=searchStr) | Q(component__icontains=searchStr))
            # if ans:
            #     ansData=list(ans)
            #
            #     menu=getMenu(ansData)
            #
            #     # 定义一个新的List以存放处理后的CVE List
            #     newAnsData=[]
            #     for i in ansData:
            #         # 将ansData中的每一个model object转化为JSON，然后删除其中不可序列化的字段
            #         i=object_to_json(i)
            #         del i['_state']
            #         del i['id']
            #         urlsObj = DatabaseIndicator.objects.get(cveid=i['cveid'])
            #         urls = object_to_json(urlsObj)
            #         del urls['_state']
            #         del urls['id']
            #         i['urls']=urls
            #         newAnsData.append(i)
            #
            #     # 构造json返回内容
            #     tmp = {}
            #     data = json.loads(json.dumps(tmp))
            #     data['searchcves'] = newAnsData
            #     data['menu'] = menu
            #     ret = json.dumps(data, ensure_ascii=False)
            #
            return HttpResponse('测试', status=200)
            # else:
            #     return HttpResponse("暂未找到匹配的数据")
    except Exception as e:
        print('search2 error',e)
        return HttpResponse("search2 error", status=400)


def searchByStr3(request):
    try:
        print("*****searchByStr3*****")
        print(time.time())
        assert request.method == 'POST'
        searchStr = request.POST.get("key")

        print("searching Str:", searchStr)
        if searchStr == None:
            return HttpResponse("后端获取到的searchStr为空")

        tp = TextPreprocess()
        phraseslist = [tp.clean_so_data_nopos(one_word.strip()) for one_word in searchStr.split(',') if
                       len(one_word) > 0]

        wordslist = []
        for one_phrase in phraseslist:
            wordslist += one_phrase.split()
        wordslist = set([one_word for one_word in wordslist if len(one_word) > 0])
        phraseslist = set([one_phrase for one_phrase in phraseslist if len(one_phrase.split()) > 1])

        priority = ['name', 'component', 'type', 'impact', 'vector', 'root']
        type_dict = {one_ele: set() for one_ele in priority}
        for one_word in wordslist:
            if new_type.get(one_word) is None:
                continue
            word_types = new_type[one_word]
            for one_type in word_types:
                type_dict[one_type].add(one_word)

        candidate_words = set()
        for one_priority in priority:
            if len(type_dict[one_priority]) > 0:
                candidate_words = type_dict[one_priority]
                break

        candidate_cves = set()
        for one_word in candidate_words:
            if new_w2cve.get(one_word) is None:
                continue
            candidate_cves = candidate_cves.union(set(new_w2cve[one_word]))

        cve_scores = {}
        for one_cve in tqdm.tqdm(candidate_cves):
            cve_scores[one_cve] = 0
            cve_words = set()

            if not new_cve2w.get(one_cve) is None:
                cve_words = set(new_cve2w[one_cve])

            cve_phrases = set()
            if not new_phrase.get(one_cve) is None:
                cve_phrases = set(new_phrase[one_cve])

            thesaurus = set()
            for one_word in wordslist:
                if new_th2type.get(one_word) is None:
                    continue
                thesaurus = thesaurus.union(set(new_th2type[one_word]))

            thesaurus_words = set()
            for one_thesa in thesaurus:
                if new_type2th.get(one_thesa) is None or one_thesa in ['impact:3', 'root:1', 'impact:4', 'impact:6']:
                    continue
                thesaurus_words = thesaurus_words.union(set(new_type2th[one_thesa]))

            for one_word in wordslist:
                if one_word in cve_words:
                    cve_scores[one_cve] += 1

            for one_phrase in phraseslist:
                if one_phrase in cve_phrases:
                    cve_scores[one_cve] += 1
                elif one_phrase in thesaurus_words:
                    cve_scores[one_cve] += 1
        cve_scores = sorted(cve_scores.items(), key=lambda x: x[1], reverse=True)[:999]
        all_cveid = [one_ele[0] for one_ele in cve_scores]
        finalCveList = []
        if len(all_cveid) > 0:
            finalCveList = CveInfoPlus.objects.filter(cveid__in=all_cveid)
            urlsObjs = DatabaseIndicator.objects.filter(cveid__in=all_cveid)
            urlsObjs = list(urlsObjs)

        # print("finalCveList:", finalCveList)
        # 根据cveid在CveInfo表格中查找对应的cve
        newAnsData = []  # 定义一个新的List以存放处理后的CVE List
        menuAns = []  # 用于getMenu传参
        for idx, i in enumerate(finalCveList):
            menuAns.append(i)
            # 将ansData中的每一个model object转化为JSON，然后删除其中不可序列化的字段
            i = object_to_json(i)
            del i['_state']
            # urlsObj = DatabaseIndicator.objects.get(cveid=i['cveid'])
            urlsObj = urlsObjs[idx]
            urls = object_to_json(urlsObj)
            del urls['_state']
            i['urls'] = urls
            # clean_aspects(i)
            newAnsData.append(i)
        print(time.time())
        menu = getMenu(menuAns)
        # searchQS = newAnsData
        # 构造json返回内容
        tmp = {}
        data = json.loads(json.dumps(tmp))
        data['searchcves'] = newAnsData
        data['menu'] = menu
        ret = json.dumps(data, ensure_ascii=False)

        return HttpResponse(ret, status=200)
    except Exception as e:
        print('search2 error',e)
        return HttpResponse("searchByStr2 error", status=400)

def clean_aspects(i):
    for one_aspect in ['product']:
        if i.get(one_aspect) is not None:
            aspect_list = i[one_aspect].split(';')
            clean_list = ['('.join(one_ele.strip().split('(')[:-1]) if '(' in one_ele else one_ele.strip() for one_ele in aspect_list]
            postfix_list = ['('+one_ele.strip().split('(')[-1] if '(' in one_ele else '' for one_ele in aspect_list]
            clean_list = [reverse_stem_map[one_ele] if reverse_stem_map.get(one_ele) is not None else one_ele for one_ele in clean_list]
            clean_list = [clean_list[i] + postfix_list[i] for i in range(len(clean_list))]
            i[one_aspect] = ';'.join(clean_list)

# 根据关键词搜索 version3 修改后版本
def searchByStr2(request):
    try:
        print("*****searchByStr2*****")
        assert request.method == 'POST'
        # 取到搜索关键字key
        searchStr = request.POST.get("key")
        # searchStr='unam'
        searchStrBackup=searchStr
        print("搜索Str:", searchStr)
        if searchStr == None:
            return HttpResponse("后端获取到的searchStr为空")
        else:
            # 第一步：筛选出candidates，根据优先级
            # 优先级：product name>vul component>vul type>impact>vector>root>version
            finalCveList=[]   # 最后将要展示在前端的CVE的CVEID的集合
            ansSet = []     # 当搜索关键词直接是CVE编号时，AnsSet直接存储对应的qs

            if searchStr.find(',')!=-1:  # 字符串中由,切割开，说明搜索条件有多个
                typelist=[]
                cveslist=[]  # cve结果集交集，用作加分的依据
                cveslistByWord=[]  # 根据优先级最高的word初步筛选cves
                cveslistByWordNext=[]  # 根据剩余的words筛选cves
                cveslistByWords=[]  # 根据词组words筛选cves
                cveAndScore = []  # 每个cve及其对应的分数

                searchStrBackup = searchStrBackup.replace(", ", ",")  # 避免词组开头的空格符号对数据库匹配造成影响
                wordslist = searchStrBackup.split(',')  # 存储词组
                wordslistCopy = list(wordslist)
                # print('wordslist：', wordslist)

                searchStr1=searchStr
                searchStr1=searchStr1.replace(", ", ",")
                searchStr1 = searchStr1.replace(" ", ",")
                wordlist=searchStr1.split(",")  # 存储单词
                wordlistCopy=[]  # 删除优先级最高的单词
                print('wordlist：', wordlist)

                # 1、从home WordType2中找出每个单词的aspect类型，然后对其按照优先级
                for word in wordlist:
                    tmp0=WordType2.objects.filter(word=word)  # 精准搜索，得到一个qs集合
                    tmp0=list(tmp0)
                    strType = ''  # 找出该词组所有的type，取优先级最高的为确定type
                    for t in tmp0:
                        strType=strType+t.type
                    if strType.find('name')!=-1:
                        typelist.append({'type': 'name', 'word': word, 'id': '1'})
                    elif strType.find('component')!=-1:
                        typelist.append({'type': 'component', 'word': word, 'id': '2'})
                    elif strType.find('type')!=-1:
                        typelist.append({'type': 'type', 'word': word, 'id': '3'})
                    elif strType.find('impact')!=-1:
                        typelist.append({'type': 'impact', 'word': word, 'id': '4'})
                    elif strType.find('vector')!=-1:
                        typelist.append({'type': 'vector', 'word': word, 'id': '5'})
                    elif strType.find('root')!=-1:
                        typelist.append({'type': 'root', 'word': word, 'id': '6'})
                    else:
                        print('word:', word)
                        print('未在WordType2数据表中找到单词的类型！')
                # 2、将typelist按照type的优先级排序，优先级为product name>vul component>vul type>impact>vector>root>version
                typelist.sort(key=lambda obj:(obj.get('id')), reverse=False)  # 按照升序排列，默认升序
                priority=[]  # 存放了按照优先级排序的关键words
                ifOneType=[]  # 优先级最高的word存在多个，如果word的优先级相同，则最后的cvelist应该是各个word对应cvelist的并集
                firstType=typelist[0]['type']  # 优先级最高的aspect
                for i in typelist:
                    wordlistCopy.append(i['word'])
                    if i['type']==firstType:
                        ifOneType.append(i['word'])
                        wordlistCopy.pop(0)  # 删除优先级最高的单词
                    priority.append(i['word'])   # 将关键词按照优先级排序
                # print('typelist：', typelist)
                # print('wordlistCopy：', wordlistCopy)
                # print('ifOneType：', ifOneType)
                # print('priority：', priority)

                # 3、根据优先级筛选出candidates
                # 根据wordlist中的单词筛选cve
                for word in ifOneType:
                    # print('word为'+word)
                    ansByWord = Word2Cve.objects.filter(word=word)  # 根据优先级最高的word在Word2Cve中查找对应的cve
                    ansByWord = list(ansByWord)
                    # print('ansByWord[0]：', ansByWord[0].type)
                    for i in ansByWord:
                        cveslistByWord.append(i.type)  # 将对应的cve添加到cvelistByWord中
                        cveAndScore.append({'cve': i.type, 'score': 0})
                    # print('len cveslistByWord：', len(cveslistByWord))

                print('len cveslistByWord：', len(cveslistByWord))


                # 第二步：打分，分高的在前面
                # 1、单词打分：提取出搜索字符串中的单词，strlist中为切分的词组
                print('*****单词打分*****')
                for word in wordlistCopy:
                    ansByWord = Word2Cve.objects.filter(word=word)  # 根据次优先级的word在Word2Cve中查找对应的cve
                    ansByWord = list(ansByWord)
                    # print('len ansByWord：', len(ansByWord))
                    for i in ansByWord:
                        cveslistByWordNext.append(i.type)  # 将对应的cve添加到cvelistByWordNext中
                # 求两个搜索结果集的交集
                cveslist=list(set(cveslistByWord) & set(cveslistByWordNext))
                print('len cveslist：', len(cveslist))
                for one in cveAndScore:
                    if one['cve'] in cveslist:
                        one['score']=one['score']+1
                # Debug
                cveAndScore.sort(key=lambda obj: (obj.get('score')), reverse=True)  # 按照升序排列，默认升序
                print('cveAndScore:', cveAndScore[0:5])

                # # 2、词组打分
                print('*****词组打分*****')
                for words in wordslist:
                    ansByWords = Phrase2Cve.objects.filter(word=words)  # 根据次优先级的word在Phrase2Cve中查找对应的cve
                    ansByWords = list(ansByWords)
                    # print('len ansByWord：', len(ansByWord))
                    for i in ansByWords:
                        cveslistByWords.append(i.type)  # 将对应的cve添加到cvelistByWordNext中
                    # 求两个搜索结果集的交集
                cveslist = list(set(cveslistByWord) & set(cveslistByWords))
                print('len cveslist：', len(cveslist))
                for one in cveAndScore:
                    if one['cve'] in cveslist:
                        one['score'] = one['score'] + 1

                # # 3、同义词打分
                # print('\n*****同义词打分*****')
                # thesauruslist=[]  # 所有word的所有同义词
                # for word in wordlist:
                #     print('word:',word)
                #     # 在WordThesaurus表中查找其同义词
                #     qs=WordThesaurus.objects.filter(thesaurus=word)
                #     # print('qs:',qs)
                #     if qs:  # 存在同义词
                #         thesaurus = []  # 存储该词所有的近义词
                #         cvesByThesaurus=[]  # 存储该词所有的近义词对应的cve
                #         allType=[]  # 该词的类型可能不只一种
                #         qs = list(qs)
                #         for q in qs:  # 一个词可能存在多种类型
                #            allType.append(q.type)
                #         for type in allType:
                #             qqs = WordThesaurus.objects.filter(type=type)
                #             qqs=list(qqs)
                #             for qq in qqs:
                #                 thesaurus.append(qq.thesaurus)
                #         print("thesaurus len:",len(thesaurus))
                #         # 查找该词所有同义词所对应的cve
                #         for words in thesaurus:
                #             ansByWords = Phrase2Cve.objects.filter(word=words)  # 根据同义词在Phrase2Cve中查找对应的cve
                #             ansByWords = list(ansByWords)
                #             for i in ansByWords:
                #                 cvesByThesaurus.append(i.type)  # 将对应的cve添加到cvesByThesaurus中
                #             # 求两个搜索结果集的交集
                #         cveslist = list(set(cveslistByWord) & set(cvesByThesaurus))
                #         print('len cveslist：', len(cveslist))
                #         for one in cveAndScore:
                #             if one['cve'] in cveslist:
                #                 one['score'] = one['score'] + 1
                #     else:
                #         pass

                # # 2.2、将cvesOfEachType按照score的高低排序，按照降序排列，分数高的在前
                print('\n*****排序*****')
                cveAndScore.sort(key=lambda obj: (obj.get('score')), reverse=True)
                for i in cveAndScore[0:99]:
                    finalCveList.append(i['cve'])

            else:  # 只有一个搜索条件
                # print("*****只有一个搜索条件*****")
                # 当搜索条件是CVE编号or正常搜索关键词时，是不同的，因为可以直接根据编号进行cveid的filter
                if searchStr.find('CVE-')!=-1:
                    ansSet = CveInfoPlus.objects.filter(cveid__icontains=searchStr)
                    global searchQS
                    searchQS=ansSet
                    print("searchQS:",searchQS)
                else:
                    wordlist=[]  # 存储搜索条件
                    if searchStr.find(' ') !=-1:
                        wordlist=searchStr.split(' ')
                    else:
                        wordlist.append(searchStr)
                    print("wordlist:",wordlist)
                    alllist = []
                    for word in wordlist:
                        # print('word为'+word)
                        tmplist = []
                        ansByWord = Word2Cve.objects.filter(word=word)  # 根据优先级最高的word在Word2Cve中查找对应的cve
                        if ansByWord:
                            ansByWord = list(ansByWord)
                            # print('ansByWord[0]：', ansByWord[0].type)
                            for i in ansByWord:
                                # tmplist.append(i.type)
                                finalCveList.append(i)
                        # alllist.append(tmplist)
                    # print("alllist:", alllist)
                    # for list in alllist:
                    #     if list:
                    #         finalCveList=list
                    #         break
                    # for list in alllist:
                    #     if list:
                    #         finalCveList = list(set(list) & set(finalCveList))



            print("finalCveList:",finalCveList)
            # 根据cveid在CveInfo表格中查找对应的cve
            newAnsData = []   # 定义一个新的List以存放处理后的CVE List
            menu=[]
            if finalCveList:
                menuAns = []  # 用于getMenu传参
                searchQSChild=[]  # 用于将list转化为querySet，数组里面的每一个元素都是一个CveInfo对象
                for cve in finalCveList[0:99]:
                    cve = cve.type
                    ans=CveInfoPlus.objects.filter(cveid=cve)
                    if ans:
                        ansData=list(ans)
                        for i in ansData:
                            menuAns.append(i)
                            # 将ansData中的每一个model object转化为JSON，然后删除其中不可序列化的字段
                            i=object_to_json(i)
                            del i['_state']
                            del i['id']
                            urlsObj = DatabaseIndicator.objects.get(cveid=cve)
                            urls = object_to_json(urlsObj)
                            del urls['_state']
                            del urls['id']
                            i['urls']=urls
                            newAnsData.append(i)
                searchQSChild=menuAns
                menu = getMenu(menuAns)
                # 将list转化为CveInfo对象
                childs=CveInfoPlus.objects.filter(cveid__in=[x.cveid for x in searchQSChild])
                # print("childs:",childs)
                searchQS=childs
            elif ansSet:  # 搜索关键词直接带有CVE编号
                ansData = list(ansSet)
                menu=getMenu(ansData)
                for i in ansData:
                    # 将ansData中的每一个model object转化为JSON，然后删除其中不可序列化的字段
                    i = object_to_json(i)
                    del i['_state']
                    del i['id']
                    urlsObj = DatabaseIndicator.objects.get(cveid=i['cveid'])
                    urls = object_to_json(urlsObj)
                    del urls['_state']
                    del urls['id']
                    i['urls'] = urls
                    newAnsData.append(i)

            # 构造json返回内容
            tmp = {}
            data = json.loads(json.dumps(tmp))
            data['searchcves'] = newAnsData
            data['menu'] = menu
            ret = json.dumps(data, ensure_ascii=False)

            return HttpResponse(ret, status=200)

    except Exception as e:
        print('search2 error',e)
        return HttpResponse("searchByStr2 error", status=400)


def getNewCve2(request):
    try:
        print("*****getNewCve2*****")
        assert request.method == 'POST'
        allCveIds = request.POST.get('allcveids').split(';')
        productname = request.POST.get('productname').split(';')
        vulcomponent = request.POST.get('vulcomponent').split(';')
        vultype = request.POST.get('vultype').split(';')
        impact = request.POST.get('impact').split(';')
        vector = request.POST.get('vector').split(';')
        root = request.POST.get('root').split(';')

        # multi select
        score1 = request.POST.get('score1')
        if (score1):
            score11 = float(score1)
        else:
            score11 = 0.0
        score2 = request.POST.get('score2')
        if (score2):
            score22 = float(score2)
        else:
            score22 = 10.0
        severity = request.POST.get('severity')
        access = request.POST.get('access')
        interaction = request.POST.get('interaction')
        authentication = request.POST.get('authentication')
        attackComplex = request.POST.get('attackComplex')
        confidentiality = request.POST.get('confidentiality')
        integrity = request.POST.get('integrity')
        avaliability = request.POST.get('avaliability')

        test = CveInfoPlus.objects.filter(cveid__in=allCveIds)  # 创建CveInfo对象

    except Exception as e:
        print(e)
        return HttpResponse("error", status=400)

# 根据条件过滤CVE
def getNewCve(request):
    try:
        print("*****getNewCve*****")
        assert request.method=='POST'
        # 取到搜索关键字
        # aspects select
        allCveIds = request.POST.get('allcveids').split(';')
        productname = request.POST.get('productname').split(';')
        vulcomponent = request.POST.get('vulcomponent').split(';')
        vultype = request.POST.get('vultype').split(';')
        impact = request.POST.get('impact').split(';')
        vector = request.POST.get('vector').split(';')
        root = request.POST.get('root').split(';')

        while '' in allCveIds:
            allCveIds.remove('')
        while '' in productname:
            productname.remove('')
        while '' in vulcomponent:
            vulcomponent.remove('')
        while '' in vultype:
            vultype.remove('')
        while '' in impact:
            impact.remove('')
        while '' in vector:
            vector.remove('')
        while '' in root:
            root.remove('')
        # multi select
        score1=request.POST.get('score1')
        if(score1):
            score11 = float(score1)
        else:
            score11=0.0
        score2 = request.POST.get('score2')
        if(score2):
            score22 = float(score2)
        else:
            score22=10.0
        severity=request.POST.get('severity')
        access=request.POST.get('access')
        interaction=request.POST.get('interaction')
        authentication=request.POST.get('authentication')
        attackComplex=request.POST.get('attackComplex')
        confidentiality=request.POST.get('confidentiality')
        integrity=request.POST.get('integrity')
        avaliability=request.POST.get('avaliability')

        # filter多条件查询
        # ans=CveInfo.objects.filter(Q(severity__icontains=access) & Q(access__icontains=access) & Q(interaction__icontains=interaction) & Q(auth__icontains=authentication) & Q(attack_complex__icontains=attackComplex) & Q(impact_confidence__icontains=confidentiality) & Q(impact_integer__icontains=integrity) & Q(impact_available__icontains=avaliability))
        nothing=0 #select menu查询是否为空
        ans=[]
        # ret=CveInfoPlus.objects.filter(cveid__in=allCveIds) # 创建CveInfo对象
        test=CveInfoPlus.objects.filter(cveid__in=allCveIds) # 创建CveInfo对象
        # global searchQS
        # if searchQS:
        #     test=searchQS
        # print("searchQS2:", searchQS)
        # 优先级1：product name，根据优先级1筛选cve
        if(len(productname)>0):
            print('productname',productname)
            ans1=test.filter(reduce(operator.or_, (Q(product__contains=one_ele) for one_ele in productname)))
            # ans1 = test.filter(product__in=productname)
            # print('ans1:',ans1)
            # print('vulcomponent:', vulcomponent)
            # ans1=list[ans1]
            if(len(vulcomponent)>0):
                # ans2=CveInfo.objects.filter(Q(product__contains=productname)&Q(component__contains=vulcomponent))
                ans2=ans1.filter(reduce(operator.or_, (Q(component__contains=one_ele) for one_ele in vulcomponent)))
                # ans2 = ans1.filter(component__in=vulcomponent)
                print('ans2', ans2)
                if(len(vultype)>0):
                    ans3=ans2.filter(reduce(operator.or_, (Q(type__contains=one_ele) for one_ele in vultype)))
                    # ans3 = ans2.filter(type__in=vultype)
                    if(len(impact)>0):
                        ans4=ans3.filter(reduce(operator.or_, (Q(impact__contains=one_ele) for one_ele in impact)))
                        # ans4 = ans3.filter(impact__in=impact)
                        if(len(vector)>0):
                            ans5=ans4.filter(reduce(operator.or_, (Q(vector__contains=one_ele) for one_ele in vector)))
                            # ans5 = ans4.filter(vector__in=vector)
                            if(len(root)>0):
                                ans6=ans5.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                                # ans6 = ans5.filter(root__in=root)
                                ret=ans6
                            else:
                                ret=ans5
                        elif(len(root)>0):
                            ans6 = ans4.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                            # ans6 = ans4.filter(root__in=root)
                            ret=ans6
                        else:
                            ret=ans4
                    elif(len(vector)>0):
                        ans5 = ans3.filter(reduce(operator.or_, (Q(vector__contains=one_ele) for one_ele in vector)))
                        # ans5 = ans3.filter(vector__in=vector)
                        if (len(root)>0):
                            ans6 = ans5.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                            # ans6 = ans5.filter(root__in=root)
                            ret = ans6
                        else:
                            ret=ans5
                    elif(len(root)>0):
                        ans6 = ans3.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                        # ans6 = ans3.filter(root__in=root)
                        ret = ans6
                    else:
                        ret = ans3
                elif(len(impact)>0):
                    ans4 = ans2.filter(reduce(operator.or_, (Q(impact__contains=one_ele) for one_ele in impact)))
                    # ans4 = ans2.filter(impact__in=impact)
                    if (len(vector)>0):
                        ans5 = ans4.filter(reduce(operator.or_, (Q(vector__contains=one_ele) for one_ele in vector)))
                        # ans5 = ans4.filter(vector__in=vector)
                        if (len(root)>0):
                            ans6 = ans5.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                            # ans6 = ans5.filter(root__in=root)
                            ret=ans6
                        else:
                            ret=ans5
                    elif (len(root)>0):
                        ans6 = ans4.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                        # ans6 = ans4.filter(root__in=root)
                        ret = ans6
                    else:
                        ret=ans4
                elif(len(vector)>0):
                    ans5 = ans2.filter(reduce(operator.or_, (Q(vector__contains=one_ele) for one_ele in vector)))
                    # ans5 = ans2.filter(vector__in=vector)
                    if (len(root)>0):
                        ans6 = ans5.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                        # ans6 = ans5.filter(root__in=root)
                        ret = ans6
                    else:
                        ret = ans5
                elif(len(root)>0):
                    ans6 = ans2.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                    # ans6 = ans2.filter(root__in=root)
                    ret = ans6
                else:
                    ret=ans2
            elif(len(vultype)>0):
                ans3 = ans1.filter(reduce(operator.or_, (Q(type__contains=one_ele) for one_ele in vultype)))
                # ans3 = ans1.filter(type__in=vultype)
                if (len(impact)>0):
                    ans4 = ans3.filter(reduce(operator.or_, (Q(impact__contains=one_ele) for one_ele in impact)))
                    # ans4 = ans3.filter(impact__in=impact)
                    if (len(vector)>0):
                        ans5 = ans4.filter(reduce(operator.or_, (Q(vector__contains=one_ele) for one_ele in vector)))
                        # ans5 = ans4.filter(vector__in=vector)
                        if (len(root)>0):
                            ans6 = ans5.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                            # ans6 = ans5.filter(root__in=root)
                            ret=ans6
                        else:
                            ret=ans5
                    elif (len(root)>0):
                        ans6 = ans4.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                        # ans6 = ans4.filter(root__in=root)
                        ret = ans6
                    else:
                        ret = ans4
                elif (len(vector)>0):
                    ans5 = ans3.filter(reduce(operator.or_, (Q(vector__contains=one_ele) for one_ele in vector)))
                    # ans5 = ans3.filter(vector__in=vector)
                    if (len(root)>0):
                        ans6 = ans5.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                        # ans6 = ans5.filter(root__in=root)
                        ret=ans6
                    else:
                        ret=ans5
                elif(len(root)>0):
                    ans6 = ans3.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                    # ans6 = ans3.filter(root__in=root)
                    ret=ans6
                else:
                    ret=ans3
            elif(len(impact)>0):
                ans4 = ans1.filter(reduce(operator.or_, (Q(impact__contains=one_ele) for one_ele in impact)))
                # ans4 = ans1.filter(impact__in=impact)
                if (len(vector)>0):
                    ans5 = ans4.filter(reduce(operator.or_, (Q(vector__contains=one_ele) for one_ele in vector)))
                    # ans5 = ans4.filter(vector__in=vector)
                    if (len(root)>0):
                        ans6 = ans5.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                        # ans6 = ans5.filter(root__in=root)
                        ret = ans6
                    else:
                        ret = ans5
                elif (len(root)>0):
                    ans6 = ans4.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                    # ans6 = ans4.filter(root__in=root)
                    ret = ans6
                else:
                    ret = ans4
            elif(len(vector)>0):
                ans5 = ans1.filter(reduce(operator.or_, (Q(vector__contains=one_ele) for one_ele in vector)))
                # ans5 = ans1.filter(vector__in=vector)
                if (len(root)>0):
                    ans6 = ans5.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                    # ans6 = ans5.filter(root__in=root)
                    ret = ans6
                else:
                    ret = ans5
            elif(len(root)>0):
                ans6 = ans1.filter(reduce(operator.or_, (Q(root__contains=one_ele) for one_ele in root)))
                # ans6 = ans1.filter(root__in=root)
                ret = ans6
            else:
                ret = ans1
        # 优先级2：vul component
        elif(len(vulcomponent)>0):
            ans2 = test.filter(component__contains=vulcomponent[0])
            if (len(vultype)>0):
                ans3 = ans2.filter(type__contains=vultype[0])
                if (len(impact)>0):
                    ans4 = ans3.filter(impact__contains=impact[0])
                    if (len(vector)>0):
                        ans5 = ans4.filter(vector__contains=vector[0])
                        if (len(root)>0):
                            ans6 = ans5.filter(root__contains=root[0])
                            ret = ans6
                        else:
                            ret = ans5
                    elif (len(root)>0):
                        ans6 = ans4.filter(root__contains=root[0])
                        ret = ans6
                    else:
                        ret = ans4
                elif (len(vector)>0):
                    ans5 = ans3.filter(vector__contains=vector[0])
                    if (len(root)>0):
                        ans6 = ans5.filter(root__contains=root[0])
                        ret = ans6
                    else:
                        ret = ans5
                elif(len(root)>0):
                    ans6 = ans3.filter(root__contains=root[0])
                    ret = ans6
                else:
                    ret=ans3
            elif (len(impact)>0):
                ans4 = ans2.filter(impact__contains=impact[0])
                if (len(vector)>0):
                    ans5 = ans4.filter(vector__contains=vector[0])
                    if (len(root)>0):
                        ans6 = ans5.filter(root__contains=root[0])
                        ret = ans6
                    else:
                        ret = ans5
                elif (len(root)>0):
                    ans6 = ans4.filter(root__contains=root[0])
                    ret = ans6
                else:
                    ret = ans4
            elif(len(vector)>0):
                ans5 = ans2.filter(vector__contains=vector[0])
                if (len(root)>0):
                    ans6 = ans5.filter(root__contains=root[0])
                    ret = ans6
                else:
                    ret = ans5
            elif(len(root)>0):
                ans6 = ans2.filter(root__contains=root[0])
                ret = ans6
            else:
                ret=ans2

        # 优先级3： vul type
        elif(len(vultype)>0):
            ans3 = test.filter(type__contains=vultype[0])
            if (len(impact)>0):
                ans4 = ans3.filter(impact__contains=impact[0])
                if (len(vector)>0):
                    ans5 = ans4.filter(vector__contains=vector[0])
                    if (len(root)>0):
                        ans6 = ans5.filter(root__contains=root[0])
                        ret = ans6
                    else:
                        ret = ans5
                elif (len(root)>0):
                    ans6 = ans4.filter(root__contains=root[0])
                    ret = ans6
                else:
                    ret = ans4
            elif (len(vector)>0):
                ans5 = ans3.filter(vector__contains=vector[0])
                if (len(root)>0):
                    ans6 = ans5.filter(root__contains=root[0])
                    ret = ans6
                else:
                    ret = ans5
            elif (len(root)>0):
                ans6 = ans3.filter(root__contains=root[0])
                ret = ans6
            else:
                ret = ans3
        # 优先级4：impact
        elif (len(impact)>0):
            ans4 = test.filter(impact__contains=impact[0])
            if (len(vector)>0):
                ans5 = ans4.filter(vector__contains=vector[0])
                if (len(root)>0):
                    ans6 = ans5.filter(root__contains=root[0])
                    ret = ans6
                else:
                    ret = ans5
            elif (len(root)>0):
                ans6 = ans4.filter(root__contains=root[0])
                ret = ans6
            else:
                ret = ans4
        elif (len(vector)>0):
            ans5 = test.filter(vector__contains=vector[0])
            if (len(root)>0):
                ans6 = ans5.filter(root__contains=root[0])
                ret = ans6
            else:
                ret = ans5
        elif (len(root)>0):
            ans6 = test.filter(root__contains=root[0])
            ret = ans6
        else:
            print('select menu为空')
            nothing=1

        newAnsData = [] #最终返回的结果
        # startRet=ret

        startRet=test # 创建CveInfo对象
        if(nothing!=1): #select menu不为空，multi face查询在此基础上进行再查询，ret为CveInfo对象
            startRet=ret
            # startRet = CveInfoPlus.objects.all()
        else: #select menu为空，搜索从头开始
            pass

        if(score1 or score2):
            startRet=startRet.filter(cvss_score__gte=score11).filter(cvss_score__lte=score22)
        if (severity):
            startRet = startRet.filter(severity=severity)
        if(access):
            startRet = startRet.filter(access=access)
        if (interaction):
            startRet = startRet.filter(interaction=interaction)
        if (authentication):
            startRet = startRet.filter(auth=authentication)
        if (attackComplex):
            startRet = startRet.filter(attack_complex=attackComplex)
        if (confidentiality):
            startRet = startRet.filter(impact_confidence=confidentiality)
        if (integrity):
            startRet = startRet.filter(impact_integer=integrity)
        if (avaliability):
            startRet = startRet.filter(impact_available=avaliability)

        # print('startRet:',startRet)

        ans = list(startRet[:999])
        # print('****************ans******************', ans)

        # 获取最新的菜单
        menu=getMenu(ans)

        all_cveids = []
        for i in ans:
            all_cveids.append(i.cveid)
        if len(all_cveids) > 0:
            urlsObjs = DatabaseIndicator.objects.filter(cveid__in=all_cveids)
            urlsObjs = list(urlsObjs)

        for idx, i in enumerate(ans):
            # 将ansData中的每一个model object转化为JSON，然后删除其中不可序列化的字段
            i = object_to_json(i)
            del i['_state']
            # urlsObj = DatabaseIndicator.objects.get(cveid=i['cveid'])
            urlsObj = urlsObjs[idx]
            urls = object_to_json(urlsObj)
            del urls['_state']
            i['urls'] = urls
            # clean_aspects(i)
            newAnsData.append(i)

        # print('newAnsData结果:', newAnsData)

        # 构造json返回内容
        tmp={}
        data=json.loads(json.dumps(tmp))
        data['findcves']=newAnsData
        data['menu']=menu
        ret=json.dumps(data,ensure_ascii=False)

        return HttpResponse(ret,status=200)
        # return HttpResponse(json.dumps(newAnsData), status=200)
    except Exception as e:
        print(e)
        return HttpResponse("error", status=400)

# objects.get()结果转换
def object_to_json(obj):
    ans={}
    # obj.__dict__ 可将django对象转化为字典
    for key, value in obj.__dict__.items():
        # 将字典转化为JSON格式
        ans[key]=value
    return ans

# 查询某一条cve的具体信息
def searchOneCve(request):
    try:
        print("*****searchOneCve*****")
        assert request.method == 'POST'
        # 取到搜索关键字key
        key = request.POST.get("cveid")
        print("cveid:", key)
        if key == None:
            return HttpResponse("后端获取到的cveid为空")
        else:
            ans=CveInfoPlus.objects.get(cveid=key)
            print('ans类型', type(ans))
            # 定义ansData，存储object.get()后的JSON数据
            ansData=object_to_json(ans)
            # 删除以下字段，否则将无法进行JSON序列化
            del ansData['_state']
            print('***ansData为***：', ansData)

            return HttpResponse(json.dumps(ansData),status=200)
    except Exception as e:
        print(e)
        return HttpResponse("error", status=400)

def getBarPicData(request):
    try:
        print("*****getBarPicData*****")
        assert request.method == 'POST'
        # 取到搜索关键字key
        product = request.POST.get("product")
        if '(' in product:
            product = '('.join(product.split('(')[:-1]).strip()
        else:
            product = product.strip()
        tp = TextPreprocess()
        product = tp.clean_so_data_nopos(product)
        aspect_type = request.POST.get("aspect_type")
        if product=='':
            return HttpResponse("product为空")
        else:
            # 1、先从Aspect2Table表中查找对应的产品编号
            ans=Aspect2Table.objects.filter(aspect=product) # 查找对应的产品编号
            if ans:
                # print('ans', ans)
                ans=ans.get(aspect_id__icontains=aspect_type)  # 因为一个词可能存在多类aspect，我们只选取aspect=product的
                # ans=list(ans)
                # print('产品编号', ans)
                id=ans.aspect_id

                # 2、再从AspectCvssInfo表中查找对应的serverity、access、interaction信息
                ans = AspectCvssInfo.objects.get(aspect_id=id)  # 查找对应的产品编号
                # 3、从Aspect2Year表中查找对应的TimeLine数据
                ans1=Aspect2Year.objects.get(aspect_id=id)
                # 4、从Aspect2CvssYear表中查找对应的C3BM数据
                ans2=Aspect2CvssYear.objects.get(aspect_id=id)

                # 定义ansData，存储object.get()后的JSON数据
                ansData=object_to_json(ans)
                del ansData['_state']
                # print('***ansData为***：', ansData)
                ansData1 = object_to_json(ans1)
                del ansData1['_state']
                del ansData1['aspect_id']
                # print('***ansData为***：', ansData)
                ansData2 = object_to_json(ans2)
                del ansData2['_state']
                del ansData2['aspect_id']
                # print('***ansData为***：', ansData)

                # 构造json返回内容
                pic_info={}
                data=json.loads(json.dumps(pic_info))
                data['bar']=ansData
                data['timeline']=ansData1
                data['c3bm']=ansData2
                ret=json.dumps(data,ensure_ascii=False)
                return HttpResponse(ret,status=200)
            else:
                return HttpResponse('0')
    except Exception as e:
        print(e)
        return HttpResponse("error", status=400)


def getAspectMultiInfo(request):
    try:
        print("*****getAspectMultiInfo*****")
        print(time.time())
        assert request.method == 'POST'
        # 取到搜索关键字key
        product = request.POST.get("product")
        if '(' in product:
            product = '('.join(product.split('(')[:-1]).strip()
        else:
            product = product.strip()
        tp = TextPreprocess()
        product = tp.clean_so_data_nopos(product)
        aspect_type = request.POST.get("aspect_type")
        if product == '':
            return HttpResponse("product为空")
        else:
            print(time.time())
            ans=Aspect2Table.objects.filter(aspect=product) # 查找对应的产品编号
            if ans:
                # print('ans', ans)
                ans=ans.get(aspect_id__icontains=aspect_type)  # 因为一个词可能存在多类aspect，我们只选取aspect=product的
                # ans=list(ans)
                # print('产品编号', ans)
                id=ans.aspect_id
                multi_info = AspectMultiInfoNew.objects.filter(aspect_1=id)
                newAnsData = []
                print(time.time())
                for i in multi_info:
                    i = object_to_json(i)
                    del i['id']
                    del i['_state']
                    # i['aspect_1'] = Aspect2Table.objects.get(aspect_id=i['aspect_1']).aspect
                    # i['aspect_2_ori'] = i['aspect_2']
                    # i['aspect_2'] = Aspect2Table.objects.get(aspect_id=i['aspect_2']).aspect
                    newAnsData.append(i)
                print(time.time())
                return HttpResponse(json.dumps(newAnsData,ensure_ascii=False), status=200)
            else:
                return HttpResponse('0')
    except Exception as e:
        print(e)
        return HttpResponse("error", status=400)


def getCompareData(request):
    try:
        print("*****getCompareData*****")
        assert request.method == 'POST'
        # 取到搜索关键字key
        cveid = request.POST.get("cveid")
        if cveid == '':
            return HttpResponse("cveid为空")
        else:
            ans = AspectCompare.objects.get(cveid=cveid)  # 查找CVE的各数据库比较数据
            print('查找结果：', ans)
            # 定义ansData，存储object.get()后的JSON数据
            ansData = object_to_json(ans)
            # 删除以下字段，否则将无法进行JSON序列化
            del ansData['_state']
            # print('ansData为：', ansData)
        return HttpResponse(json.dumps(ansData), status=200)
    except Exception as e:
        print(e)
        return HttpResponse("error", status=400)


def searchByStrHe(request):
    try:
        print("*****searchByStr2*****")
        assert request.method == 'POST'
        # 取到搜索关键字key
        searchStr = request.POST.get("key")
        # searchStr='unam'
        searchStrBackup=searchStr
        print("搜索Str:", searchStr)
        if searchStr == None:
            return HttpResponse("后端获取到的searchStr为空")
        else:
            # 第一步：筛选出candidates，根据优先级
            # 优先级：product name>vul component>vul type>impact>vector>root>version
            finalCveList=[]   # 最后将要展示在前端的CVE的CVEID的集合
            ansSet = []     # 当搜索关键词直接是CVE编号时，AnsSet直接存储对应的qs

            if searchStr.find(',')!=-1:  # 字符串中由,切割开，说明搜索条件有多个
                typelist=[]
                cveslist=[]  # cve结果集交集，用作加分的依据
                cveslistByWord=[]  # 根据优先级最高的word初步筛选cves
                cveslistByWordNext=[]  # 根据剩余的words筛选cves
                cveslistByWords=[]  # 根据词组words筛选cves
                cveAndScore = []  # 每个cve及其对应的分数

                searchStrBackup = searchStrBackup.replace(", ", ",")  # 避免词组开头的空格符号对数据库匹配造成影响
                wordslist = searchStrBackup.split(',')  # 存储词组
                wordslistCopy = list(wordslist)
                # print('wordslist：', wordslist)

                searchStr1=searchStr
                searchStr1=searchStr1.replace(", ", ",")
                searchStr1 = searchStr1.replace(" ", ",")
                wordlist=searchStr1.split(",")  # 存储单词
                wordlistCopy=[]  # 删除优先级最高的单词
                print('wordlist：', wordlist)

                # 1、从home WordType2中找出每个单词的aspect类型，然后对其按照优先级
                for word in wordlist:
                    tmp0=WordType2.objects.filter(word=word)  # 精准搜索，得到一个qs集合
                    tmp0=list(tmp0)
                    strType = ''  # 找出该词组所有的type，取优先级最高的为确定type
                    for t in tmp0:
                        strType=strType+t.type
                    if strType.find('name')!=-1:
                        typelist.append({'type': 'name', 'word': word, 'id': '1'})
                    elif strType.find('component')!=-1:
                        typelist.append({'type': 'component', 'word': word, 'id': '2'})
                    elif strType.find('type')!=-1:
                        typelist.append({'type': 'type', 'word': word, 'id': '3'})
                    elif strType.find('impact')!=-1:
                        typelist.append({'type': 'impact', 'word': word, 'id': '4'})
                    elif strType.find('vector')!=-1:
                        typelist.append({'type': 'vector', 'word': word, 'id': '5'})
                    elif strType.find('root')!=-1:
                        typelist.append({'type': 'root', 'word': word, 'id': '6'})
                    else:
                        print('word:', word)
                        print('未在WordType2数据表中找到单词的类型！')
                # 2、将typelist按照type的优先级排序，优先级为product name>vul component>vul type>impact>vector>root>version
                typelist.sort(key=lambda obj:(obj.get('id')), reverse=False)  # 按照升序排列，默认升序
                priority=[]  # 存放了按照优先级排序的关键words
                ifOneType=[]  # 优先级最高的word存在多个，如果word的优先级相同，则最后的cvelist应该是各个word对应cvelist的并集
                firstType=typelist[0]['type']  # 优先级最高的aspect
                for i in typelist:
                    wordlistCopy.append(i['word'])
                    if i['type']==firstType:
                        ifOneType.append(i['word'])
                        wordlistCopy.pop(0)  # 删除优先级最高的单词
                    priority.append(i['word'])   # 将关键词按照优先级排序
                # print('typelist：', typelist)
                # print('wordlistCopy：', wordlistCopy)
                # print('ifOneType：', ifOneType)
                # print('priority：', priority)

                # 3、根据优先级筛选出candidates
                # 根据wordlist中的单词筛选cve
                for word in ifOneType:
                    # print('word为'+word)
                    ansByWord = Word2Cve.objects.filter(word=word)  # 根据优先级最高的word在Word2Cve中查找对应的cve
                    ansByWord = list(ansByWord)
                    # print('ansByWord[0]：', ansByWord[0].type)
                    for i in ansByWord:
                        cveslistByWord.append(i.type)  # 将对应的cve添加到cvelistByWord中
                        cveAndScore.append({'cve': i.type, 'score': 0})
                    # print('len cveslistByWord：', len(cveslistByWord))

                print('len cveslistByWord：', len(cveslistByWord))


                # 第二步：打分，分高的在前面
                # 1、单词打分：提取出搜索字符串中的单词，strlist中为切分的词组
                print('*****单词打分*****')
                for word in wordlistCopy:
                    ansByWord = Word2Cve.objects.filter(word=word)  # 根据次优先级的word在Word2Cve中查找对应的cve
                    ansByWord = list(ansByWord)
                    # print('len ansByWord：', len(ansByWord))
                    for i in ansByWord:
                        cveslistByWordNext.append(i.type)  # 将对应的cve添加到cvelistByWordNext中
                # 求两个搜索结果集的交集
                cveslist=list(set(cveslistByWord) & set(cveslistByWordNext))
                print('len cveslist：', len(cveslist))
                for one in cveAndScore:
                    if one['cve'] in cveslist:
                        one['score']=one['score']+1
                # Debug
                cveAndScore.sort(key=lambda obj: (obj.get('score')), reverse=True)  # 按照升序排列，默认升序
                print('cveAndScore:', cveAndScore[0:5])

                # # 2、词组打分
                print('*****词组打分*****')
                for words in wordslist:
                    ansByWords = Phrase2Cve.objects.filter(word=words)  # 根据次优先级的word在Phrase2Cve中查找对应的cve
                    ansByWords = list(ansByWords)
                    # print('len ansByWord：', len(ansByWord))
                    for i in ansByWords:
                        cveslistByWords.append(i.type)  # 将对应的cve添加到cvelistByWordNext中
                    # 求两个搜索结果集的交集
                cveslist = list(set(cveslistByWord) & set(cveslistByWords))
                print('len cveslist：', len(cveslist))
                for one in cveAndScore:
                    if one['cve'] in cveslist:
                        one['score'] = one['score'] + 1

                # # 3、同义词打分
                # print('\n*****同义词打分*****')
                # thesauruslist=[]  # 所有word的所有同义词
                # for word in wordlist:
                #     print('word:',word)
                #     # 在WordThesaurus表中查找其同义词
                #     qs=WordThesaurus.objects.filter(thesaurus=word)
                #     # print('qs:',qs)
                #     if qs:  # 存在同义词
                #         thesaurus = []  # 存储该词所有的近义词
                #         cvesByThesaurus=[]  # 存储该词所有的近义词对应的cve
                #         allType=[]  # 该词的类型可能不只一种
                #         qs = list(qs)
                #         for q in qs:  # 一个词可能存在多种类型
                #            allType.append(q.type)
                #         for type in allType:
                #             qqs = WordThesaurus.objects.filter(type=type)
                #             qqs=list(qqs)
                #             for qq in qqs:
                #                 thesaurus.append(qq.thesaurus)
                #         print("thesaurus len:",len(thesaurus))
                #         # 查找该词所有同义词所对应的cve
                #         for words in thesaurus:
                #             ansByWords = Phrase2Cve.objects.filter(word=words)  # 根据同义词在Phrase2Cve中查找对应的cve
                #             ansByWords = list(ansByWords)
                #             for i in ansByWords:
                #                 cvesByThesaurus.append(i.type)  # 将对应的cve添加到cvesByThesaurus中
                #             # 求两个搜索结果集的交集
                #         cveslist = list(set(cveslistByWord) & set(cvesByThesaurus))
                #         print('len cveslist：', len(cveslist))
                #         for one in cveAndScore:
                #             if one['cve'] in cveslist:
                #                 one['score'] = one['score'] + 1
                #     else:
                #         pass

                # # 2.2、将cvesOfEachType按照score的高低排序，按照降序排列，分数高的在前
                print('\n*****排序*****')
                cveAndScore.sort(key=lambda obj: (obj.get('score')), reverse=True)
                for i in cveAndScore[0:99]:
                    finalCveList.append(i['cve'])

            else:  # 只有一个搜索条件
                # print("*****只有一个搜索条件*****")
                # 当搜索条件是CVE编号or正常搜索关键词时，是不同的，因为可以直接根据编号进行cveid的filter
                if searchStr.find('CVE-')!=-1:
                    ansSet = CveInfoPlus.objects.filter(cveid__icontains=searchStr)
                    global searchQS
                    searchQS=ansSet
                    print("searchQS:",searchQS)
                else:
                    wordlist=[]  # 存储搜索条件
                    if searchStr.find(' ') !=-1:
                        wordlist=searchStr.split(' ')
                    else:
                        wordlist.append(searchStr)
                    print("wordlist:",wordlist)
                    alllist = []
                    for word in wordlist:
                        # print('word为'+word)
                        tmplist = []
                        ansByWord = Word2Cve.objects.filter(word=word)  # 根据优先级最高的word在Word2Cve中查找对应的cve
                        if ansByWord:
                            ansByWord = list(ansByWord)
                            # print('ansByWord[0]：', ansByWord[0].type)
                            for i in ansByWord:
                                # tmplist.append(i.type)
                                finalCveList.append(i)
                        # alllist.append(tmplist)
                    # print("alllist:", alllist)
                    # for list in alllist:
                    #     if list:
                    #         finalCveList=list
                    #         break
                    # for list in alllist:
                    #     if list:
                    #         finalCveList = list(set(list) & set(finalCveList))



            print("finalCveList:",finalCveList)
            # 根据cveid在CveInfo表格中查找对应的cve
            newAnsData = []   # 定义一个新的List以存放处理后的CVE List
            menu=[]
            if finalCveList:
                menuAns = []  # 用于getMenu传参
                searchQSChild=[]  # 用于将list转化为querySet，数组里面的每一个元素都是一个CveInfo对象
                for cve in finalCveList[0:99]:
                    ans=CveInfoPlus.objects.filter(cveid=cve)
                    if ans:
                        ansData=list(ans)
                        for i in ansData:
                            menuAns.append(i)
                            # 将ansData中的每一个model object转化为JSON，然后删除其中不可序列化的字段
                            i=object_to_json(i)
                            del i['_state']
                            del i['id']
                            urlsObj = DatabaseIndicator.objects.get(cveid=cve)
                            urls = object_to_json(urlsObj)
                            del urls['_state']
                            del urls['id']
                            i['urls']=urls
                            newAnsData.append(i)
                searchQSChild=menuAns
                menu = getMenu(menuAns)
                # 将list转化为CveInfo对象
                childs=CveInfoPlus.objects.filter(cveid__in=[x.cveid for x in searchQSChild])
                # print("childs:",childs)
                searchQS=childs
            elif ansSet:  # 搜索关键词直接带有CVE编号
                ansData = list(ansSet)
                menu=getMenu(ansData)
                for i in ansData:
                    # 将ansData中的每一个model object转化为JSON，然后删除其中不可序列化的字段
                    i = object_to_json(i)
                    del i['_state']
                    del i['id']
                    urlsObj = DatabaseIndicator.objects.get(cveid=i['cveid'])
                    urls = object_to_json(urlsObj)
                    del urls['_state']
                    del urls['id']
                    i['urls'] = urls
                    newAnsData.append(i)

            # 构造json返回内容
            tmp = {}
            data = json.loads(json.dumps(tmp))
            data['searchcves'] = newAnsData
            data['menu'] = menu
            ret = json.dumps(data, ensure_ascii=False)

            return HttpResponse(ret, status=200)

    except Exception as e:
        print('search2 error',e)
        return HttpResponse("searchByStr2 error", status=400)