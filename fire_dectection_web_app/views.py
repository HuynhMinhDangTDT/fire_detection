from django.shortcuts import render , redirect, get_object_or_404
from .models import information
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from server_smart_skylight import  server
# from real_time_fire_detection import fire_detection

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            # return redirect(request.GET.get('next'))
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.success(request, ('userID or Password is incorrect!!!!'))
            return redirect('login')
    else:
        return render (request,'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def dashboard(request):
    mess = ""
    # run_real_time_fire = fire_detection
    data = next(server())
    temperature = data["temperature"]
    humidity = data["humidity"]
    photoresistor = data["photoresistor"]
    rain = data["rain"]
    ultrasonic = data["ultrasonic"]
    message = data["message"]
    
    #bắt đầu dữ liệu ảo

    # temperature = "35"
    # humidity = "80"
    # photoresistor = "2000"
    # rain = "1"
    # ultrasonic = "37"
    # message = ""
    
    message_thoi_tiet = ""
    message_thoi_diem = ""
    
    if int(photoresistor) >= 1000 and int(rain) == 1:
        message_thoi_tiet = "Nắng"
    elif int(rain) == 0:
        message_thoi_tiet = "Mưa"
    else:
        message_thoi_tiet = "Ban đêm không mưa"
        
    if int(photoresistor) >= 1000:
        message_thoi_diem = "Ban Ngày"
    else:
        message_thoi_diem = "Ban Đêm"
    
    try:
        with open("log.txt", "r") as f:
            message = f.read()
    except:
        pass
    
    # hết dữ liệu ảo
    message_dieu_khien = ""        
    if request.method == 'POST':
        if request.POST.get("auto"):
            message_dieu_khien = "auto"
            print("che do auto")
        elif request.POST.get("manual"):
            message_dieu_khien = "manual"
            print("che do manual")
        elif request.POST.get("mo_gieng"):
            message_dieu_khien = "mo"
            print("mo gieng")
        elif request.POST.get("dong_gieng"):
            message_dieu_khien = "dong"
            print("dong gieng")
    
    try:
        with open("log_dieu_khien.txt", "w") as f:
            f.write(message_dieu_khien)
    except:
        pass
    
    

        
    # print(message == "" and int(ultrasonic) < 37)
    if message == 'lua'and int(float(ultrasonic)) > 37:
        mess = "Nhà đang có cháy"
    elif message == "" and int(float(ultrasonic)) < 37:
        mess = "Có trộm đột nhập"
    elif message == 'lua' and int(float(ultrasonic)) < 37:
        mess = "Nhà đang có cháy và có trộm đột nhập"
    elif  message == "" and int(float(ultrasonic)) > 37:
        mess = "An toàn"
    
    # return render(request, 'dashboard.html', {'temp': data})
    return render(request, 'dashboard.html', {'temp': temperature, 'hum': humidity,'mess': mess, 'message_thoi_tiet': message_thoi_tiet, 'message_thoi_diem': message_thoi_diem})
    # return render(request, 'dashboard.html', {'temp': temperature, 'hum': humidity, 'photores': photoresistor, 'rain': rain, 'ultrasonic': ultrasonic, 'mode_dieu_khien': string_mode_dieu_khien ,'mess': message})