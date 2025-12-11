from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class tasks(models.Model):
    TASK_CHOICES=[
        ('pending','pending'),
        ('inprogress', 'in progress'),
        ('completed','complted')
    ]
    PRIORITY_CHOICES=[
        ('low','low'),
        ('medium','medium'),
        ('high','high')
    ]


    title=models.CharField(max_length=40)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    description=models.TextField(max_length=250)
    created_at=models.DateTimeField(auto_now_add=True)
    completed_at=models.DateTimeField(blank=True,null=True)
    priority=models.CharField(choices=PRIORITY_CHOICES,default='low')
    due_date=models.DateTimeField(blank=True,null=True)
    is_important=models.BooleanField(default=False)
    is_due=models.BooleanField(default=False)
    IS_COMPLETED=models.BooleanField(default=False)
    task_status=models.CharField(choices=TASK_CHOICES,default='pending')

    def __str__(self):
        return self.title
   
    def istaskdue(self):
        if self.due_date is not None:
            if self.IS_COMPLETED==False and timezone.now() > self.due_date:
                self.is_due=True
        
    
    def mark_completed(self):
        if self.IS_COMPLETED==True:
            self.is_due=False
            self.completed_at=timezone.now()
            self.task_status='completed'
        else:
            self.task_status='pending'
            self.completed_at=None


    def save(self,**kwargs):
        self.mark_completed()
        self.istaskdue()
        return super().save()
    
class message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_messages')
    task=models.ForeignKey(tasks,on_delete=models.CASCADE,related_name='messages',null=True,blank=True)
    hedder=models.CharField(max_length=100)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.user.username} at {self.timestamp}'