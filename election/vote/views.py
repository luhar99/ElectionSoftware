from django.shortcuts import render
import os
from shutil import copyfile

# Create your views here.
names = {"explorers":[],"challengers":[],"voyagers":[],"pioneers":[],"prefect":[]}
align = 0
voters={"explorers": {"random":0, "names":0, "test":0}, "pioneers":{}, "voyagers":{}, "challengers":{}, "prefect":{}}

path = os.path.dirname(os.path.abspath(__file__)) + "/static/image/"

def index(request):
    return render(request, 'vote/main.html', {})

def choose(request):
    house = request.GET.get("house")
    return render(request, 'vote/choose.html', {'voters': voters[house], 'house': house})

def voter(request):
    person = request.GET.get("voter")
    house = request.GET.get("house")
    voters[house][person] = 1
    return render(request, 'vote/voter.html', {'house': house, 'person': person})

def votepage(request):
    house = request.GET.get("house")
    return render(request, 'vote/vote.html', {'names': names[house], 'align': align})

def count(request):
    house = request.GET.get("house")
    name = request.GET.get("name")
    for i in names[house]:
        if i["name"] == name:
            i["count"] += 1
    return render(request, 'vote/refresh.html', {'house': house})

def results(request):
    house = request.GET.get("house")
    return render(request, 'vote/results.html', {'names': names[house]})

# Saves the files with their names in files.
def settings(request):
    if request.method == "POST":
        print(request.POST)
        house = request.POST.get("house")
        number = request.POST.get("number")
        global align
        if number == "3":
            align = 2
        else:
            align = 10

        for i in range(1,int(number)+1):
            info = {}

            name = request.POST.get("name"+str(i))
            imagepath = request.POST.get("image" + str(i))
            newpath = path + house + "image" + str(i)
            copyfile(imagepath, newpath)
            count = 0
            info["name"] = name
            info["image"] = "image/" + house + "image" + str(i)
            info["count"] = count
            info["house"] = house
            names[house].append(info)

            
    return render(request, 'vote/settings.html', {})
