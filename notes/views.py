from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
from datetime import date
# Create your views here.

def about(request):
    return render(request,'about.html')

def index(request):
    return render(request,'index.html')

def contact(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fullname']
        em = request.POST['email']
        m = request.POST['mobile']
        s = request.POST['subject']
        msg = request.POST['message']
        try:

            Contact.objects.create(fullname=f, email=em, mobile=m, subject=s, message=msg,msgdate=date.today(),isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request, 'contact.html', locals())

def userlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'login.html', locals())

def login_admin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error ="yes"
        except:
            error = "yes"
    return render(request,'login_admin.html', locals())

def signup1(request):
    error=""
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        e = request.POST['emailid']
        p = request.POST['password']
        b = request.POST['branch']
        r = request.POST['role']
        try:
            user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user, contact=c,branch=b,role=r)
            error="no"
        except:
            error="yes"
    return render(request,'signup.html', locals())

def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    pn = Notes.objects.filter(status="pending").count()
    an = Notes.objects.filter(status="Accept").count()
    rn = Notes.objects.filter(status="Reject").count()
    alln = Notes.objects.all().count()
    d = {'pn':pn,'an':an,'rn':rn,'alln':alln}
    return render(request,'admin_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)


    d = {'data':data,'user':user}
    return render(request,'profile.html',d)

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)
    error = False
    if request.method=='POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        b = request.POST['branch']
        user.first_name = f
        user.last_name = l
        data.contact = c
        data.branch = b
        user.save()
        data.save()
        error=True

    d = {'data':data,'user':user,'error':error}
    return render(request,'edit_profile.html',d)

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"

    return render(request,'changepassword.html', locals())

def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    if request.method=='POST':
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.FILES['notesfile']
        f = request.POST['filetype']
        d = request.POST['description']
        u = User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,subject=s,notesfile=n,
                                 filetype=f,description=d,status='pending')
            error="no"
        except:
            error="yes"
    return render(request,'upload_notes.html', locals())

def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user = user)

    d = {'notes':notes}
    return render(request,'view_mynotes.html',d)

def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return  redirect('view_mynotes')

def view_allnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user = user)

    d = {'notes':notes}
    return render(request,'view_allnotes.html',d)

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    users = Signup.objects.all()

    d = {'users':users}
    return render(request,'view_users.html',d)

def delete_users(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('view_users')

def pending_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status = "pending")
    d = {'notes':notes}
    return render(request, 'pending_notes.html',d)

def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status = "Accept")
    d = {'notes':notes}
    return render(request, 'accepted_notes.html',d)

def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.filter(status = "Reject")
    d = {'notes':notes}
    return render(request, 'rejected_notes.html',d)

def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.all()
    d = {'notes':notes}
    return render(request, 'all_notes.html',d)

def assign_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Notes.objects.get(id=pid)
    error = ""
    if request.method=='POST':
        s = request.POST['status']
        try:
            notes.status = s
            notes.save()
            error="no"
        except:
            error="yes"
    d = {'notes':notes,'error':error}
    return render(request, 'assign_status.html',d)

def delete_notes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return  redirect('all_notes')

def viewallnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    notes = Notes.objects.filter(status='Accept')
    d = {'notes':notes}
    return render(request, 'viewallnotes.html',d)

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        try:
            if user.check_password(o):
                user.set_password(n)

                user.save()

                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'change_passwordadmin.html', locals())

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html', locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html', locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())

def mode(request):
    return render(request, 'index.html',locals())



# ############################################################

# serverID = 'LoginServerID'
# ## On changing this variable:
# # Also change in: 1. core/base.html, 2. server/base.html, 3. manage_server.html

# ## Time in second for expiery of session
# session_expiry = 14400

# # Create your views here.
# def home(request):
#     if request.method == "POST":
#         if request.POST['type'] == "code":
#             code_id = request.POST['code_id']
#             return redirect('server-code', code_id)
#         else:
#             server_id = request.POST['server_id']
#             return redirect('server-code-list', server_id)
#     return render(request, 'server/index.html')

# def login(request):
#     if request.method == "POST":
#         server_id = request.POST['server_id']
#         secret_key = request.POST["secret_key"]

#         for c in server_id:
#             if not str(c).isalnum():
#                 messages.error(request, "Invalid server id")
#                 return redirect('server-create')

#         server_detail = firebase.check_login(server_id, secret_key)
#         if not server_detail:
#             messages.error(request ,"Incorrect server id or secret key")
#             return redirect('server-create')
#         request.session[serverID] = server_id
#         request.session.set_expiry(session_expiry) ## session is expired here.
#         return redirect('server-manage')
#     return redirect('server-create')

# def manage_server(request):
#     context={'data':None}
#     if request.session.get(serverID, False):
#         server_id = request.session.get(serverID)
#         data = firebase.get_server_code(server_id)
#         context['data'] = data

#         ## Processing the files
#         files = firebase.get_server_files(server_id)
#         managed_files = []
#         for file in files:
#             folder_name = file.name.split('/')[1]
#             file_title = folder_name[27:]
#             managed_files.append({
#                 'title':file_title,
#                 'folder':folder_name,
#                 'url':file.public_url
#                 })
#         context['files'] = managed_files
#     else:
#         return redirect('server-create')
#     return render(request, 'server/manage_server.html', context=context)

# def delete(request, id):
#     if request.session.get(serverID, False):
#         server_id = request.session.get(serverID)
#         res = firebase.delete_file(server_id, id)
#         if res:
#             messages.success(request, "Code deleted successfully")
#             return redirect('server-manage')
#         else:
#             messages.error(request, "Unauthorized code ID")
#             return redirect('server-manage')
#     return redirect('server')

