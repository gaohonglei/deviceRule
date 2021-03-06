#!/usr/bin/env python
# coding=utf-8
import Ice
import Vistek.Data as v_data
import traceback,copy
import uuid,datetime,time
#创建VistekDeviceRule服务客户端
try:
    ic = Ice.initialize()
    base = ic.stringToProxy("DeviceRuleServer:tcp -h 172.16.0.181 -p 30004")
    RuleServer = v_data.RuleServicePrx.checkedCast(base)
except:
    raise RuntimeError("连接ice出错！！")

def getJsonTree(deviceTree):
    '''
    生成json数据结构
    :param deviceTree:
    :return:
    '''
    if deviceTree:
        jsonTree = []
        for parent in deviceTree:
            pnode = {}
            pnode["text"] = parent.text
            pnode["tags"] = parent.tags
            pnode["nodes"] = []
            for node in parent.nodes:
                cnode = {}
                cnode["text"] = node.text
                cnode["tags"] = node.tags
                cnode["href"] = node.href
                cnode["nodes"] = []
                for grandchileNode in node.nodes:
                    gnode = {}
                    print(type(grandchileNode.text))
                    gnode["text"] = grandchileNode.text
                    gnode["href"] = grandchileNode.href
                    cnode["nodes"].append(gnode)
                pnode["nodes"].append(cnode)
            jsonTree.append(pnode)
        return jsonTree
    else:
        return None
def WCreateRuleSerClient(RuleServer):
    '''
    带参数的装饰器
    :param RuleServer:
    :return:
    '''
    def common(fun):
        def wraper(*args,**kwargs):
            try:
                return fun(*args,ruleserver=RuleServer)
            except:
                traceback.print_exc()
                raise RuntimeError("调用ice接口返回异常！！请检查调用接口~~")
        return wraper
    return common


def CreateRuleSerClient():
    try:
        ic=Ice.initialize()
        base=ic.stringToProxy("DeviceRuleServer:tcp -h 172.16.0.181 -p 30004")
        RuleServer=v_data.RuleServicePrx.checkedCast(base)
        return (ic, RuleServer)
    except Exception,ex:
        traceback.print_exc()
        if ic:
            ic.destroy()
        return None
        #raise RuntimeError("Create Rule Service Client error!!")

@WCreateRuleSerClient(RuleServer)
def getAlldevice(ruleserver):
    '''
    获取所有设备
    :param ruleserver:
    :return:
    '''
    deviceTree=ruleserver.GetAllDevices()
    jsonTree=getJsonTree(deviceTree)
    return jsonTree

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
        if ic:
            ic.destroy()
@WCreateRuleSerClient(RuleServer)
def getDeviceRule(ruleID,ruleserver):
    '''
    根据规则ID，获取规则详情
    :param ruleID:
    :param ruleserver:
    :return:
    '''
    rule=ruleserver.GetRuleByID(ruleID)
    return rule
@WCreateRuleSerClient(RuleServer)
def updateRule(ruleEditData,ruleserver):
    '''
    更新规则
    :param ruleEditData:
    :param ruleserver:
    :return:
    '''
    ruleID=ruleEditData["ruleID"]
    rule=getDeviceRule(ruleID)
    ruleEditDataIce=valueData(ruleEditData,rule)
    flag=ruleserver.UpdateRule(rule.baseRule)
    return flag

@WCreateRuleSerClient(RuleServer)
def addRule(rulePOST,ruleserver):
    '''
    添加规则
    :param rulePOST: post表单数据
    :param ruleserver:
    :return:
    '''
    AsRule=v_data.AsRule()
    AsRule.ID=str(uuid.uuid1())
    AsRule.Name=rulePOST["Name"].encode("utf-8")
    AsRule.DeviceID=rulePOST["DeviceID"]
    AsRule.ChannelIndex=int(rulePOST["ChannelIndex"])
    AsRule.StreamIndex=int(rulePOST["StreamIndex"])
    AsRule.ServiceID=rulePOST["ServiceID"]
    AsRule.EventLevel=int(rulePOST["EventLevel"])
    rulePOST["IsActive"]=rulePOST["IsActive"].encode("utf-8")
    if int(rulePOST["IsActive"])==0:
        AsRule.IsActive=False
    else:
        AsRule.IsActive=True
    AsRule.EventSourceID=rulePOST["EventSourceID"]
    AsRule.ConfigData=bytearray(source=rulePOST["EventSourceConfig"],encoding='utf-8')
    AsRule.ChangedDateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flag=ruleserver.UpdateRule(AsRule)
    return flag

def valueData(ruleData,rule):
    '''
    根据ruleData 生成指定的ruleEdit结构
    :param ruleData: post表单数据
    :param rule:
    :return:
    '''
    ruleEditIce = v_data.ruleEdit()
    ruleData["EventLevel"]=int(ruleData["EventLevel"])
    if int(ruleData["IsActive"])==1:
        rule.baseRule.IsActive=True
    else:
        rule.baseRule.IsActive=False
    print(ruleData["IsActive"])
    if ruleData["StreamIndex"]=='1':
        rule.baseRule.StreamIndex=1
    else:
        rule.baseRule.StreamIndex=0
    rule.baseRule.Name=ruleData["Name"].encode("utf-8")
    rule.baseRule.EventLevel=ruleData["EventLevel"]
    rule.baseRule.ServiceID=ruleData["ServiceID"]
    rule.baseRule.EventSourceID=ruleData["EventSourceID"]
    rule.baseRule.ConfigData=bytearray(source=ruleData["EventSourceConfig"],encoding='utf-8')
    #print(rule.baseRule)
@WCreateRuleSerClient(RuleServer)
def getServiceAndEventSource(ruleserver):
    '''
    从上层服务获取service和EventSource列表
    :param ruleserver:
    :return:
    '''
    ServiceAndEvent=ruleserver.getServiceAndEventSource()
    return ServiceAndEvent
@WCreateRuleSerClient(RuleServer)
def deleteRule(ruleID,ruleserver):
    '''
    根据规则ID 删除规则
    :param ruleID:
    :param ruleserver:
    :return:
    '''
    flag=ruleserver.DeleteRule(ruleID)
    return flag