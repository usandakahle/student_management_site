from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponseRedirect, FileResponse
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from training.models import User_record, User_unit, Unit, Task, Submission
from datetime import  datetime, date
from django.db.models import Q

from django.conf import settings
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.core.mail import send_mail


# a function to extract the initials of the logged user tp display in the initials circle on the main pages
def getInitials(user_id):
   user = User.objects.get(id = user_id)
   initials = user.first_name[0].upper()+ user.last_name[0].upper()
   return initials


#review or ignore
def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")

def home(request):
    return render(request,'home.html')


#students dashboard
@login_required
def dashboard(request):
    
    logged = request.user
    user_id = logged.id
    initials = getInitials(user_id)
    
#if the user type is a student and the user_unit unit id of the student is the same as the admin
#then the student should see the assigned task in their dashboard
# user_unit = User_unit.objects.get(user = logged).unit
    user_record = User_record.objects.get(user_id = user_id)
    if user_record.user_type == "Student":
       
        user = User.objects.get(id=user_id)
        user_tasks = Task.objects.filter(user = user_id)
    # only the tasks that have the same user_id as the logged user
    
        today = date.today()

       #loop for changing the statuses of the tasks 
        for task in user_tasks:
            if task.status != "Complete":
                
                if task.start_date and task.start_date <= today :
                    task.status = "Open" 
                    task.save()
                if task.due_date and task.due_date < today:
                    task.status = "Closed"
                    task.save()
    
        datej = user.date_joined.date()
        number_of_days = (today - datej).days

        tasks= user_tasks
        #query that is entered in  the search bar
        q = ""

        if request.method == "POST":
            q = request.POST['q']
            if q:
                tasks = user_tasks.filter(Q(name__contains=q) |                          
                Q(status__contains=q) |
                Q(start_date__contains=q) |
                Q(due_date__contains=q)
                )
                
        
        if request.GET.get("export_pdf"):
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            
            y_position = height - 50  # Starting position for the text
            margin = 50  # Left margin
            max_width = width - 2 * margin  

            for task in tasks:
                #editting how the data will be exported onto the generated pdf
                p.setFont("Helvetica-Bold", 12)
                p.drawString(margin, y_position, f"Task Name: {task.name}")
                y_position -= 14

                p.setFont("Helvetica", 10)


                description = f"Description: {task.description}"
                description_lines = p.beginText(margin, y_position)
                description_lines.setTextOrigin(margin, y_position)
                description_lines.setFont("Helvetica", 10)
                for line in description.splitlines():
                    description_lines.textLine(line)
                    y_position -= 14

                p.drawText(description_lines)
                y_position -= 14


                p.drawString(50, y_position, f"Start Date: {task.start_date}")
                y_position -= 14

                p.drawString(50, y_position, f"Due Date: {task.due_date}")
                y_position -= 14

                p.drawString(50, y_position, f"Status: {task.status}")
                y_position -= 14

                y_position -= 10  # Add some space between tasks

                if y_position < 50:  # If we're running out of space on the page, create a new page
                    p.showPage()
                    y_position = height - 50

            p.showPage()
            p.save()
            buffer.seek(0)

            return FileResponse(buffer, as_attachment=True, filename='tasks.pdf')
        
        #test after making modifications in settings.py
        if  request.GET.get("share"):
          email_subject = "Task Details"
          email_body = "Here are the details of your tasks:\n\n"
          for task in tasks:
            email_body += f"Task Name: {task.name}\n"
            email_body += f"Description: {task.description}\n"
            email_body += f"Start Date: {task.start_date}\n"
            email_body += f"Due Date: {task.due_date}\n"
            email_body += f"Status: {task.status}\n\n"
            
            email_from = settings.EMAIL_HOST_USER
            send_mail(
                email_subject,
                email_body,
                email_from,  # From email
                ['sandakbhengu18@gmail.com'],  # To email
                fail_silently=False,
            )
          

        
    dashdict= {'initials': initials, 'tasks': tasks, 'days':number_of_days,"query":q }
    return render(request,'mainView.html',dashdict)

