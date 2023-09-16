from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Anomally_Detect(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
     title = models.CharField(max_length=255,default='title',blank=True,null=True)
     original = models.FileField(upload_to='anomaly_detect/original',blank=True,null=True)
     weekday_plot = models.ImageField(upload_to='anomaly_detect/weekday',blank=True,null=True)
     hist_img = models.ImageField(upload_to='anomaly_detect/weekday',blank=True,null=True)
     final = models.FileField(upload_to='anomaly_detect/final',blank=True,null=True)
     outliers = models.FileField(upload_to='anomaly_detect/outliers',blank=True,null=True)
     anomaly = models.FileField(upload_to='anomaly_detect/anomaly',blank=True,null=True)

     def __str__(self):
          return self.title