import imp
from django.shortcuts import render
import psycopg2
# Create your views here.


def home(request):
    return render(request,'Dtables/home.html',{})


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
                conn = psycopg2.connect(
                        host="ec2-44-199-52-133.compute-1.amazonaws.com",
                        database="d3cghqvqk02ucg",
                        user="fpgmhtjqlwixcj",
                        port="5432",
                        password="34a96669eff5909572740d2860fbfeac7bf1646f4e7994988b66a0acf7a779be")
                cur = conn.cursor()
                cur.execute(cq)
                desc="SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '"+request.POST["table_name"].lower()+"';"
                cur.execute(desc)
                data["data"]= cur.fetchall()
                data["data_tablename"]=request.POST["table_name"].lower().title()
                cur.close()
                conn.commit()
            except (Exception, psycopg2.DatabaseError) as error:
                data["error"]=str(error).replace("relation","Table").title()
                conn.rollback()
            finally:
                if conn is not None:
                    conn.close()

    data["range_col"]=range(1,no_col+1)
    data["no_col"]=no_col
    return render(request,'Dtables/create_table.html',data)

def delete_table(request):
    data={}
    if request.method == 'POST':
        try:
            conn = psycopg2.connect(
                    host="ec2-44-199-52-133.compute-1.amazonaws.com",
                    database="d3cghqvqk02ucg",
                    user="fpgmhtjqlwixcj",
                    port="5432",
                    password="34a96669eff5909572740d2860fbfeac7bf1646f4e7994988b66a0acf7a779be")
            cur = conn.cursor()
            cur.execute("DROP TABLE "+request.POST["table_name"].lower()+";")
            data["message"]='Table "'+request.POST["table_name"].lower().title()+'" Successfully Deleted'
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            data["error"]=str(error).title()
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()
    return render(request,'Dtables/delete_table.html',data)

def user_login(request):
    return render(request,'Dtables/login.html',{})

def user_signup(request):
    return render(request,'Dtables/signup.html',{})