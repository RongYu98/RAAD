from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import hashlib, requests, json, hmac, base64, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def signin(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8').split('&')
        username, password = '', ''
        for param in body:
            if param.startswith('username='):
                username = param.replace('username=', '')
            elif param.startswith('password='):
                password = param.replace('password=', '')
                                
        # get current salt
        res = requests.get('https://127.0.0.1:9000/get_current_salt', verify=False).json()
        if res and res['status'] == 200:
            salt = res['detail']
            password = hmac.new(salt.encode(), password.encode(), hashlib.sha256)
            password = password.hexdigest()
            # check password
            data = {"password": password, "username": username}
            res = requests.post('https://127.0.0.1:9000/check_password', data=data, verify=False).json()
            if res and res['status'] == 200:
                request.session['active'] = True
                return JsonResponse({"status": 200})
                # return redirect('/admin/blacklist/')
            else:
                request.session['active'] = False
                # return redirect('/admin/')    
        else:
            request.session['active'] = False
            # return redirect('/admin/')
            
    # return redirect('/error/')
    return JsonResponse({"status": 500})


def signout(request):
    if request.method == 'GET' and request.session['active']:
        request.session.flush()
        return redirect('/admin/')
    
    return redirect('/error/')


def blacklist_ip(request):
    if request.method == 'POST' and request.session['active']:
        body = request.body.decode('utf-8').split('&')
        data = {}
        for param in body:
            if param.startswith('ip='):
                data['ip'] = param.replace('ip=', '')
                break
        res = requests.post('https://127.0.0.1:9000/blacklist_ip', data=data, verify=False).json()
        return JsonResponse(res)


def remove_blacklisted_ip(request, ip):
    if request.method == 'GET' and request.session['active']:
        res = requests.delete('https://127.0.0.1:9000/remove_blacklisted_ip', data={'ip': ip}, verify=False).json()
        if res and res['status'] == 200:
            return redirect('/admin/blacklist/')

    return redirect('/error/')


def set_threshold(request):
    if request.method == 'PUT' and request.session['active']:
        body = request.body.decode('utf-8').split('&')
        data = {}
        for param in body:
            data[param.split('=')[0]] = param.split('=')[1]
        res = requests.put('https://127.0.0.1:9000/set_threshold', data=data, verify=False).json()
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
            res = requests.get('https://127.0.0.1:9000/get_random_salt', verify=False).json()
            if res and res['status'] == 200:
                salt = res['detail']
                password = hmac.new(salt.encode(), password.encode(), hashlib.sha256)
                password = password.hexdigest()
                # update password
                data = {"password": password, "username": "root"}
                res = requests.post('https://127.0.0.1:9000/set_password', data=data, verify=False).json()
                return JsonResponse({"status": res['status']})
            
    return JsonResponse({"status": 500})
