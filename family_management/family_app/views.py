from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_list= User.objects.filter(username= username)

        if user_list:
            error_name='The user name already exists'
            return render (request, 'register.html',{'error_name': error_name})
        else:
            newuser=User.objects.create(username=username, password=password,email=email)
            newuser.save()
        return redirect('/login')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        obj_user = User.objects.filter(username=username, password=password)
        if obj_user:
            request.session["uid"]=request.POST.get('username')
            messages.success(request, "Login Successfully.")
            return redirect('/index')
        error = 'Wrong username or password'

    return render(request, "login.html", locals())

def index(request):
    if request.session.has_key('uid'):
        user_name = (request.session["uid"]).capitalize()
        total_family= Family.objects.count()
        total_members= FamilyMember.objects.count()
        return render(request, "index.html", locals())
    else:
        return redirect('/login')

def logout(request):
    try:
        del request.session["uid"]
    except KeyError:
        pass
    return redirect("/login")

def family(request):
    if request.session.has_key('uid'):
        user_name = (request.session["uid"]).capitalize()
        family_list = Family.objects.all()
        return render(request, 'family.html', locals())
    else:
        return redirect('/login')

def add_family(request):
    if request.session.has_key('uid'):
        if request.method=='POST':
            name=request.POST.get('name')
            entry=Family(
                name = name,
            )
            entry.save()
            return redirect("/family")
    return redirect('/login')

def delete_family(request,id):
    if request.session.has_key('uid'):
        family = Family.objects.get(id=id)
        family.delete()
        return redirect("/family")
    return redirect('/login')

def family_details(request, family_id):
    if request.session.has_key('uid'):
        if request.session.has_key('uid'):
            user_name = (request.session["uid"]).capitalize()
            family = Family.objects.get(id=family_id)
            family_members = FamilyMember.objects.filter(family=family.id)
            age_data = [(person, person.calculate_age()) for person in family_members]
            return render(request, 'family_details.html', {'family': family, 'family_members': family_members, 'user_name' :user_name, 'age_data' : age_data })
    return redirect('/login')

def add_family_member(request, family_id):
    if request.session.has_key('uid'):
        if request.method == 'POST':
            family = Family.objects.get(id=family_id)
            name = request.POST.get('name')
            date_of_birth = request.POST.get('date_of_birth')
            gender = request.POST.get('gender')
            mobile_number = request.POST.get('mobile_number')
            entry = FamilyMember(
                family= family,
                name=name,
                date_of_birth= date_of_birth,
                gender=gender,
                mobile_number= mobile_number
            )
            try:
                entry.save()
            except:
                messages.warning(request,"Duplicate Phone Number")
            return redirect("family_details", family_id=family.id)
    return redirect('/login')

def update_family_member(request, family_id, family_member_id):
    if request.session.has_key('uid'):
        family = Family.objects.get(id=family_id)
        family_member = FamilyMember.objects.get(id=family_member_id)
        if request.method == 'POST':
            name = request.POST.get('name')
            date_of_birth = request.POST.get('date_of_birth')
            gender = request.POST.get('gender')
            mobile_number = request.POST.get('mobile_number')
            entry = FamilyMember(
                id= family_member.id,
                family=family,
                name=name,
                date_of_birth=date_of_birth,
                gender=gender,
                mobile_number=mobile_number
            )
            try:
                entry.save()
            except:
                messages.warning(request, "Duplicate Phone Number")
            return redirect("family_details", family_id=family.id)
    return redirect('/login')

def delete_family_member(request, family_id, family_member_id):
    if request.session.has_key('uid'):
        family_member = FamilyMember.objects.get(id=family_member_id)
        family_member.delete()
        return redirect("family_details", family_id=family_id)
    return redirect('/login')

