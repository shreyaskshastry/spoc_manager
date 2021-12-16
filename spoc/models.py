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
    ('DU(BFS)', 'DU(BFS)'),
    ('DU(CTU)', 'DU(CTU)'),
    ('DU(EM)', 'DU(EM)'),
    ('DU(Ins)', 'DU(Ins)'),
    ('DU(LS)', 'DU(LS)'),
    ('DU(M&E)', 'DU(M&E)'),
    ('DU(MFG)', 'DU(MFG)'),
    ('DU(O&G)', 'DU(O&G)'),
    ('DU(INT)', 'DU(INT)'),
    # PU teams 
    ('PU(OR)', 'PU(OR)'),
    ('PU(CIS)', 'PU(CIS)'),
    ('PU(AEG)', 'PU(AEG)'),
    ('PU(DATA)', 'PU(DATA)'),
    ('PU(SAP)', 'PU(SAP)'),
    ('PU(DGT)', 'PU(DGT)'),
    ('PU(CSGT)', 'PU(CSGT)'),
    ('PU(CLD)', 'PU(CLD)'),
    ('PU(IIOT)', 'PU(IIOT)'),
]

class Spoc(models.Model):   
    id = models.AutoField(primary_key=True)
    screen_name =  models.CharField(max_length=50,choices=screen_name_choices,null=True)
    team_name =  models.CharField(max_length=50,choices=team_name_choices,null=True)
    spoc_name =  models.CharField(max_length=50,null=True)
    created_date = models.DateField(auto_now_add=True)
    created_by = models.CharField(max_length=50,null=True)
    modified_date = models.DateField(auto_now_add=True)
    modified_by = models.CharField(max_length=50,null=True)
    is_delete = models.BooleanField(default=False)
    is_approve = models.BooleanField(default=False)

# b = Spoc(screen_name = 'Project master',team_name = 'DU',spoc_name = 'shreyas', created_by = 'Shreyas', modified_by = 'Shreyas')
