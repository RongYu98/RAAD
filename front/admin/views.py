from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

def home(request):
    if request.session.has_key('active'): # session is alive
        if request.session['active'] == False: # failed to login
            del request.session['active']
            return render(request, 'admin/index.html', context={'active': False, 'alert_msg': 'Unsuccessful Login'})
        else: # previously logged in, but revisited
            del request.session['active']
            return render(request, 'admin/index.html', context={'active': None})
    else: #just opened website
        return render(request, 'admin/index.html', context={'active': None})

def blacklist(request):
    if request.session.has_key('active'): # session is alive
        if request.session['active']: # logged in with admin account
            try:
                res = requests.get('https://127.0.0.1:9000/blacklisted_ips', verify=False).json()
                if res and res['status'] == 200:
                    blacklists = res['detail']
                return render(request, 'admin/admin.html', {'content_type':'blacklist', 'blacklists':blacklists})
            except Exception:
                return render(request, 'admin/admin.html', {'content_type':'blacklist', 'blacklists':[]})
        else: #logged in with different account
            del request.session['active']
            return redirect('/')
    else: # session is dead
        return redirect('/')

def threshold(request):
    if request.session.has_key('active'): # session is alive
        if request.session['active']: # logged in with admin account
            try:
                res = requests.get('https://127.0.0.1:9000/get_threshold', verify=False).json()
                if res and res['status'] == 200:
                    maxretry,findtime, bantime = res['detail']['maxretry'], res['detail']['findtime'], res['detail']['bantime']
                else:
                    maxretry, findtime, bantime = 3, 1, 3600 # default
            except Exception:
                maxretry, findtime, bantime = 0, 0, 0
            finally:
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
        
def error(request, exception=None):
    return render(request, 'error.html', {})