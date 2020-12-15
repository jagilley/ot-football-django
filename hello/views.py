from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import requests
from .models import Greeting, User
from .forms import NameForm
import random

# Create your views here.
def index(request):
    #r = requests.get('http://httpbin.org/status/418')
    #template = loader.get_template('templates/base.html')
    return render(request, "templates/base.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

def register(request):
    return render(request, "register.html")

def process_reg(request):
    print(request)
    return render(request, "register.html")

def grid(request):
    print("test!!")
    my_user = User(name="Jasper Gilley", email="myemail@gmail.com")
    my_name = my_user.name
    scores = [round(random.uniform(0,20),2) for i in range(8)]
    total = round(sum(scores),2)
    return render(request, "grid.html", {"scores": scores, "total": total, "name": my_name})

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            name = form.cleaned_data['your_name']
            new_user = User(name=name, email=f"{name}@demoemail.com", wins=0, losses=0)
            new_user.save()
            print(new_user.name, new_user.email)
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})