from django.conf.urls import *
from corehq.apps.reminders.models import REMINDER_TYPE_ONE_TIME
from corehq.apps.reminders.views import (
    CreateScheduledReminderView,
    EditScheduledReminderView,
    RemindersListView,
    CreateComplexScheduledReminderView,
    KeywordsListView,
    AddStructuredKeywordView,
    EditStructuredKeywordView,
    AddNormalKeywordView,
    EditNormalKeywordView,
    BroadcastListView,
    CreateBroadcastView,
    EditBroadcastView,
    CopyBroadcastView,
)

urlpatterns = patterns('corehq.apps.reminders.views',
    url(r'^list/$', RemindersListView.as_view(), name=RemindersListView.urlname),
    url(r'^delete/(?P<handler_id>[\w-]+)/$', 'delete_reminder', name='delete_reminder'),
    url(r'^broadcasts/$', BroadcastListView.as_view(), name=BroadcastListView.urlname),
    url(r'^broadcasts/add/$', CreateBroadcastView.as_view(), name=CreateBroadcastView.urlname),
    url(r'^broadcasts/edit/(?P<broadcast_id>[\w-]+)/$', EditBroadcastView.as_view(),
        name=EditBroadcastView.urlname),
    url(r'^broadcasts/copy/(?P<broadcast_id>[\w-]+)/$', CopyBroadcastView.as_view(),
        name=CopyBroadcastView.urlname),
    url(r'^scheduled/', 'scheduled_reminders', name='scheduled_reminders'),
    url(r'^schedule/complex/$',
        CreateComplexScheduledReminderView.as_view(), name=CreateComplexScheduledReminderView.urlname),
    url(r'^schedule/(?P<handler_id>[\w-]+)/$',
        EditScheduledReminderView.as_view(), name=EditScheduledReminderView.urlname),
    url(r'^schedule/$',
        CreateScheduledReminderView.as_view(), name=CreateScheduledReminderView.urlname),
    url(r'^keywords/$', KeywordsListView.as_view(), name=KeywordsListView.urlname),
    url(r'^keywords/structured/add/$', AddStructuredKeywordView.as_view(),
        name=AddStructuredKeywordView.urlname),
    url(r'^keywords/normal/add/$', AddNormalKeywordView.as_view(),
        name=AddNormalKeywordView.urlname),
    url(r'^keywords/structured/edit/(?P<keyword_id>[\w-]+)/$',
        EditStructuredKeywordView.as_view(),
        name=EditStructuredKeywordView.urlname),
    url(r'^keywords/normal/edit/(?P<keyword_id>[\w-]+)/$',
        EditNormalKeywordView.as_view(), name=EditNormalKeywordView.urlname),
    url(r'^survey_list/$', 'survey_list', name='survey_list'),
    url(r'^add_survey/$', 'add_survey', name='add_survey'),
    url(r'^edit_survey/(?P<survey_id>[\w-]+)/$', 'add_survey', name='edit_survey'),
    url(r'^add_sample/$', 'add_sample', name='add_sample'),
    url(r'^edit_sample/(?P<sample_id>[\w-]+)/$', 'add_sample', name='edit_sample'),
    url(r'^sample_list/$', 'sample_list', name='sample_list'),
    url(r'^edit_contact/(?P<sample_id>[\w-]+)/(?P<case_id>[\w-]+)/$', 'edit_contact', name='edit_contact'),
    url(r'^reminders_in_error/$', 'reminders_in_error', name='reminders_in_error'),
    url(r'^one_time_reminders/$', 'list_reminders', name='one_time_reminders', kwargs={"reminder_type" : REMINDER_TYPE_ONE_TIME}),
    url(r'^one_time_reminders/add/$', 'add_one_time_reminder', name='add_one_time_reminder'),
    url(r'^one_time_reminders/edit/(?P<handler_id>[\w-]+)/$', 'add_one_time_reminder', name='edit_one_time_reminder'),
    url(r'^one_time_reminders/copy/(?P<handler_id>[\w-]+)/$', 'copy_one_time_reminder', name='copy_one_time_reminder'),
    url(r'^rule_progress/$', 'rule_progress', name='reminder_rule_progress'),
)
