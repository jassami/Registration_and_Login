from django.shortcuts import redirect, render
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        request.session['send']= "register"
        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            request.session['first_name'] = request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['birthday'] = request.POST['birthday']
            request.session['email'] = request.POST['email']
            return redirect('/')
        else:
            request.session['first_name']= request.POST['first_name']
            pw_hash= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            reg_user= User.objects.create(first_name= request.POST['first_name'], last_name=request.POST['last_name'], birthday= request.POST['birthday'], email= request.POST['email'], password= pw_hash)
            request.session['reg_user_id'] = reg_user.id
        return redirect('/success')
    else:
        return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        request.session['send']= "login"
        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        else:
            user= User.objects.filter(email=request.POST['email'])
            if len(user) != 1:
                return redirect('/')
            if user:
                logged_user= user[0]
                request.session['first_name'] = logged_user.first_name
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['logged_user_id']= logged_user.id
                    print(request.POST)
                    return redirect('/success')
    else:
        return redirect('/')

def success(request):
    if 'logged_user_id' not in request.session:
        return redirect('/')
    request.session['send']= "reg_success"
    try:
        user= User.objects.get(id= request.session['reg_user_id'])
        print(user.first_name)
        messages.success(request, "Successfully registered!")
        return render(request, 'success.html')
    except:
        user= User.objects.get(id= request.session['logged_user_id'])
        print(user.first_name)
        messages.success(request, "Successfully logged in!")
        return render(request, 'success.html')

def logout(request):
    request.session.clear()
    return redirect('/')
