#!/usr/bin/env python
# coding=utf-8
from django.shortcuts import render
from django.conf import settings
#from django.core.cache import cache as redisConn
from django.contrib.auth import authenticate,login
from  .forms import RuleForm,RuleAdd
import json,redis
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from models import User
import traceback,copy
import RuleOperation
redisConn=redis.StrictRedis(host="172.16.0.181")

@login_required
def GetAllDevice(request):
    # if request.method== 'POST':
    #     form = forms.AuthenticationForm(request.POST)
    #     if form.is_valid():
    #         username=form.cleaned_data['username']
    #         password=form.cleaned_data['password']
    #         user=User.objects.filter(username__exact=username,password__exact=password)
    #         if user:
    #             repose
    try:
        deviceTree=RuleOperation.getAlldevice()
        if deviceTree:
            jsonTree=[]
            for parent in deviceTree:
                pnode={}
                pnode["text"]=parent.text
                pnode["tags"]=parent.tags
                pnode["nodes"]=[]
                for node in parent.nodes:
                    cnode={}
                    cnode["text"]=node.text
                    cnode["tags"]=node.tags
                    cnode["href"]=node.href
                    cnode["nodes"]=[]
                    for grandchileNode in node.nodes:
                        gnode={}
                        gnode["text"]=grandchileNode.text
                        gnode["href"]=grandchileNode.href
                        cnode["nodes"].append(gnode)
                    pnode["nodes"].append(cnode)
                jsonTree.append(pnode)
            context={"aa":json.dumps(jsonTree)}
        else:
            context={"aa":None}
    except RuntimeError,ex:
        print(ex)
        context={"aa":None}
    finally:
        return render(request, 'rulelist/test.html', context)

def GetDeviceRuleChannel(request,deviceID,channelID):
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
    try:
        if request.method=='POST':
            a=request.POST["IsActive"]
            ruleEditData=request.POST.copy()
            ruleEditData["ruleID"]=ruleID
            flag=RuleOperation.updateRule(ruleEditData)
            if flag==False:
                return HttpResponse("修改失败")
            else:
                return HttpResponse("修改成功")
        else:
            rule=RuleForm()
            eventSource=RuleOperation.getDeviceRule(ruleID)
            sourceList=[]
            for source in eventSource.SourceList:
                for k,v in source.items():
                    sourceForm=(k,v)
                    sourceList.append(sourceForm)
            rule.fields["EventSourceID"].choices=sourceList
            rule.fields["EventSourceID"].initial = eventSource.baseRule.EventSourceID
            serviceList=[]
            for service in eventSource.ServList:
                for k,v in service.items():
                    serviceList.append((k,v))
            rule.fields["ServiceID"].choices=serviceList
            rule.fields["ServiceID"].initial=eventSource.baseRule.ServiceID
            rule.fields["Name"].initial=eventSource.baseRule.Name
            #rule.fields["level"].choices=[(0,0),(1,3),(2,4),(3,5),(4,6)]
            rule.fields["EventLevel"].initial=eventSource.baseRule.EventLevel
            rule.fields["EventSourceConfig"].initial=eventSource.baseRule.ConfigData
            if eventSource.baseRule.IsActive:
                rule.fields["IsActive"].initial=1
            else:
                rule.fields["IsActive"].initial=0
            if eventSource.baseRule.StreamIndex==1:
                rule.fields["StreamIndex"].initial=1
            else:
                rule.fields["StreamIndex"].initial=0
            return render(request,'rulelist/ruleDetail.html',{'form':rule})
    except:
        traceback.print_exc()

def deleteRuleByRuleID(request,ruleID):
    try:
        print(ruleID)
        flag=RuleOperation.deleteRule(ruleID)
        print(flag)
        if flag==0:
            return HttpResponse("删除成功")
        else:
            return HttpResponse("删除失败")
    except:
        traceback.print_exc()
        return HttpResponse("删除失败")
def AddRuleByDeviceID(request,deviceID,channelID):
    try:
        if request.method=="POST":
            # rule=RuleAdd(request.POST)
            rule = request.POST.copy()
            rule["DeviceID"]=deviceID
            rule["ChannelIndex"]=int(channelID)
            flag=RuleOperation.addRule(rule)
            if flag==False:
                return HttpResponse("添加失败")
            else:
                return HttpResponse("添加成功")
        else:
            rule=RuleAdd()
            rule.fields["IsActive"].initial=0
            serviceAndEvent=RuleOperation.getServiceAndEventSource()
            sourceList=[]
            for source in serviceAndEvent["eventSource"]:
                for k,v in source.items():
                    sourceForm=(k,v)
                    sourceList.append(sourceForm)
            rule.fields["EventSourceID"].choices=sourceList
            serviceList=[]
            for source in serviceAndEvent["serviceList"]:
                for k,v in source.items():
                    sourceForm=(k,v)
                    serviceList.append(sourceForm)
            rule.fields["ServiceID"].choices=serviceList
            return render(request, 'rulelist/ruleDetail.html', {'form': rule})
    except:
        traceback.print_exc()
        pass