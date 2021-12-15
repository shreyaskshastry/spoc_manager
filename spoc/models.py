from django.db import models
from django.contrib.auth.models import User
from django.utils  import timezone

# Create your models here.

screen_name_choices  = [
    ('Proof_master', 'Proof_master'),
    ('Project_master', 'Project_master'),
    ('Admin_master', 'Admin_master'),
    ('RI_master', 'RI_master'),
    ('Account_master','Account_master'),
]

team_name_choices = [
    ('Audit & Compliance', 'Audit & Compliance'),
    ('Governance','Governance'),
    ('Dev_team','Dev_team'),
    # DU teams 
    ('BFS', 'BFS'),
    ('CTU', 'CTU'),
    ('EM', 'EM'),
    ('Ins', 'Ins'),
    ('LS', 'LS'),
    ('M&E', 'M&E'),
    ('MFG', 'MFG'),
    ('O&G', 'O&G'),
    ('INT', 'INT'),
    # PU teams 
    ('OR', 'OR'),
    ('CIS', 'CIS'),
    ('AEG', 'AEG'),
    ('DATA', 'DATA'),
    ('SAP', 'SAP'),
    ('DGT', 'DGT'),
    ('CSGT', 'CSGT'),
    ('CLD', 'CLD'),
    ('IIOT', 'IIOT'),
]

class Spoc(models.Model):   
    screen_name =  models.CharField(max_length=50,choices=screen_name_choices,null=True)
    team_name =  models.CharField(max_length=50,choices=team_name_choices,null=True)
    spoc_name =  models.CharField(max_length=50,null=True)
    created_date = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=50,null=True)
    modified_date = models.DateField(auto_now_add=True)
    modified_by = models.CharField(max_length=50,null=True)

# b = Spoc(screen_name = 'Project master',team_name = 'DU',spoc_name = 'shreyas', created_by = 'Shreyas', modified_by = 'Shreyas')
