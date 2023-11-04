from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def checkusername(username): # Special Character not allowed
    if username != '' and all(chr.isalnum() or chr.isspace() for chr in username):
        return True
    else:
        return False

def uniqueemail(email):  # Email Should be unique
    search_email = User.objects.filter(email=email)
    if search_email:
        return False
    else:
        return True

def checkemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def checkpassword(password):  # Password format
    if password != '' :
        return True
    else:
        return False

def validate_registration(request,username,email,password):
    if checkusername(username)==False:
        messages.warning(request, "Username should contain only alphabets")
    elif checkemail(email)==False:
        messages.warning(request, "Enter a valid email address")
    elif uniqueemail(email)==False:
        messages.warning(request, "This Email is already Registered")
    elif checkpassword(password)==False:
        messages.warning(request, "Password can't be blank")
    else:
        return 1

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        psw = request.POST.get('password')
        repeat_psw= request.POST.get('psw_repeat')
        if validate_registration(request,username,email,psw) == 1:
            if psw == repeat_psw:
                password = make_password(psw)
                obj_user = User.objects.filter(username=username)
                if obj_user:
                    error = 'Username already exists'
                    messages.warning(request, "Username already exists")
                    return render(request, "register.html", locals())
                else:
                    newuser = User.objects.create(username=username, password = password, email=email)
                    newuser.save()
                    messages.success(request, "User Register Successfully.")
                    return redirect('/login')
            else:
                messages.warning(request, "Password and Confirm Password should be same")
        return render(request, "register.html", locals())
    return render(request, "register.html", locals())

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        psw = request.POST.get('password')
        try:
            get_user_by_username =User.objects.get(username=username)
            if get_user_by_username:
                flag= check_password(psw, get_user_by_username.password)
                if flag:
                    request.session["uid"] = request.POST.get('username')
                    messages.success(request, "Login Successfully.")
                    return redirect('/index')
                error = 'Wrong password'
                messages.warning(request, "Wrong password")
                return render(request, "login.html", locals())
        except:
            error = 'Wrong username or password'
            messages.error(request, "Wrong username or password")
            return render(request, "login.html", locals())
    return render(request, "login.html", locals())

def password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        psw = request.POST.get('new_psw')
        repeat_psw = request.POST.get('psw_repeat')
        try:
            get_user = User.objects.get(username=username)
            print("get", get_user)
            if get_user:
                if psw == repeat_psw:
                    password = make_password(psw)
                    User.objects.filter(pk=get_user.id).update(password=password)
                    messages.success(request, "Password reset Successfully.")
                    return render(request, 'password_reset.html')
                else:
                    error= 'Password and Confirm Password should be same'
                    messages.warning(request, "Password and Confirm Password should be same")
                    return render(request, "password_reset.html", locals())
        except:
            messages.warning(request, "User not exists")
            return render(request, 'password_reset.html')
    return render(request, 'password_reset.html')

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
        messages.warning(request, "Invalid Date (Date Of Birth should not be greater than today)")
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
            if checkname(name)==True:
                entry=Family(
                    name = name,
                )
                entry.save()
                messages.success(request, "Family Added Successfully")
                return redirect("/family")
            else:
                messages.warning(request, "Name of a family should contain only alphabets")
                return redirect("/family")
    return redirect('/login')

def update_family(request,id):
    if request.session.has_key('uid'):
        family_id = Family.objects.get(id=id)
        name = request.POST.get('name')
        if checkname(name) == True:
            entry = Family(
                id=id,
                name=name,
            )
            entry.save()
            messages.info(request, "Family Name Updated Successfully")
            return redirect("/family")
        else:
            messages.warning(request, "Name of a family should contain only alphabets")
            return redirect("/family")
    return redirect('/login')

def delete_family(request,id):
    if request.session.has_key('uid'):
        family = Family.objects.get(id=id)
        family.delete()
        messages.success(request, "Family Deleted Successfully")
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
                    messages.success(request, "Member Added Successfully")
                except Exception as e:
                    messages.error(request,e)
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
                    messages.success(request, "Member Updated Successfully")
                except:
                    messages.error(request, "Mobile number already exists!")
                return redirect("family_details", family_id=family.id)
            return redirect("family_details", family_id=family.id)
    return redirect('/login')

def delete_family_member(request, family_id, family_member_id):
    if request.session.has_key('uid'):
        family_member = FamilyMember.objects.get(id=family_member_id)
        family_member.delete()
        messages.success(request, "Member Deleted Successfully")
        return redirect("family_details", family_id=family_id)
    return redirect('/login')

