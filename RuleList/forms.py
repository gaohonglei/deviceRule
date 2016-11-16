#!/usr/bin/env python
# coding=utf-8
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
class RuleForm(forms.Form):
    Name=forms.CharField(label="规则名称",required=True,max_length=50)
    StreamIndex=forms.ChoiceField(label="分析码流",choices=[(0,"主码流"),(1,"辅码流")])
    EventLevel=forms.ChoiceField(label="事件等级",choices=[(0,0),(1,1),(2,2),(3,3)])
    IsActive=forms.ChoiceField(label="是否激活",required=True,choices=[(0,"不激活"),(1,"激活")],widget=forms.RadioSelect)
    ServiceID=forms.ChoiceField(label="隶属服务")
    EventSourceID=forms.ChoiceField(label="分析算法")
    EventSourceConfig=forms.CharField(label="配置文件",required=False,widget=forms.Textarea)
class RuleAdd(forms.Form):
    Name=forms.CharField(label="规则名称",required=True,max_length=50,error_messages={"required":"规则名称不能为空"})
    StreamIndex = forms.ChoiceField(label="分析码流", choices=[(0, "主码流"), (1, "辅码流")])
    EventLevel=forms.ChoiceField(label="事件等级",choices=[(0,0),(1,1),(2,2),(3,3)])
    IsActive=forms.ChoiceField(label="是否激活",required=True,choices=[(0,"不激活"),(1,"激活")],widget=forms.RadioSelect)
    ServiceID=forms.ChoiceField(label="隶属服务")
    EventSourceID=forms.ChoiceField(label="分析算法")
    EventSourceConfig = forms.CharField(label="配置文件", required=False,widget=forms.Textarea)
    def __init__(self,*args,**kwargs):
        super(RuleAdd,self).__init__(*args)
        self.fields["ServiceID"].choices=kwargs["ServiceChoices"]
        self.fields["EventSourceID"].choices=kwargs["EventSourceChoices"]
    # def clean(self):
    #     raise forms.ValidationError("Please input correct username")
    #     print(1)