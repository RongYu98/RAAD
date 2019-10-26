from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account
import hashlib

def signin(request):
    if request.method == 'POST':
        body = str(request.body, 'utf-8').split('&')
        username, password = None, None
        
        for param in body:
            if 'username=' in param:
                username = param[9:].strip()
            elif 'password=' in param:
                password = param[9:].strip()
                password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            if Account.objects.get(username=username, password=password):
                request.session['active'] = True
                return redirect('/admin/blacklist/')
        except Account.DoesNotExist:
            request.session['active'] = False
            return redirect('/')
    
    return redirect('/error/')

def signout(request):
    if request.method == 'GET':
        if request.session['active']:
            del request.session['active']
            return redirect('/')
    
    return redirect('/error/')

def password(request):
    if request.method == 'PUT':
        if request.session['active']:
            body = str(request.body, 'utf-8').split('&')
            password, confirmed_password = None, None
            
            for param in body:
                if 'password=' in param:
                    password = param[9:].strip()
                elif 'confirmed_password=' in param:
                    confirmed_password = param[19:].strip()
            
            if password and confirmed_password and password == confirmed_password:
                # api request
                return redirect('/admin/password')

    return redirect('/error/')