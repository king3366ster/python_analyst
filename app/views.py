# -*- coding: utf-8 -*-  
import os, re, json, random, pdb
from django import forms
from django.template import Context, Template
from django.template.loader import get_template  
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

from django.contrib.auth.decorators import login_required  
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render_to_response('index.html')