@login_required
def adminDash(request):
    user_id = request.user.id
    initials = getInitials(user_id)
    user = request.user
    logged =  User_record.objects.get(email = user)
    logged_unit_name = User_unit.objects.get(user=logged).unit
    logged_unit = logged_unit_name.unit_id

    user_tasks = Task.objects.filter(unit = logged_unit)
    in_unit = User_unit.objects.filter(unit = logged_unit)
    users_in_unit = [user_unit.user for user_unit in in_unit]
  
   #for manages tasks button in the admin viewtasks page
    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'delete':
            task_ids = request.POST.getlist('task_ids')
            Task.objects.filter(taks_id__in=task_ids).delete()
            Task.save()
            return redirect('viewTask')

    tasks = user_tasks
    q = ""

    if request.method == "POST":
        q = request.POST['q']
        if q :
            tasks = Task.objects.filter(Q(name__contains=q) |                          
            Q(status__contains=q) |
            Q(start_date__contains=q) |
            Q(due_date__contains=q)
        )
        
        if q.isdigit():
           tasks = Task.objects.filter(user = q)
            
    dashdict = {'initials': initials,'tasks': tasks,"query":q }    
    return render(request,'taskView.html', dashdict)

def register(request):
    units = Unit.objects.all()
        
    if request.method =="POST" :
      ufirstname = request.POST['first_name']
      ulastname = request.POST['last_name']
      uemail = request.POST['email']
      upassword = request.POST['password1']
      cupassword = request.POST['password2']
      user_typer = request.POST['user_type']
      unit_id = request.POST['unit_id']
     
      
      if upassword==cupassword:
        if User.objects.filter(email= uemail).exists():
           messages.info(request,"Email already exists. Please Login") 
        else:
            user = User.objects.create_user(username=uemail, 
                                            email=uemail,
                                            password=upassword,
                                            first_name =ufirstname, 
                                            last_name = ulastname
                                            )
            user.save()
            user2 = User_record.objects.create(user_id = getattr(user, 'id'),
                                                firstname = getattr(user, 'first_name'),
                                                lastname = getattr(user,'last_name'),
                                                email = getattr(user,'email'),
                                                reg_date = getattr(user,'date_joined'),
                                                user_type = user_typer)
            
            user2.save()

            user_unit= User_unit.objects.create(user=user2, unit = Unit.objects.get(unit_id = unit_id))
            user_unit.save()
            if user_typer == 'Student':
                messages.success(request,"Successfully registered! Login")
                return render(request, 'login.html')
            
            if user_typer=='Dept Admin':
                if Unit.objects.filter(unit_id=unit_id).exists():
                    #unit = Unit.objects.get(unit_id = unit_id)
                    #aunit = User_unit.objects.create(user_id = getattr(user, 'id'),unit= unit)
                    #aunit.save()
                    messages.success(request,"Successfully registered! Login")
                    return render(request,'login.html')
                else:
                    messages.error(request,"Unit does not exist")
                    return redirect('home')
                #verify that they are a dept admin by asking for their unit id then send request for admin dash
      else:
        messages.error(request,"Passwords do not match") 
        return redirect('register')   
    return render(request,'register.html',{"units": units})

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        user = authenticate(request, username=email,password=password)
     
        if user is not None:
            try:
                u = User_record.objects.get(user_id = user.id)
                
                usertype = u.user_type

                login(request,user) 
                if usertype == "Student":
                    messages.success(request,"Logged in")
                    return redirect('dashboard')
                elif usertype== "Dept Admin":
                    messages.success(request,"Logged in")
                    return redirect('adminDash')
                else:
                    messages.error(request,"Error logging in")  
                    return redirect('login')
            except User_record.DoesNotExist:
                messages.error(request, "User account not found")
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')
    else:
      return render(request,'login.html')


@login_required
def createTask(request):
    user = request.user
    logged =  User_record.objects.get(email = user)
    logged_unit_name = User_unit.objects.get(user=logged).unit
    logged_unit = logged_unit_name.unit_id

    in_unit = User_unit.objects.filter(unit = logged_unit)
    #get the user names to display in assignment of task
    users_in_unit = [logged_unit.__getattribute__("user") for logged_unit in in_unit]
 
    if request.method =="POST" :
      
      if 'file' not in request.FILES:
         file = None
      else:
         file = request.POST['file']
      taskname = request.POST['taskname']
      description = request.POST['description']
      start= request.POST['start_date']
      due = request.POST['due_date']
      
      user_id = request.POST['user_id']
      
      
      try:
        assigned = User_record.objects.get(user_id = user_id)  
        task = Task.objects.create(
        name = taskname,
        description = description, 
        start_date = start, 
        due_date = due,
        files = file,
        user = assigned,
        unit = logged_unit_name
         )
        task.save()
        messages.success(request,"Task created successfully")
        return redirect('viewTask')
      except User_unit.DoesNotExist:
        messages.error(request,"Unit not exist")
        return redirect('home')
      
    return render(request,'createTask.html', {'users': users_in_unit})

