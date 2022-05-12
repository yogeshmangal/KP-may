from django.http import HttpResponse
from django.shortcuts import render,redirect
from pymongo import MongoClient
from neo4j import GraphDatabase
import requests

# Create your views here.

def home(request):
    return HttpResponse("hello, your response has been sent");

def contribute(request):
    if request.method == "POST":
        ptype=request.POST['ptype']
        itype=request.POST['itype']
        psummary=request.POST['psummary']
        pdescription=request.POST['pdescription']
        products=request.POST['products']
        kanalysis=request.POST['kanalysis']
        kinsights=request.POST['kinsights']
        

        conn = MongoClient()
        db=conn.knowledgeplatform
        collection=db.knowledge

        #making a collection to send to mongo database
        rec1={
        #   "username":username1,          
          "ptype":ptype,
          "psummary":psummary,
          "pdescription":pdescription,
          "products":products,
          "kanalysis":kanalysis,
          "kinsights":kinsights,

        }
        
        collection.insert_one(rec1)


        graphdb=GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "admin"))
        session=graphdb.session()
        q2='''Merge (kp:knowledge {pdescription: '%s', ptype: '%s', psummary: '%s' , kanalysis:'%s', kinsights:'%s', products:'%s'})
        '''%(pdescription,ptype,psummary,kanalysis,kinsights,products)
        q1=" match(n) return n "

        session.run(q2)
        session.run(q1)

        

        return redirect("home")
      
    return render(request,"contribute.html")


   