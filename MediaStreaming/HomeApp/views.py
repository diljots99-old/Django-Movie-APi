from django.shortcuts import render



def index(request):

    context = {
        "page_title ":"Home App"
    }
    return render(request,'HomeApp/index.html',context)# Create your views here.
