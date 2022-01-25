import imp
from xmlrpc.client import boolean
from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out
from django.conf import settings
from django.http import HttpResponseRedirect, request
from urllib.parse import urlencode
from datetime import datetime
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
            cur.execute("SELECT table_name FROM alltables Where username = '"+request.user.username+"';")
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
                time = str(datetime.now())
                logs = "Table - "+request.POST["table_name"].lower() + " created"
                cur.execute("INSERT INTO alltables (table_name, username) VALUES ('"+request.POST["table_name"].lower()+"', '"+request.user.username+"');")
                cur.execute("INSERT INTO auditlogs (username, logs, time) VALUES ('"+request.user.username+"','"+logs+"','"+time+"');")
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
        cur.execute("SELECT table_name FROM alltables Where username = '"+request.user.username+"';")
        tables=[x[0] for x in cur.fetchall()]
        data['tables']=tables
        if request.method == 'POST':
            if request.POST["table_name"].lower() in tables:
                time = str(datetime.now())
                logs = "Table - "+request.POST["table_name"].lower() + " deleted"
                cur.execute("DROP TABLE "+request.POST["table_name"].lower()+";")
                cur.execute("DELETE FROM alltables Where table_name = '"+request.POST["table_name"].lower()+"';")
                cur.execute("INSERT INTO auditlogs (username, logs, time) VALUES ('"+request.user.username+"','"+logs+"','"+time+"');")
                data["message"]='Table "'+request.POST["table_name"].lower().title()+'" Successfully Deleted'
                cur.execute("SELECT table_name FROM alltables Where username = '"+request.user.username+"';")
                tables=[x[0] for x in cur.fetchall()]
                data['tables']=tables
            else:
                data["error"]='Table "'+request.POST["table_name"].lower().title()+'" Does Not Exist'
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        data["error"]=str(error).title()
        conn.rollback()
    return render(request,'Dtables/delete_table.html',data)


def insert_data(request):
    data={}
    try:
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM alltables Where username = '"+request.user.username+"';")
        tables=[x[0] for x in cur.fetchall()]
        data['tables']=tables
        if request.method == 'POST':
            if request.POST["table_name"].lower() in tables:
                if 'insert' in request.POST:
                    fdata=dict(request.POST)
                    fdata.pop('csrfmiddlewaretoken')
                    fdata.pop('insert')
                    
                    iq="INSERT INTO "+fdata['table_name'][0]+" VALUES ("
                    fdata.pop('table_name')
                    desc=[]
                    values=[]
                    for c,v in fdata.items():
                        desc.append(c.split("%")[1])
                        values.append(v[0])
                    v=[]
                    for i in range(len(values)):
                        t=""
                        if not (desc[i]=="boolean" or desc[i]=="integer"):
                            t+="'"
                        t+=values[i]
                        if not (desc[i]=="boolean" or desc[i]=="integer"):
                            t+="'"
                        v.append(t)
                    iq+=", ".join(v)
                    iq+=");"
                    cur.execute(iq)
                    data["message"]= "Record Inserted Successfully"
                    time = str(datetime.now())
                    logs = "Data inserted into Table - "+request.POST["table_name"].lower()
                    cur.execute("INSERT INTO auditlogs (username, logs, time) VALUES ('"+request.user.username+"','"+logs+"','"+time+"');")
                cur.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '"+request.POST["table_name"].lower()+"';")
                struct={}
                for x in cur.fetchall():
                    struct[x[0]]=x[1]
                data["struct"]=struct
                cur.execute(
    "SELECT c.column_name FROM information_schema.key_column_usage AS c LEFT JOIN information_schema.table_constraints AS t ON t.constraint_name = c.constraint_name WHERE t.table_name = '"+request.POST["table_name"].lower()+"' AND t.constraint_type = 'PRIMARY KEY';")
                data["primary"]=cur.fetchall()[0][0]
                cur.execute("SELECT * FROM "+request.POST["table_name"].lower()+";")
                data["data"]= cur.fetchall()
                data["table_name"]=request.POST["table_name"].lower()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        data["error"]=str(error).title()
        conn.rollback()
    return render(request,'Dtables/insert_data.html',data)

