from django.db import models

class DeploySheet(models.Model):
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


class Variables(models.Model):
    Attr_Name = models.CharField(max_length=50)
    Attr_Value = models.CharField(max_length=200)
    sheet =  models.ForeignKey(DeploySheet)

    def __str__(self):
        return self.Attr_Name


class Instances(models.Model):
    Instance = models.CharField(max_length=50)
    Inst_Name = models.CharField(max_length=50)
    Inst_Id = models.CharField(max_length=50)
    Inst_Ip = models.CharField(max_length=20)
    Inst_Fqdn = models.CharField(max_length=50)
    Inst_Cmd = models.CharField(max_length=200)
    sheet =  models.ForeignKey(DeploySheet)

    def __str__(self):
        return self.Inst_Name

class Deploys(models.Model):
    Instance = models.ForeignKey(Instances)
    Order = models.CharField(max_length=5, default="3")
    Cmd = models.CharField(max_length=200)
    Status = models.CharField(max_length=5, default="0")
    sheet =  models.ForeignKey(DeploySheet)

    def __str__(self):
        return self.Instance

class Webhook(models.Model):
    name = models.CharField(max_length=100, default="test")
    post_data = models.CharField(max_length=10000, default="this is a test")
    
    def __str__(self):
        return self.name



# Create your models here.
