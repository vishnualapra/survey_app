from django.shortcuts import render,loader
from django.http import HttpResponse
from master import models

# Create your views here.
def index(request):
    files = []
    temp ='web/login.html'
    msg = ""
    sucf = 1
    if request.method == 'POST' and 'name' in request.POST:
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            try:
                user = models.Participants.objects.get(email=email)
                request.session['id'] = user.id
                request.session['name'] = user.full_name
                request.session['email'] = user.email
                if user.is_completed is True:
                    msg = "already_completed"
                    temp ='web/login.html'
                else:
                    fls = models.UpFiles.objects.filter(status=True)
                    for i in fls:
                        try:
                            f = models.UserFiles.objects.get(file_details_id=i.id,participant_id=user.id)
                        except:
                            f = models.UserFiles()
                            f.participant_id = user.id
                            f.file_details_id = i.id
                            f.save()
                    files = models.UserFiles.objects.filter(participant_id=user.id)
                    sucf = models.UserFiles.objects.filter(participant_id=user.id,is_downloaded=False).count()
                    msg = "not_completed"
                    temp = 'web/index.html'

            except:
                user = models.Participants()
                user.full_name = name
                user.email = email
                user.save()
                fls = models.UpFiles.objects.filter(status=True)
                for i in fls:
                    f = models.UserFiles()
                    f.participant_id = user.id
                    f.file_details_id = i.id
                    f.save()
                files = models.UserFiles.objects.filter(participant_id=user.id)
                sucf = models.UserFiles.objects.filter(participant_id=user.id,is_downloaded=False).count()
                request.session['id'] = user.id
                request.session['name'] = user.full_name
                request.session['email'] = user.email
                msg = "started"
                temp = 'web/index.html'


        except:
            msg = "error"
            temp ='web/login.html'

    if request.method == 'POST' and 'fid' in request.POST:
        f = models.UserFiles.objects.get(id=request.POST.get('fid'))
        f.is_downloaded = True
        f.save()
        f.file_details.downloads = int( f.file_details.downloads) + 1
        f.file_details.save()
        sucf = models.UserFiles.objects.filter(participant_id=f.participant_id,is_downloaded=False).count()
        if sucf == 0:
            f.participant.is_files_downloaded = True
            f.participant.save()
        download = f.file_details.file.url
        files = models.UserFiles.objects.filter(participant_id=f.participant_id)
        request.session['id'] = f.participant_id
        request.session['name'] = f.participant.full_name
        request.session['email'] = f.participant.email
        msg = "started"
        temp = 'web/index.html'

    if request.method == 'POST' and 'location' in request.POST:
        user = models.Participants.objects.get(id=request.session['id'])
        location = request.POST.get('location')
        job = request.POST.get('job')
        industry = request.POST.get('industry')
        affects = request.POST.get('question_3')
        des = request.POST.get('description')
        sur = models.SurveyResult()
        sur.participant_id = user.id
        sur.location = location
        sur.job = job
        sur.industry = industry
        if affects == "Yes":
            sur.corona_affects_financially = True
        else:
            sur.corona_affects_financially = False
        sur.lockdown_activites = des
        sur.save()
        user.is_completed = True
        user.save()
        msg = "completed"
        temp ='web/login.html'
        
        
    template = loader.get_template(temp)
    return HttpResponse(template.render({'files':files,'msg':msg,'sucf':sucf},request))