def delete_data(request):
    data={}
    try:
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM alltables Where username = '"+request.user.username+"';")
        tables=[x[0] for x in cur.fetchall()]
        data['tables']=tables
        if request.method == 'POST':
            if request.POST["table_name"].lower() in tables: 
                cur.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '"+request.POST["table_name"].lower()+"';")
                struct={}
                for x in cur.fetchall():
                    struct[x[0]]=x[1]
                data["struct"]=struct
                cur.execute(
    "SELECT c.column_name FROM information_schema.key_column_usage AS c LEFT JOIN information_schema.table_constraints AS t ON t.constraint_name = c.constraint_name WHERE t.table_name = '"+request.POST["table_name"].lower()+"' AND t.constraint_type = 'PRIMARY KEY';")
                data["primary"]=cur.fetchall()[0][0]
                cur.execute("SELECT * FROM "+request.POST["table_name"].lower()+";")
                td=[zip(struct.keys(),x) for x in cur.fetchall()]
                data["data"]=zip(td,range(len(td)))
                data["table_name"]=request.POST["table_name"].lower()
                if "delete" in request.POST:
                    dq="DELETE FROM "+data["table_name"]+" WHERE "
                    for d,i in data["data"]:
                        if i == int(request.POST["delete"]):
                            for n,v in d:
                                if n == data["primary"]:
                                    dq+=n+"="
                                    if type(v) == int:
                                        dq+=str(v)
                                    else:
                                        dq+="'"+v+"'"
                    dq+=";"
                    cur.execute(dq)
                    data["message"]="Record Deleted Successfully"
                    time = str(datetime.now())
                    logs = "Data deleted from Table - "+request.POST["table_name"].lower()
                    cur.execute("INSERT INTO auditlogs (username, logs, time) VALUES ('"+request.user.username+"','"+logs+"','"+time+"');")
                    cur.execute("SELECT * FROM "+request.POST["table_name"].lower()+";")
                    td=[zip(struct.keys(),x) for x in cur.fetchall()]
                    data["data"]=zip(td,range(len(td)))
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        data["error"]=str(error).title()
        conn.rollback()
    return render(request,'Dtables/delete_data.html',data)

def view_table(request,table_name):
    data={}
    try:
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM alltables Where username = '"+request.user.username+"';")
        tables=[x[0] for x in cur.fetchall()]
        data['tables']=tables
        if not table_name.lower() in tables:
            return redirect('/')
        cur.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '"+table_name.lower()+"';")
        struct={}
        for x in cur.fetchall():
            struct[x[0]]=x[1]
        data["struct"]=struct
        cur.execute(
"SELECT c.column_name FROM information_schema.key_column_usage AS c LEFT JOIN information_schema.table_constraints AS t ON t.constraint_name = c.constraint_name WHERE t.table_name = '"+table_name.lower()+"' AND t.constraint_type = 'PRIMARY KEY';")
        data["primary"]=cur.fetchall()[0][0]
        cur.execute("SELECT * FROM "+table_name.lower()+";")
        data["data"]= cur.fetchall()
        data["table_name"]=table_name.lower()
        if request.method == 'POST':
            data["col"],data["col_type"]=request.POST["column_name"].split("%")
            if 'filter_data' in request.POST:
                fq="SELECT * FROM "+table_name.lower()+" WHERE "+data["col"]+" "
                valid_q= True
                fl= request.POST["filter"]
                if "NULL" in fl: fq+=fl
                elif data["col_type"]=="boolean":
                    if fl == "FALSE": fq=fq.replace("WHERE", "WHERE NOT")
                elif "LIKE" in fl:
                    if request.POST["value"]:
                        if "s" in fl: fl=fl[:-1]+"'"+request.POST["value"]+"%'"
                        elif "e" in fl: fl=fl[:-1]+"'%"+request.POST["value"]+"'"
                        elif "c" in fl: fl=fl[:-1]+"'%"+request.POST["value"]+"%'"
                        fq+=fl
                    else:
                        data["error"] = "Value Is Required For This Filter"
                        valid_q = False

                else:
                    if request.POST["value"]:
                        fq+=fl+" "
                        if data["col_type"] == "integer":
                            fq+=request.POST["value"]
                        else:
                            fq+="'"+request.POST["value"]+"'"
                    else:
                        data["error"] = "Value Is Required For This Filter"
                        valid_q = False
                if valid_q:
                     cur.execute(fq)
                     data["data"]=cur.fetchall()
            elif "refresh" in request.POST:
                cur.execute("SELECT * FROM "+table_name.lower()+";")
                data["data"]= cur.fetchall()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        data["error"]=str(error).title()
        conn.rollback()
    return render(request,'Dtables/view_table.html',data)

def audit_logs(request):
    data = {}
    try:
        cur = conn.cursor()
        cur.execute("SELECT logs, time FROM auditlogs where username ='"+request.user.username+ "'")
        data["data"] = cur.fetchall()
        cur.close()
        conn.commit()
    except:
        data["error"] = "No Audit History Found"
        conn.rollback()
    return render(request,'Dtables/audit_log.html',data)

def user_logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)