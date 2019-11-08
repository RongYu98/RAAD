from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Account
import hashlib, requests, json

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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
    if request.method == 'GET' and request.session['active']:
        request.session.flush()
        return redirect('/')
    
    return redirect('/error/')


def blacklist_ip(request):
    if request.method == 'POST' and request.session['active']:
        body = request.body.decode('utf-8').split('&')
        data = {}
        for param in body:
            if param.startswith('ip='):
                data['ip'] = param.replace('ip=', '')
                break
        res = requests.post('http://127.0.0.1:9000/blacklist_ip', data=data).json()
        return JsonResponse(res)


def remove_blacklisted_ip(request, ip):
    if request.method == 'GET' and request.session['active']:
        res = requests.delete('http://127.0.0.1:9000/remove_blacklisted_ip', data={'ip': ip}).json()
        if res and res['status'] == 200:
            return redirect('/admin/blacklist/')

    return redirect('/error/')


def set_threshold(request):
    if request.method == 'PUT' and request.session['active']:
        body = request.body.decode('utf-8').split('&')
        data = {}
        for param in body:
            data[param.split('=')[0]] = param.split('=')[1]
        res = requests.put('http://127.0.0.1:9000/set_threshold', data=data).json()
        return JsonResponse(res)


def password(request):
    if request.method == 'PUT' and request.session['active']:
        body = request.body.decode('utf-8').split('&')
        password, confirmed_password = None, None
            
        for param in body:
            if param.startswith('password='):
                password = param[9:].strip()
            elif param.startswith('confirmed_password='):
                confirmed_password = param[19:].strip()
            
        if password and confirmed_password and password == confirmed_password:
            # update password
            change = Account.objects.get(username="root")
            # password = hashlib.sha256(password.encode()).hexdigest()
            change.password = password
            change.save()
            return JsonResponse({"status": 200})

    return JsonResponse({"status": 500})
