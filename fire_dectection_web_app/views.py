from django.shortcuts import render
from server_smart_skylight import  server

def dashboard(request):
    # Temperature = 'a'
    data = next(server())
    temperature = data["temperature"]
    message = data["message"]
    # print(data["temperature"])
    # print(data["message"])
    # for item in server():
    #     print(item)
    # print(next(server())[0])
    # print(next(server())[1])
    if message == 'lua':
        message = "Nhà đang có cháy"
    else:
        message = "An toàn"
    
    # return render(request, 'dashboard.html', {'temp': data})
    return render(request, 'dashboard.html', {'temp': temperature, 'mess': message})