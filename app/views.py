# -*- coding: utf-8 -*-  
import os, re, json, random, pdb
from django import forms
from django.template import Context, Template
from django.template.loader import get_template  
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

from django.contrib.auth.decorators import login_required  
from django.views.decorators.csrf import csrf_exempt
from datasettings.presets import presets

@login_required(login_url="/adminlogin/")
def index(request):
    return render_to_response('index.html')

@csrf_exempt
def get_presets (request):
	user = request.user
	navlist = {
		'code': 200,
		'presets': presets,
	}
	return HttpResponse(
		json.dumps(navlist)
	)