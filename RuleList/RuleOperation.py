#!/usr/bin/env python
# coding=utf-8
import Ice
import Vistek.Data as v_data
import traceback,copy
import uuid,datetime,time
def CreateRuleSerClient():
    try:
        ic=Ice.initialize()
        base=ic.stringToProxy("DeviceRuleServer:tcp -h 172.16.0.181 -p 30003")
        RuleServer=v_data.RuleServicePrx.checkedCast(base)
        return (ic, RuleServer)
    except Exception,ex:
        traceback.print_exc()
        return None
        #raise RuntimeError("Create Rule Service Client error!!")
    finally:
        if not ic:
            ic.destroy()

def getAlldevice():
    try:
        client=CreateRuleSerClient()
        if  client:
            ic=client[0]
            ruleserver=client[1]
            deviceTree=ruleserver.GetAllDevices()
            #print(deviceTree)
            ic.destroy()
            return deviceTree
        else:
            raise RuntimeError("Connect ice cause Error!!")
    except:
        traceback.print_exc()
        return None
    finally:
        if not ic:
            ic.destroy()
def getDeviceRuleList(ruleIdList):
    try:
        client=CreateRuleSerClient()
        if client:
            ic=client[0]
            ruleserver=client[0]
            ruleList=ruleserver.GetRuleByIdList(ruleIdList)
            ic.destroy()
            return ruleIdList
        else:
            raise RuntimeError("Connect ice cause Error!!")
    except:
        traceback.print_exc()
        return None
    finally:
        if not ic:
            ic.destroy()

def getDeviceRule(ruleID):
    try:
        client=CreateRuleSerClient()
        if client:
            ic=client[0]
            ruleserver=client[1]
            rule=ruleserver.GetRuleByID(ruleID)
            ic.destroy()
            return rule
        else:
            raise RuntimeError("Connect ice cause Error!!")
    except:
        traceback.print_exc()
        return None
    finally:
        if not ic:
            ic.destroy()
def updateRule(ruleEditData):
    try:
        client=CreateRuleSerClient()
        if client:
            ic=client[0]
            ruleserver=client[1]
            ruleID=ruleEditData["ruleID"]
            rule=getDeviceRule(ruleID)
            ruleEditDataIce=valueData(ruleEditData,rule)
            flag=ruleserver.UpdateRule(rule.baseRule)
            ic.destroy()
            return flag
        else:
            raise RuntimeError("Connect ice cause Error!!")
    except:
        traceback.print_exc()
        return None
    finally:
        if not ic:
            ic.destroy()
def addRule(rulePOST):
    try:
        client=CreateRuleSerClient()
        if client:
            ic=client[0]
            ruleserver=client[1]
            AsRule=v_data.AsRule()
            AsRule.ID=str(uuid.uuid1())
            AsRule.Name=rulePOST["Name"].encode("utf-8")
            AsRule.DeviceID=rulePOST["DeviceID"]
            AsRule.ChannelIndex=int(rulePOST["ChannelIndex"])
            AsRule.StreamIndex=int(rulePOST["StreamIndex"])
            AsRule.ServiceID=rulePOST["ServiceID"]
            AsRule.EventLevel=int(rulePOST["EventLevel"])
            if rulePOST["IsActive"]==0:
                AsRule.IsActive=False
            else:
                AsRule.IsActice=True
            AsRule.EventSourceID=rulePOST["EventSourceID"]
            AsRule.ConfigData=bytearray(source=rulePOST["EventSourceConfig"],encoding='utf-8')
            AsRule.ChangedDateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            flag=ruleserver.UpdateRule(AsRule)
            ic.destroy()
            return flag
        else:
            raise RuntimeError("Connect ice cause Error!!")
    except:
        traceback.print_exc()
        return None
    finally:
        if not ic:
            ic.destroy()
def valueData(ruleData,rule):
    ruleEditIce = v_data.ruleEdit()
    ruleData["EventLevel"]=int(ruleData["EventLevel"])
    if ruleData["IsActive"]==1:
        ruleData["IsActive"]=True
    else:
        ruleData["IsActive"]=False
    if ruleData["StreamIndex"]=='1':
        ruleData["StreamIndex"]=1
    else:
        ruleData["StreamIndex"]=0
    rule.baseRule.Name=ruleData["Name"].encode("utf-8")
    rule.baseRule.IsActive=ruleData["IsActive"]
    rule.baseRule.EventLevel=ruleData["EventLevel"]
    rule.baseRule.StreamIndex=ruleData["StreamIndex"]
    rule.baseRule.ServiceID=ruleData["ServiceID"]
    rule.baseRule.EventSourceID=ruleData["EventSourceID"]
    rule.baseRule.ConfigData=bytearray(source=ruleData["EventSourceConfig"],encoding='utf-8')
    #print(rule.baseRule)
def getServiceAndEventSource():
    try:
        client=CreateRuleSerClient()
        if client:
            ic=client[0]
            ruleserver=client[1]
            ServiceAndEvent=ruleserver.getServiceAndEventSource()
            return ServiceAndEvent
        else:
            raise RuntimeError("Connect ice cause Error!!")
    except:
        traceback.print_exc()
        return None
    finally:
        if not ic:
            ic.destroy()

def deleteRule(ruleID):
    try:
        client=CreateRuleSerClient()
        if client:
            ic=client[0]
            ruleserver=client[1]
            flag=ruleserver.DeleteRule(ruleID)
            return flag
        else:
            raise RuntimeError("Connect ice cause Error!!")
    except:
        traceback.print_exc()
        return None
    finally:
        if not ic:
            ic.destroy()