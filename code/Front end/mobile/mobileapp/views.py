from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Result
from django.contrib import messages
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
import random




# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')


Registration = 'register.html'
def register(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        email = request.POST['email']
        password = request.POST['password']
        conpassword = request.POST['conpassword']
        age = request.POST['Age']
        contact = request.POST['contact']

        print(Name, email, password, conpassword, age, contact)
        if password == conpassword:
            user = User(username=Name,email=email, password=password)
            user.save()
            return render(request, 'login.html')
        else:
            msg = 'Register failed!!'
            return render(request, Registration,{msg:msg})

    return render(request, Registration)

# Login Page 
def login(request):
    if request.method == 'POST':
        lemail = request.POST['email']
        lpassword = request.POST['password']

        d = User.objects.filter(email=lemail, password=lpassword).exists()
        print(d)
        if d:
            us = request.session['email']=lemail
            return redirect(userhome)
    return render(request, 'login.html')

def userhome(request):
    return render(request,'userhome.html')

def view(request):
    global df
    if request.method=='POST':
        g = int(request.POST['num'])
        df = pd.read_csv('mobileapp/20230329093832Mobile-Addiction-.csv')
        col = df.head(g).to_html()
        return render(request,'view.html',{'table':col})
    return render(request,'view.html')


def module(request):
    global df,x_train, x_test, y_train, y_test
    df = pd.read_csv('mobileapp/20230329093832Mobile-Addiction-.csv')
    # **fill a Null Values**
    col = df.select_dtypes(object)
    # filling a null Values applying a ffill method
    for i in col:
        df[i].fillna(method='ffill',inplace=True)
    df['Can you live a day without phone ? '].fillna(method='bfill',inplace=True)
    df['whether you are addicted to phone?'].fillna(method='bfill',inplace=True)
    # Apply The Label Encoding
    le = LabelEncoder()
    for i in col:
        df[i]=le.fit_transform(df[i])
    # Delete The unknown column
    print(df.shape)
    df.drop('Timestamp', axis = 1,inplace = True)
    df.drop('Full Name :', axis = 1,inplace = True)
    x = df.drop(['whether you are addicted to phone?'], axis = 1) 
    y = df['whether you are addicted to phone?']
    Oversample = RandomOverSampler(random_state=72)
    x_sm, y_sm = Oversample.fit_resample(x[:100],y[:100])
    x_train, x_test, y_train, y_test = train_test_split(x_sm, y_sm, test_size = 0.3, random_state= 72)
    if request.method=='POST':
        model = request.POST['algo']

        if model == "1":
            re = RandomForestClassifier(random_state=72)
            re.fit(x_train,y_train)
            re_pred = re.predict(x_test)
            ac = accuracy_score(y_test,re_pred)
            ac
            msg='Accuracy of RandomForest : ' + str(ac)
            return render(request,'module.html',{'msg':msg})
        elif model == "2":
            de = DecisionTreeClassifier()
            de.fit(x_train,y_train)
            de_pred = de.predict(x_test)
            ac1 = accuracy_score(y_test,de_pred)
            ac1
            msg='Accuracy of Decision tree : ' + str(ac1)
            return render(request,'module.html',{'msg':msg})
        elif model == "3":
            le = LogisticRegression()
            le.fit(x_train,y_train)
            le_pred = le.predict(x_test)
            ac2 = accuracy_score(y_test,le_pred)
            msg='Accuracy of LogisticRegression : ' + str(ac2)
            return render(request,'module.html',{'msg':msg})
    return render(request,'module.html')


def prediction(request):
    global df,x_train, x_test, y_train, y_test
    col = x_train.columns
    col.shape

    if request.method == 'POST':
        inp = request.POST.dict()
        print(inp)
        del inp['csrfmiddlewaretoken']
        l = []
        for i in inp.keys():
            l.append(inp[i])
        inp = []
        for i in l[1::]:
            inp.append(int(i))
        print(l)
        de = DecisionTreeClassifier()
        de.fit(x_train,y_train)
        pred = de.predict([inp])
        if inp[2] == 0:
             msg = 'Not addicted.'
        elif pred == 0:
            msg = 'Not addicted.'
        elif pred == 1:
            msg = 'Maybe addicted.'
        elif pred == 2:
            msg = 'addicted'
            
            
        confidence = de.predict_proba([inp])[0]  # Get prediction probabilities for the input
        confidence_percentage = max(confidence) * 100 
        ra = random.randint(0, 9)
        score = confidence_percentage-ra
        
        if l[1] == '0':
            aa = 'Male'
        elif l[0] == '1':
            aa = 'Female'
        else:
            aa = 'Other'
        
        
        print(l[2:8])
        da = []
        for i in l[1:9]:
            if i == '0':
                da.append('No')
            else:
                da.append('Yes')
                
        print('_______________________')
        print(len(da))      
        print('_______________________')  
                
        if l[9]== '0':
            cc = 'Never'
        elif l[9] == '1':
            cc = 'Often'
        elif l[9] == '2':
            cc = 'Rarely'
        else:
            cc = 'Sometimes'
            
            
        ca = []       
        for i in l[10:16]:
            if i == '0':
                ca.append('No')
            else:
                ca.append('Yes')
                
        print('_______________________')
        print(len(cc))  
        print('_______________________')   
                
                
        if l[17]== '0':
            qq = '0 Hours'
        elif l[17] == '1':
            qq = '1 Hours'
        elif l[17] == '2':
            qq = '2 Hours'
        elif l[17] == '3':
            qq = '3 Hours'
        elif l[17] == '4':
            qq = '4 Hours'
        else:
            qq = '5 Hours'
            
            
        
        if l[18] == '0':
           dd = 'No'
        else:
            dd = 'Yes'
        
        ema = request.session['email']
        res = Result.objects.create(a=l[0],b=aa,c=da[0],d=da[1],e=da[2],f=da[3],g=da[4],h=da[5],i=da[6],j=da[7],k=cc,l=ca[0],m=ca[1],n=ca[2],o=ca[3],p=ca[4],q=ca[5],r = qq,s=dd, out=msg,email=ema)
        return render(request,'res.html',{'msg':msg,'score':score})
    return render(request,'prediction.html',{'col':col})


def hist(req):
    col = x_train.columns
    data = Result.objects.filter(email = req.session['email'])
    return render(req,'hist.html',{'data':data,'col':col})

