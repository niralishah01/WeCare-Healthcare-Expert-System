from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect,HttpResponseRedirect
from django.urls import reverse
from django.template.context_processors import csrf
from registration.models import UserDetails,Doctor,Disease
import requests
from django.db.models import Q
# from newsapi import NewsApiClient
# Create your views here.
symp=['back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
    'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
    'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
    'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
    'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
    'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
    'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
    'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
    'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
    'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
    'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
    'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
    'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
    'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
    'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
    'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
    'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
    'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
    'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
    'yellow_crust_ooze','itchy skin','hunger']
def index(request):
    return render(request,'index.html')

def doctorhome(request):
    return render(request,'doctor_home.html')

def adminhome(request):
    return render(request,'admin_home.html')

def news(request):
    # https://www.medicalnewstoday.com/
    # newsapi = NewsApiClient(api_key='81606bad15824906a328e56705cc8f52')
    # top_headlines = newsapi.get_top_headlines(q='bitcoin',
    #                                       sources='bbc-news,the-verge',
    #                                       category='business',
    #                                       language='en',
    #                                       country='us')
    # print(top_headlines)
    # return render(request,'home.html')
    url = ('http://newsapi.org/v2/top-headlines?'
        'q=medical&'
        'apiKey=81606bad15824906a328e56705cc8f52')
    response = requests.get(url)
    # print(response.json())
    results=response.json()['articles']
    # print(results)
    news=[]#title
    image=[]#url for image
    desc=[]#description
    content=[]
    urls=[]
    for l in range(len(results)):
        t=results[l]
        news.append(t['title'])
        image.append(t['urlToImage'])
        desc.append(t['description'])
        content.append(t['content'])
        urls.append(t['url'])
    mylist=zip(news,desc,content,image,urls)
    return render(request,'news.html',{'mylist':mylist})

def getprofile(request):
    name=request.session['doctor']
    d=UserDetails.objects.get(name=name)
    c={}
    c.update(csrf(request))
    return render(request,'profile.html',{'d':d,'c':c})

def updateprofile(request):
    name=request.POST['name']
    email=request.POST['email']
    contactno=request.POST['contactno']
    education=request.POST['education']
    speciality=request.POST['speciality']
    UserDetails.objects.filter(name=name).update(emailID=email)
    u=UserDetails.objects.get(name=name)
    d=Doctor(contactno=contactno,education=education,speciality=speciality,userID=u)
    d.save()
    return HttpResponseRedirect('/home/doctorhome/')

def gotosearch(request):
    
    c={}
    c.update(csrf(request))
    return render(request,'search.html',{'c':c,'l1':symp}) 

def search(request):
    c={}
    c.update(csrf(request))
    sym1=(int)(request.POST['sym1'])
    sym2=(int)(request.POST['sym2'])
    if(sym1==0 or sym2==0):
        return render(request,'search.html',{'c':c,'found':False,'l1':symp,'errmsg':'please enter atleast 2 symptoms details'})
    ds1=Disease.objects.filter(Q(Symptoms__icontains=symp[sym1-1]))
    ds2=Disease.objects.filter(Q(Symptoms__icontains=symp[sym2-1]))
    sym3=(int)(request.POST['sym3'])
    if(ds1 or ds2):
        q1=set(ds1)
        q2=set(ds2)
        q=set(ds1).intersection(set(ds2))
    
        if(q):
            return render(request,'search.html',{'q':q,'found':True,'c':c,'l1':symp})
        else:
            return render(request,'search.html',{'q1':q1,'found':True,'c':c,'q2':q2,'l1':symp,'sug':'provide more symptoms to get perfect results if possible'})
    else:
        return render(request,'search.html',{'msg':'Sorry!!!not found any matching results..kindly request you to provide this details in FAQ. our team will give you satisfiable answer there..','found':False,'c':c,'l1':symp})
   
    

    