# def delete_file(request, folder):
#     if request.session.get(serverID, False):
#         server_id = request.session.get(serverID)
#         filepath = server_id + "/"+folder
#         try:
#             firebase.delete_server_files(filepath)
#             messages.success(request, "File deleted successfully")
#         except:
#             messages.error(request, "Unable to delete file")
#         return redirect('server-manage')
#     return redirect('server-create')

# def upload(request):
#     context = {'isError':False}
#     try:
#         if request.session.get(serverID, False):
#             server_id = request.session.get(serverID)
#             if request.method == "POST":
#                 title = request.POST['title']
#                 upload_type = request.POST['upload_type']
#                 if upload_type == "code":
#                     code = request.POST['code']
#                 else:
#                     file = request.FILES['code_file']
#                     code = file.read().decode("utf-8")
#                 code_id = generate_code_id()

#                 if len(code) < 7:
#                     context['isError'] = True
#                     context['message'] = "Very less code."
#                     return render(request, 'server/upload.html', context)
#                 firebase.upload_code(server_id, code_id, title, code)
#                 messages.success(request, "Code uploaded successfully")
#                 return redirect('server-manage')
#         else:
#             context['isError'] = True
#             context['message'] = "Please login first"
#     except Exception as e:
#         context['isError'] = True
#         context['message'] = "Unable to upload the file."
#         print(e)
#     return render(request, 'server/upload.html', context)

# def upload_file(request):
#     context = {'isError':False}
#     try:
#         if request.session.get(serverID, False):
#             server_id = request.session.get(serverID)
#             if request.method == "POST":
#                 title = request.POST['file_title']
#                 code_id = generate_code_id()
#                 if request.FILES:
#                     file = request.FILES['my_file']
#                     filename = default_storage.save(file.name, file)
#                     file_url = default_storage.path(filename)
                    
#                     firebase.upload_file(server_id, title,file_url, filename)
#                     ## upload here file
#                     messages.success(request, "File uploaded successfully")
#                     return redirect('server-manage')
#                 else:
#                     context['isError'] = True
#                     context['message'] = "No file is selected"
#         else:
#             context['isError'] = True
#             context['message'] = "Please login first"
#     except Exception as e:
#         context['isError'] = True
#         context['message'] = "Unable to upload file"
#         print(e)
#     return render(request, 'server/upload.html', context)

# def change_password(request):
#     if request.session.get(serverID, False):
#         server_id = request.session.get(serverID)
#         if request.method == "POST":
#             sec1 = request.POST['sec1']
#             sec2 = request.POST['sec2']
#             if sec1 != sec2:
#                 messages.error(request, "Password didn't match")
#                 return redirect('server-manage')
#             firebase.change_password(server_id=server_id, secret_key=sec1)
#             messages.success(request, 'Password changed successfully')
#             return redirect('server-manage')
#     return redirect('server-create')

# def create_server(request):
#     form = ServerForm()
#     context = {'form':form}
#     if request.method == "POST":
#         form = ServerForm(request.POST)
#         if form.is_valid():
#             server_id = form.cleaned_data['server_id']
#             secret_key = form.cleaned_data['secret_key']
#             secret_key_cnf = form.cleaned_data['secret_key_cnf']
            
#             server_val = True
#             for c in server_id:
#                 if not str(c).isalnum():
#                     context['server_id_error'] = True
#                     server_val = False
#                     break
            
#             pass_val = True
#             if secret_key != secret_key_cnf:
#                 context['password_error'] = True
#                 pass_val = False

#             if server_val and pass_val:
                
#                 server_check = firebase.check_server(server_id)
#                 if not server_check:
#                     firebase.create_server(server_id=server_id, secret_key=secret_key)
#                     request.session[serverID] = server_id
#                     request.session.set_expiry(session_expiry)  ## session is expiring here.
#                     return redirect("server-manage")
#                 else:
#                     context['duplicate_server_error'] = True
#             else:
#                 context['form'] = form
#     return render(request, 'server/create.html', context=context)



# def code(request, code_id):
#     if not str(code_id).upper().isalpha():
#         messages.error(request, "Invalid code ID")
#         return redirect('server')

#     code = firebase.get_code(code_id)
#     if not code:
#         messages.error(request, "Code not found")
#         return redirect('server')

#     return render(request, 'server/code.html', {'codes':code})

# def code_list(request, server_id):
#     if not str(server_id).isalnum():
#         messages.error(request, "Invalid server id")
#         return redirect("server")
    
#     codes = firebase.get_server_code(server_id=server_id)
#     if not codes:
#         messages.error(request, "Server not found")
#         return redirect("server")

#     ## Processing the files
#     files = firebase.get_server_files(server_id)
#     managed_files = []
#     for file in files:
#         folder_name = file.name.split('/')[1]
#         file_title = folder_name[27:]
#         managed_files.append({
#             'title':file_title,
#             'folder':folder_name,
#             'url':file.public_url
#             })

#     return render(request, 'server/codelist.html',
#         {'data':codes, 'files':managed_files,'serverID':server_id})

# def delete_server(request):
#     if request.session.get(serverID, False):
#         server_id = request.session.get(serverID)
#         res = firebase.delete_server(server_id)
#         if res:
#             request.session.clear() ## Clearing the all session variable
#             messages.success(request, "Server deleted successfully")
#             return redirect('server')
#         else:
#             messages.error(request, "Unable to delete server")
#             return redirect('server-manage')
#     return redirect('server-create')

# ### helper function
# def generate_code_id():
#     codeID = firebase.get_all_codeID()
#     letters = string.ascii_uppercase

#     key = ""
#     for i in range(6):
#         key += random.choice(letters)

#     while key in codeID:
#         key = ""
#         for i in range(6):
#             key += random.choice(letters)
#     return key
