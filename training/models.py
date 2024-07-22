
from django.db import models
class Unit(models.Model):
   unit_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
   unit_name = models.CharField(max_length=50)
   unit_description = models.CharField(max_length=100)

   def __str__(self):
      return (f"{self.unit_name}")
class User_record(models.Model):
   user_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
   firstname = models.CharField(max_length=50)
   lastname = models.CharField(max_length=50)
   email = models.CharField(max_length=50)
   reg_date = models.DateField(auto_now_add=True)
   user_type = models.CharField(max_length=50)

   def __str__(self):
      return (f"{self.firstname} {self.lastname}")
   

class User_unit(models.Model):
   unit= models.ForeignKey(Unit, blank=False, on_delete=models.PROTECT)
   user = models.ForeignKey(User_record, blank=False, on_delete=models.PROTECT)
   start_date = models.DateField(auto_now_add=True)
   end_date = models.DateField(null=True, blank=True)

   def __str__(self):
      return (f"{self.unit_id} {self.user_id}")
   
class Task(models.Model):
   task_id =models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
   user = models.ForeignKey(User_record, blank=True, on_delete=models.PROTECT)
   unit = models.ForeignKey(Unit, blank = True, on_delete=models.PROTECT)
   name = models.CharField(max_length= 100)
   description = models.TextField()
   start_date = models.DateField(blank=True, null= True)
   due_date = models.DateField(blank= True, null =True)
   files = models.FileField(upload_to="{% media 'files/task_files' %}")
   status = models.CharField(max_length= 50 ,default = "Assigned")

   def __str__(self):
      return (f"{self.task_id} {self.name}")
   
class Submission(models.Model):
   task = models.ForeignKey(Task, blank = False, on_delete=models.PROTECT)
   sub_file = models.FileField(upload_to="{% media 'files/submission_files' %}")
   comments = models.TextField(max_length=1000)
   sub_date = models.DateField(auto_now_add=True)
  
   def __str__(self):
      return (f"Submission for {self.task}")


