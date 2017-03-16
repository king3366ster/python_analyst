# -*- coding: utf-8 -*-
import os, re, json, random, pdb
from django import forms
from django.template import Context, Template
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.auth.models import User, Group, Permission

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datasettings.presets import presets
from datasettings.settings import setting_config

def check_perm (user, presets):
    user_obj = User.objects.get(username = user)
    if user_obj.is_superuser:
        return presets
    preset_new = []
    for item in presets:
        if 'perm' not in item:
            preset_new.append(item)
        else:
            perms = item['perm']
            for perm in perms:
                perm = perm.strip()
                if user_obj.has_perm('app.perm_%s' % perm):
                    preset_new.append(item)
                    break
    return preset_new

@login_required(login_url="/adminlogin/")
def index(request):
    return render_to_response('index.html')

@csrf_exempt
def get_presets (request):
    user = request.user
    navlist = {
        'code': 200,
        'presets': check_perm(user, presets)
    }
    return HttpResponse(
        json.dumps(navlist)
    )

@csrf_exempt
def get_loadfiles (request):
    user = request.user
    if 'loadpath' in setting_config:
        loadpath = setting_config['loadpath']