@login_required
def viewTask(request):
    user_id = request.user.id
    initials = getInitials(user_id)
    user = request.user
    logged =  User_record.objects.get(email = user)
    logged_unit_name = User_unit.objects.get(user=logged).unit
    logged_unit = logged_unit_name.unit_id

    user_tasks = Task.objects.filter(unit = logged_unit)
    in_unit = User_unit.objects.filter(unit = logged_unit)
    users_in_unit = [user_unit.user for user_unit in in_unit]

    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'delete':
            task_ids = request.POST.getlist('task_ids')
            Task.objects.filter(taks_id__in=task_ids).delete()
            Task.save()
            return redirect('viewTask')

    tasks = user_tasks
    q = ""

    if request.method == "POST":
        q = request.POST['q']
        if q :
            tasks = Task.objects.filter(Q(name__contains=q) |                          
            Q(status__contains=q) |
            Q(start_date__contains=q) |
            Q(due_date__contains=q)
        )
        
        if q.isdigit():
          tasks = Task.objects.filter(user = q)
            
    dashdict = {'initials': initials,'tasks': tasks,"query":q }    
    return render(request,'taskView.html', dashdict)
   


def mainView(request):
   #task_id = request.GET.get('task_id')
  # task = Task.objects.get(task_id= task_id)
   return render(request,'mainView.html')

@login_required
def submission(request):
   user = request.user
   print(user)
   today = date.today()

   task_id = request.GET.get('task_id') 
   if not task_id:
    task_id = request.POST['task_id']
   
   if not task_id:
    messages.error(request, "No task ID provided.")
    return redirect('dashboard')
   try:
    task = Task.objects.get(task_id=task_id)
   except Task.DoesNotExist:
    messages.error(request, "Task does not exist.")
    return redirect('dashboard')
  
    
   if request.method =="POST" :
        if 'file' not in request.FILES:
          subfile = None
        else:
          subfile = request.FILES['file'] 
          comment = request.POST['comment']
      
        
        try:
            submission = Submission.objects.create(
                task = task,
                sub_file = subfile,
                comments = comment,
                sub_date= today
            )
            submission.save()

            task.status = "Complete" 
            task.save()
            
            messages.success(request,"Task submitted successfully")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request,f"An error occured: {e}")
            return redirect('submission')
    
   return render(request,'submission.html',{'task':task})

def feedback(request):
    user = request.user
    logged =  User_record.objects.get(email = user)
    logged_unit_name = User_unit.objects.get(user=logged).unit
    logged_unit = logged_unit_name.unit_id

    tasks = Task.objects.filter(unit = logged_unit)
    in_unit = User_unit.objects.filter(unit = logged_unit)
    users_in_unit = [user_unit.user for user_unit in in_unit]

    submissions={}

    for task in tasks:
       if task.status == "Complete":
         submissions[task] = Submission.objects.filter(task = task)
    
     
        
    if request.GET.get("export_pdf"):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        
        y_position = height - 50  # Starting position for the text
        margin = 50  # Left margin
        max_width = width - 2 * margin  

        for task in tasks:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(margin, y_position, f"Task Name: {task.name}")
            y_position -= 14

            p.setFont("Helvetica", 10)


            description = f"Description: {task.description}"
            description_lines = p.beginText(margin, y_position)
            description_lines.setTextOrigin(margin, y_position)
            description_lines.setFont("Helvetica", 10)
            for line in description.splitlines():
                description_lines.textLine(line)
                y_position -= 14

            p.drawText(description_lines)
            y_position -= 14


            p.drawString(50, y_position, f"Start Date: {task.start_date}")
            y_position -= 14

            p.drawString(50, y_position, f"Due Date: {task.due_date}")
            y_position -= 14

            p.drawString(50, y_position, f"Status: {task.status}")
            y_position -= 14

            y_position -= 10  # Add some space between tasks

            if y_position < 50:  # If we're running out of space on the page, create a new page
                p.showPage()
                y_position = height - 50

        p.showPage()
        p.save()
        buffer.seek(0)

        return FileResponse(buffer, as_attachment=True, filename='tasks.pdf')
   # submissions = Submission.objects.filter(task__in = tasks)
    return render(request,'feedback.html', {'tasks':tasks, 'submissions': submissions})

