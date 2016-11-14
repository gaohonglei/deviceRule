#!/usr/bin/env python
# coding=utf-8
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': ''}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

class RuleForm(forms.Form):
    Name=forms.CharField(label="规则名称",max_length=50)
    EventLevel=forms.ChoiceField(label="事件等级",choices=[(0,0),(1,1),(2,2),(3,3),(4,4)])
    IsActive=forms.ChoiceField(label="是否激活",required=True,choices=[(0,"不激活"),(1,"激活")],widget=forms.RadioSelect)
    ServiceID=forms.ChoiceField(label="隶属服务")
    StreamIndex=forms.ChoiceField(label="分析码流",choices=[(0,"主码流"),(1,"辅码流")])
    EventSourceID=forms.ChoiceField(label="分析算法")
    EventSourceConfig=forms.CharField(label="配置文件",widget=forms.Textarea)
class RuleAdd(forms.Form):
    Name=forms.CharField(label="规则名称",max_length=50)
    StreamIndex = forms.ChoiceField(label="分析码流", choices=[(0, "主码流"), (1, "辅码流")])
    EventLevel=forms.ChoiceField(label="事件等级",choices=[(0,0),(1,1),(2,2),(3,3),(4,4)])
    IsActive=forms.ChoiceField(label="是否激活",required=True,choices=[(0,"不激活"),(1,"激活")],widget=forms.RadioSelect)
    ServiceID=forms.ChoiceField(label="隶属服务")
    EventSourceID=forms.ChoiceField(label="分析算法")
    EventSourceConfig = forms.CharField(label="配置文件", widget=forms.Textarea)