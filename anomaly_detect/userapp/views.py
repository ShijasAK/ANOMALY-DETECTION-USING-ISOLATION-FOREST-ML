import csv

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

from .function import Anomally
from .models import Anomally_Detect

mpl.rcParams['figure.figsize'] = (10 , 8)
mpl.rcParams['axes.grid'] = False
from .forms import UserRegisterForm
import warnings
from django.contrib import messages, auth
from django.contrib.auth import logout

warnings.filterwarnings('ignore')


def register(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        obj=form.save()
        auth.login(request, obj)
        username = form.cleaned_data.get('username')
        messages.success(request, f'Account created for {username}!')
        return redirect('home')
    return render(request,'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
import os
from django.core.files import File

def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            dataset = request.FILES['datset']
            obj = Anomally(dataset,title,request)
            return render(request,'result.html',{'obj':obj})
            # return render(request,'home.html',params
    else:
        return redirect('login')
    return render(request, 'home.html')

def result(request,id):
    if request.user.is_authenticated:
        obj = Anomally_Detect.objects.get(id=id)
        return render(request,'result.html',{'obj':obj})
    return redirect('login')

def dwn_final(request,id):
    if request.user.is_authenticated:
        obj = Anomally_Detect.objects.get(id=id)
        filename = obj.final.path
        data = open(filename, 'r').read()
        resp = HttpResponse(data)
        resp['Content-Disposition'] = 'attachment;filename=final.csv'
        return resp
    return redirect('login')

def dwn_out(request,id):
    if request.user.is_authenticated:
        obj = Anomally_Detect.objects.get(id=id)
        filename = obj.outliers.path
        data = open(filename, 'r').read()
        resp = HttpResponse(data)
        resp['Content-Disposition'] = 'attachment;filename=outlier.csv'
        return resp
    return redirect('login')


def total_result(request):
    if request.user.is_authenticated:
        user_obj = User.objects.get(username=request.user)
        obj = Anomally_Detect.objects.filter(user=user_obj)
        return render(request, 'com_result.html',{'obj':obj})
    return redirect('login')

def detail(request,id):
    if request.user.is_authenticated:
        obj = Anomally_Detect.objects.get(id=id)
        return render(request,'result.html',{'obj':obj})
    return redirect('login')

# def final_csv(request):
#     data = open('userapp/static/final/Users.csv','r').read()
#     resp = HttpResponse(data)
#     resp['Content-Disposition'] = 'attachment;filename=table.csv'
#     return resp
#
# def anomally_csv(request):
#     data = open('userapp/static/final/anomally.csv','r').read()
#     resp = HttpResponse(data)
#     resp['Content-Disposition'] = 'attachment;filename=table.csv'
#     return resp
from pathlib import Path
from django.core.files import File
from PIL import Image
