import imp
from django.shortcuts import render
import psycopg2
# Create your views here.
conn = psycopg2.connect(
    host="ec2-44-199-52-133.compute-1.amazonaws.com",
    database="d3cghqvqk02ucg",
    user="fpgmhtjqlwixcj",
    port="5432",
    password="34a96669eff5909572740d2860fbfeac7bf1646f4e7994988b66a0acf7a779be")

def home(request):
    return render(request,'Dtables/home.html',{})

def create_table(request):
    data={}
    if request.method == 'POST':
        q = request.POST['query']
        data["q"]=q
    return render(request,'Dtables/create_table.html',data)

def user_login(request):
    return render(request,'Dtables/login.html',{})

def user_signup(request):
    return render(request,'Dtables/signup.html',{})