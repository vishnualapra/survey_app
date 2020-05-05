from django.shortcuts import render,loader
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from . import models

# Create your views here.

@login_required(login_url='/master/login/')
def index(request):
    return HttpResponseRedirect('/master/dashboard/')

def login_view(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(username=username, password=password)
        if user is None:
            msg = "Invalid Login Details"
            try:
                ac = get_user_model()
                ac = ac.objects.get(username=username)
                if ac.is_active is False:
                    msg = "Account Not Active"
            except:
                msg = "No User Account Found"
        else:
            if user.is_active is True:
                login(request, user)
                return HttpResponseRedirect('/master/dashboard/')
            else:
                msg = "User account Not Active"

    template = loader.get_template('master/login.html')
    return HttpResponse(template.render({'msg':msg},request))

@login_required(login_url="/master/login/")
def dashboard(request):
    msg = ''
    
    template = loader.get_template('master/dashboard.html')
    return HttpResponse(template.render({'msg':msg,'mainp': 'dashboard',},request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/master/login/')

@login_required(login_url="/master/login/")
def files(request):
    msg = ''
    if request.method == "POST" and 'ftitle' in request.POST:
        ftitle = request.POST.get('ftitle')
        fle = request.FILES['fle']
        f = models.UpFiles()
        f.file_name = ftitle
        f.file = fle
        f.save()
        msg = "sucadd"
    if request.method == 'POST' and 'deleteid' in request.POST:
        try:
            models.UpFiles.objects.get(id=request.POST.get('deleteid')).delete()
            msg = "sucdlt"
        except:
            msg = "not_dlt"
    files = models.UpFiles.objects.all()
    template = loader.get_template('master/files.html')
    return HttpResponse(template.render({'msg':msg,'files':files,'page':'files'},request))



@login_required(login_url="/master/login/")
def participants(request):
    msg = ''
    files = models.Participants.objects.all()
    template = loader.get_template('master/participants.html')
    return HttpResponse(template.render({'msg':msg,'files':files,'page':'parti'},request))


@login_required(login_url="/master/login/")
def participant(request,id):
    msg = ''
    participant = models.Participants.objects.get(id=id)
    survey = models.SurveyResult.objects.get(participant_id=id)
    files = models.UserFiles.objects.filter(participant_id=id)
    template = loader.get_template('master/participant.html')
    return HttpResponse(template.render({'msg':msg,'participant':participant,'survey':survey,'files':files,'page':'parti'},request))