from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.session.has_key('alive'): #failed to login
        if request.session['alive']:
            return redirect('/admin/')
        else:
            del request.session['alive']
            return render(request, 'admin/index.html', context={'alive': False})
    else: #just opened website
        return render(request, 'admin/index.html', context={'alive': None})
        
def admin(request):
    if request.session.has_key('alive'): #somehow logged in
        if request.session['alive']: #logged in with admin account
            return render(request, 'admin/admin.html', {})
        else: #logged in with different account
            del request.session['alive']
            return render(request, 'error.html', {})
            
    else:
        return redirect('/')
        
    