#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache as redisConn
from django.contrib.auth import authenticate,login
from  .forms import RuleForm,RuleAdd
import json,redis
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from models import User
import traceback,copy
import RuleOperation

def getServiceAndEventSource():
    '''
    从上层服务获取service和EventSource列表
    '''
    serviceAndEvent = RuleOperation.getServiceAndEventSource()
    sourceList = []
    for source in serviceAndEvent["eventSource"]:
        for k, v in source.items():
            sourceForm = (k, v)
            sourceList.append(sourceForm)
    serviceList = []
    for source in serviceAndEvent["serviceList"]:
        for k, v in source.items():
            sourceForm = (k, v)
            serviceList.append(sourceForm)
    return serviceList,sourceList
@login_required
def GetAllDevice(request):
    '''
    获取所有设备，以及上面的规则，以json格式渲染到html中
    :param request:
    :return:
    '''
    print(request)
    try:
        jsonTree=RuleOperation.getAlldevice()
        if jsonTree:
            message=request.GET.get("message")
            if message:
                DetailData=message
            else:
                DetailData=''
            context={"aa":json.dumps(jsonTree),"DetailData":DetailData}
        else:
            context={"aa":None,"DetailData":"没有设备，请先添加设备~"}
    except Exception,ex:
        traceback.print_exc()
        context={"aa":None,"DetailData":ex}
    finally:
        return render(request, 'rulelist/test.html', context)

def GetDeviceRuleChannel(request,deviceID,channelID):
    '''
    根据设备ID和通道ID获取通道上面的规则
    :param request:
    :param deviceID:
    :param channelID:
    :return:
    '''
    redisID=":{0}:{1},{2}".format("ruleDevice",deviceID,channelID)
    ruleIdList=redisConn.smembers(redisID)
    #ruleIdList=redisConn.get(":ruleDevice:17763917-051e-4508-9ff3-d3bd186fa4c1_0")
    if len(ruleIdList)==0:
        return HttpResponse("This channel has not any rule!!")
    try:
        ruleList=RuleOperation.getDeviceRuleList(ruleIdList)
        if ruleList:
            context={"ruleList":ruleList}
        else:
            context={"ruleList":None}
    except RuntimeError,ex:
        context={"ruleList":None}
    finally:
        return render(request, 'rulelist/redis.html', context)

def GetRuleByRuleID(request,ruleID):
    '''
    根据规则ID，获取规则，展示规则
    :param request:
    :param ruleID:
    :return:
    '''
    try:
        if request.method=='POST':
            ruleEditData=request.POST.copy()
            ruleEditData["ruleID"]=ruleID
            flag=RuleOperation.updateRule(ruleEditData)
            if flag==False:
                return HttpResponseRedirect('/deviceRule/?message=修改失败')
            else:
                return HttpResponseRedirect('/deviceRule/?message=修改成功')
        else:
            rule=RuleForm()
            AssembleRule=RuleOperation.getDeviceRule(ruleID)
            if AssembleRule:
                sourceList=[]
                for source in AssembleRule.SourceList:
                    for k,v in source.items():
                        sourceForm=(k,v)
                        sourceList.append(sourceForm)
                rule.fields["EventSourceID"].choices=sourceList
                rule.fields["EventSourceID"].initial = AssembleRule.baseRule.EventSourceID
                serviceList=[]
                for service in AssembleRule.ServList:
                    for k,v in service.items():
                        serviceList.append((k,v))
                rule.fields["ServiceID"].choices=serviceList
                rule.fields["ServiceID"].initial=AssembleRule.baseRule.ServiceID
                rule.fields["Name"].initial=AssembleRule.baseRule.Name
                #rule.fields["level"].choices=[(0,0),(1,3),(2,4),(3,5),(4,6)]
                rule.fields["EventLevel"].initial=AssembleRule.baseRule.EventLevel
                rule.fields["EventSourceConfig"].initial=AssembleRule.baseRule.ConfigData
                if AssembleRule.baseRule.IsActive:
                    rule.fields["IsActive"].initial=1
                else:
                    rule.fields["IsActive"].initial=0
                if AssembleRule.baseRule.StreamIndex==1:
                    rule.fields["StreamIndex"].initial=1
                else:
                    rule.fields["StreamIndex"].initial=0
                return render(request,'rulelist/ruleDetail.html',{'form':rule})
            else:
                return render(request,'rulelist/error.html',context={"DetailData":"没有此规则，或者此规则刚刚删除，请刷新页面！"})
    except RuntimeError,ex:
        traceback.print_exc()
        return render(request, 'rulelist/error.html', {'DetailData': ex})

def deleteRuleByRuleID(request,ruleID):
    '''
    根据规则ID，删除指定的规则
    :param request:
    :param ruleID:
    :return:
    '''
    try:
        flag=RuleOperation.deleteRule(ruleID)
        if flag==0:
            return HttpResponse("删除成功")
        else:
            return HttpResponse("删除失败")
    except:
        traceback.print_exc()
        return HttpResponse("删除失败")

def AddRuleByDeviceID(request,deviceID,channelID):
    '''
    根据设备ID和通道ID,，添加到此设备通道上
    :param request:
    :param deviceID:
    :param channelID:
    :return:
    '''
    try:
        if request.method=="POST":
            serviceList,sourceList=getServiceAndEventSource()
            form=RuleAdd(request.POST,ServiceChoices=serviceList,EventSourceChoices=sourceList)
            # rule=RuleAdd(request.POST)
            rule = request.POST.copy()
            rule["DeviceID"]=deviceID
            rule["ChannelIndex"]=int(channelID)
            flag=RuleOperation.addRule(rule)
            if flag==False:
                return HttpResponseRedirect('/deviceRule/?message=修改失败')
            else:
                return HttpResponseRedirect('/deviceRule/?message=添加失败')
        else:
            serviceList,sourceList=getServiceAndEventSource()
            rule=RuleAdd(ServiceChoices=serviceList,EventSourceChoices=sourceList)
            rule.fields["IsActive"].initial=0
            return render(request, 'rulelist/ruleDetail.html', {'form': rule})
    except Exception,ex:
        traceback.print_exc()
        message='/deviceRule/?message=调用ice接口发生错误，或者提交表时发生错误！！错误详情：{0}'.format(ex)
        return HttpResponseRedirect(message)

