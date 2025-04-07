from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def events(request):
    return render(request, 'main/events.html')

def resources(request):
    return render(request, 'main/resources.html')

def team(request):
    return render(request, 'main/team.html')

def advertise(request):
    return render(request, 'main/advertise.html')

def opportunities(request):
    return render(request, 'main/opportunities.html')

def contact(request):
    return render(request, 'main/contact.html')
