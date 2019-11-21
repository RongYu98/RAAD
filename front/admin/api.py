from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import hashlib, requests, json, hmac, base64

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # get current salt
        res = requests.get('http://127.0.0.1:9000/get_current_salt').json()
        if res and res['status'] == 200:
            salt = res['detail']
            password = hmac.new(salt.encode(), password.encode(), hashlib.sha256)
            password = password.hexdigest()
            # check password
            data = {"password": password, "username": username}
            res = requests.post('http://127.0.0.1:9000/check_password', data=data).json()
            if res and res['status'] == 200:
                request.session['active'] = True
                return redirect('/admin/blacklist/')
            else:
                request.session['active'] = False
                return redirect('/')    
        else:
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
            # get random salt
            res = requests.get('http://127.0.0.1:9000/get_random_salt').json()
            if res and res['status'] == 200:
                salt = res['detail']
                password = hmac.new(salt.encode(), password.encode(), hashlib.sha256)
                password = password.hexdigest()
                # update password
                data = {"password": password, "username": "root"}
                res = requests.post('http://127.0.0.1:9000/set_password', data=data).json()
                return JsonResponse({"status": res['status']})
            
    return JsonResponse({"status": 500})
