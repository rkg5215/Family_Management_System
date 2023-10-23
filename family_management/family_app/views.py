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
            messages.success(request, "User Registered Successfully.")
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

def checkname(name):
    if name != '' and all(chr.isalpha() or chr.isspace() for chr in name):
        return True
    else:
        return False

def checkphone(phone):
    if phone != "" and phone.isdigit() and len(phone) == 10:
        return True
    else:
        return False

def checkgender(gender):
    if gender == "Male" or gender == "Female" :
        return True
    else:
        return False

def checkdate(Enter_date):
    from datetime import date
    today = date.today()
    if str(today) < Enter_date:
        return False
    else:
        return True

def validation_all(request,name,Enter_date,phone,gender):
    if checkname(name)==False:
        messages.warning(request, "Name of a person should contain only alphabets")
    elif checkdate(Enter_date)==False:
        messages.warning(request, "Date Of Birth should not be greater than today")
    elif checkphone(phone)==False:
        messages.warning(request, "Phone number should be digit and not greater than 10")
    elif checkgender(gender)==False:
        messages.warning(request, "Gender should be male or female only")

    else:
        return 1

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

def update_family(request,id):
    if request.session.has_key('uid'):
        family_id = Family.objects.get(id=id)
        name = request.POST.get('name')
        entry = Family(
            id=id,
            name=name,
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
            if validation_all(request, name, date_of_birth, mobile_number, gender) == 1:
                entry = FamilyMember(
                    family= family,
                    name=name,
                    date_of_birth= date_of_birth,
                    gender=gender,
                    mobile_number= mobile_number
                )
                try:
                    entry.save()
                except Exception as e:
                    messages.warning(request,e)
                return redirect("family_details", family_id=family.id)
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
            if validation_all(request,name,date_of_birth,mobile_number,gender)==1:
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
                    messages.warning(request, "Mobile number already exists!")
                return redirect("family_details", family_id=family.id)
            return redirect("family_details", family_id=family.id)
    return redirect('/login')

def delete_family_member(request, family_id, family_member_id):
    if request.session.has_key('uid'):
        family_member = FamilyMember.objects.get(id=family_member_id)
        family_member.delete()
        return redirect("family_details", family_id=family_id)
    return redirect('/login')

