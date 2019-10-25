from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account
import hashlib

def login(request):
    if request.method == 'POST':
        body = str(request.body, 'utf-8').split('&')
        username, password = None, None
        
        for param in body:
            if 'username=' in param:
                username = param[9:]
            elif 'password=' in param:
                password = param[9:]
                password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            if Account.objects.get(username=username, password=password):
                request.session['alive'] = True
                return redirect('/admin/')
        except Account.DoesNotExist:
            request.session['alive'] = False
            return redirect('/')
    
    return render(request, 'error.html', {})

def logout(request):
    if request.method == 'GET':
        if request.session['alive']:
            del request.session['alive']
            return redirect('/')
    
    return render(request, 'error.html', {})