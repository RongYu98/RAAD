from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

def home(request):
    if request.session.has_key('active'): # session is alive
        if request.session['active'] == False: # failed to login
            return render(request, 'admin/index.html', context={'active': False})
        else: # previously logged in, but revisited
            del request.session['active']
            return render(request, 'admin/index.html', context={'active': None})
    else: #just opened website
        return render(request, 'admin/index.html', context={'active': None})

def blacklist(request):
    if request.session.has_key('active'): # session is alive
        if request.session['active']: # logged in with admin account
            # blacklists = requests.get('')
            blacklists = [{'ip':'1.1.1.1'}]
            return render(request, 'admin/admin.html', {'content_type':'blacklist', 'blacklists':blacklists})
        else: #logged in with different account
            del request.session['active']
            return redirect('/')
    else: # session is dead
        return redirect('/')

def threshold(request):
    if request.session.has_key('active'): # session is alive
        if request.session['active']: # logged in with admin account
            maxretry = 2
            findtime = 2
            bantime = 2
            return render(request, 'admin/admin.html', {'content_type':'threshold', 'maxretry': maxretry, 'findtime': findtime, 'bantime': bantime})
        else: #logged in with different account
            del request.session['active']
            return redirect('/')
    else: # session is dead
        return redirect('/')
        
def password(request):
    if request.session.has_key('active'): # session is alive
        if request.session['active']: # logged in with admin account
            return render(request, 'admin/admin.html', {'content_type':'password'})
        else: #logged in with different account
            del request.session['active']
            return redirect('/')
    else: # session is dead
        return redirect('/')
        
def error(request):
    return render(request, 'error.html', {})