from django.db import models

# Create your models here.
class UpFiles(models.Model):
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files')
    downloads = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name


class Participants(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_completed = models.BooleanField(default=False)
    is_files_downloaded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class UserFiles(models.Model):
    participant = models.ForeignKey(Participants,on_delete=models.PROTECT)
    file_details = models.ForeignKey(UpFiles,on_delete=models.PROTECT)
    is_downloaded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        fname = str(self.participant.full_name) + "," + str(self.file_details.file_name)
        return fname


class SurveyResult(models.Model):
    participant = models.ForeignKey(Participants,on_delete=models.PROTECT)
    location = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    corona_affects_financially = models.BooleanField()
    lockdown_activites = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.participant.full_name
    

    



    
