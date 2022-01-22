import imp
from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
import psycopg2
# Create your views here.

conn = psycopg2.connect(
                host="ec2-34-194-171-47.compute-1.amazonaws.com",
                database="ddffht99no2b23",
                user="uxihixqyaetpsc",
                port="5432",
                password="0c9e94b7c928423a19bc8d4fd5de1133e2cb424c82bd5f7c2365c93419b0ddcd")

def home(request):
    user = request.user
    if user.is_authenticated:
        data={}
        try:
            cur = conn.cursor()
            cur.execute("SELECT table_name FROM alltables Where username = 'NA';")
            data["alltables"]= [x[0] for x in cur.fetchall()]
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            data["error"]=str(error)
            conn.rollback()
        return render(request,'Dtables/home.html',data)
    else:
        return render(request,'Dtables/index.html',{})


def create_table(request):
    data={}
    no_col=1
    if request.method == 'POST':
        if 'no_col' in request.POST:
            no_col=int(request.POST['no_col'])
            if no_col<1:
                no_col=1
        elif 'create' in request.POST:
            table=request.POST
            cq = "CREATE TABLE "+ request.POST["table_name"] + " ( "
            for i in range(1,100):
                k=str(i)
                if "n"+k in table:
                    cq+=table["n"+k] + " "
                    if table["d"+k]=="String" or table["d"+k]=="Email":
                        cq+="TEXT "
                    elif table["d"+k]=="Number":
                        cq+="INT "
                    elif table["d"+k]=="Boolean":
                        cq+="BOOLEAN "
                    elif table["d"+k]=="Datetime":
                        cq+="Date "
                    if table['primary']==k:
                        cq+="PRIMARY KEY "
                    cq+=", "
            cq=cq[:-2]+");"

            try:
                cur = conn.cursor()
                cur.execute(cq)
                cur.execute("INSERT INTO alltables (table_name, username) VALUES ('"+request.POST["table_name"].lower()+"', 'NA');")
                cur.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '"+request.POST["table_name"].lower()+"';")
                data["data"]= cur.fetchall()
                data["data_tablename"]=request.POST["table_name"].lower().title()
                cur.close()
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                data["error"]=str(error).replace("relation","Table").title()
                conn.rollback()

    data["range_col"]=range(1,no_col+1)
    data["no_col"]=no_col
    return render(request,'Dtables/create_table.html',data)

def delete_table(request):
    data={}
    try:
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM alltables Where username = 'NA';")
        tables=[x[0] for x in cur.fetchall()]
        data['tables']=tables
        if request.method == 'POST':
            if request.POST["table_name"].lower() in tables:
                cur.execute("DROP TABLE "+request.POST["table_name"].lower()+";")
                cur.execute("DELETE FROM alltables Where table_name = '"+request.POST["table_name"].lower()+"';")
                data["message"]='Table "'+request.POST["table_name"].lower().title()+'" Successfully Deleted'
            else:
                data["error"]='Table "'+request.POST["table_name"].lower().title()+'" Does Not Exist'
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        data["error"]=str(error).title()
        conn.rollback()
    return render(request,'Dtables/delete_table.html',data)

def user_logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)