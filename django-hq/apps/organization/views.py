# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.exceptions import *
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.utils.translation import ugettext_lazy as _
from django.db.models.query_utils import Q
from django.core.urlresolvers import reverse

from datetime import timedelta
from django.db import transaction
from djflot import dbhelper

from xformmanager.models import *
from modelrelationship.models import *
from organization.models import *

from django.contrib.auth.models import User 
from django.contrib.contenttypes.models import ContentType

#from forms import *
import logging
import hashlib
import settings
import traceback
import sys
import os
import string

@login_required()
def dashboard(request, template_name="organization/dashboard.html"):
    context = {}
    if ExtUser.objects.all().filter(id=request.user.id).count() == 0:
        template_name="organization/no_permission.html"
        return render_to_response(template_name, context, context_instance=RequestContext(request))
        
    default_delta = timedelta(days=1)
    enddate = datetime.now()
    startdate = datetime.now() - default_delta    
    
    for item in request.GET.items():
        if item[0] == 'startdate':
            startdate_str=item[1]
            startdate = datetime.strptime(startdate_str,'%m/%d/%Y')            
        if item[0] == 'enddate':
            enddate_str=item[1]
            enddate = datetime.strptime(enddate_str,'%m/%d/%Y')
            
    context['startdate'] = startdate
    context['enddate'] = enddate
    
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@login_required()
def org_report(request, template_name="organization/org_report.html"):
    context = {}
    if ExtUser.objects.all().filter(id=request.user.id).count() == 0:
        template_name="organization/no_permission.html"
        return render_to_response(template_name, context, context_instance=RequestContext(request))
    
    contenttype_id = None
    content_id = None
    default_delta = timedelta(days=1)
    enddate = datetime.now()
    startdate = datetime.now() - default_delta    
    
    for item in request.GET.items():
        if item[0] == 'content_type':
            contenttype_id=item[1]
        if item[0] == 'content_id':
            content_id=item[1]
        if item[0] == 'startdate':
            startdate_str=item[1]
            startdate = datetime.strptime(startdate_str,'%m/%d/%Y')            
        if item[0] == 'enddate':
            enddate_str=item[1]
            enddate = datetime.strptime(enddate_str,'%m/%d/%Y')                
    
    if contenttype_id != None and content_id != None:
        ctype = ContentType.objects.all().get(id=contenttype_id)
        context['selected_type'] = ctype
        content_instance = ctype.model_class().objects.all().get(id=content_id)
        context['selected_object'] =  content_instance
    else:
        context['selected_object'] = None
    
    context['startdate'] = startdate
    context['enddate'] = enddate    
    
    extuser = ExtUser.objects.all().get(id=request.user.id)        
    context['extuser'] = extuser    
    return render_to_response(template_name, context, context_instance=RequestContext(request))

@login_required()
def register_xform(request, template_name="organization/register_xform.html"):
    return ''


@login_required()
def manage_xforms(request, template_name="oranization/manage_xforms.html"):
    return''

@login_required()
def summary_trend(request, template_name="djflot/summary_trend.html"):    
    context = {}        
    
    formname = ''
    formdef_id = -1
    extuser = ExtUser.objects.all().get(id=request.user.id)
    for item in request.GET.items():
        if item[0] == 'formdef_id':
            formdef_id=item[1]    
    if formdef_id == -1:
        context['chart_title'] = 'All Data'
        context['dataset'] = {}        
        defs = FormDefData.objects.all().filter(uploaded_by__domain=extuser.domain)
    
        for fdef in defs:            
            d = dbhelper.DbHelper(fdef.element.table_name, fdef.form_display_name)            
            context['dataset'][fdef.form_display_name.__str__()] = d.get_counts_dataset(None,None)                    
    
    else:
        fdef = FormDefData.objects.all().filter(id=formdef_id)
        context['chart_title'] = fdef[0].form_display_name
        d = dbhelper.DbHelper(fdef[0].element.table_name,fdef[0].form_display_name)        
        context['dataset'] = d.get_integer_series_dataset()
    
    context ['maxdate'] = 0;
    context ['mindate'] = 0;
    return render_to_response(template_name, context, context_instance=RequestContext(request))

