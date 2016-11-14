from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.GetAllDevice,name='getkey'),
    #url(r'(?P<deviceID>\w+)/(?P<channelID>\w+)/$',views.GetDeviceRuleChannel,name='getRuleByID'),
    url(r'rule/(?P<ruleID>(.+))/$',views.GetRuleByRuleID,name='getRuleByRuleID'),
    url(r'addRule/(?P<deviceID>(.+))/(?P<channelID>(.+))/$',views.AddRuleByDeviceID,name='AddRuleByDeviceID'),
    url(r'deleteRule/(?P<ruleID>(.+))/$',views.deleteRuleByRuleID,name='DeleteRuleByDeviceID'),
    ]