from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, ProjectForm, DocumentForm, MessageForm, EmployeeForm, UpdateUserForm, DivisionForm, TaskForm, MessageMailForm, MailForm
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
from core.models import *
import datetime

from .models import Tasks, Projects

@login_required(login_url='login')
def home(request):
    tasks = []
    if request.user.is_superuser:
        tasks = Tasks.objects.all()
    else:
        emp = Employees.objects.get(user=request.user)
        tasks = emp.employee_to_task.all()

    types = {
        0: [],
        1 : [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: []
    }

    for task in tasks:
        tp = task.get_type
        types[tp].append(task)

    docs = []
    for object in Projects.objects.all():
        for element in object.project_to_document.all():
            if (datetime.date.today() - element.duration).days >= 30:
                docs.append({'doc' : element, 'obj' : object})
    context = {
        'tasks': tasks,
        't0' : len(types[0]),
        't1': len(types[1]),
        't2': len(types[2]),
        't3': len(types[3]),
        't4': len(types[4]),
        't5': len(types[5]),
        't6': len(types[6]),
        't7': len(types[7]),
        't8': len(types[8]),
        'docs': docs,
        'user': Employees.objects.filter(user=request.user)[0]
    }
    return render(request, 'core/index.html', context)


@login_required(login_url='login')
def show_docs(request):
    docs = CompanyDocuments.objects.get(pk=1).company_to_document.all()

    context = {
        'docs' : docs,
        'user': Employees.objects.filter(user=request.user)[0]
    }

    return render(request, 'core/documents.html', context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def docs_edit(request, id_doc):
    id_proj = 1
    if id_doc == 0:
        form = DocumentForm()
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                print('OK')
                saved_doc = form.save()
                CompanyDocuments.objects.get(pk=id_proj).company_to_document.add(Documents.objects.get(pk=saved_doc.pk))
                return redirect('show_docs')
            else:
                print(form.errors)
                print('ERROR')
        context = {'form': form,
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/document_adding.html', context=context)
    else:
        document = Documents.objects.get(pk=id_doc)
        form = DocumentForm()
        if request.method == 'POST':
            a = Documents.objects.get(pk=id_doc)
            form = DocumentForm(request.POST, request.FILES, instance=a)
            if form.is_valid():
                form.save()
                print('OK')
                return redirect('show_docs')
            else:
                print(form.errors)
                print('ERROR')
        for field in document._meta.fields:
            val = getattr(document, field.name)
            if 'duration' in field.name:
                if val is not None:
                    form.initial[f'{field.name}'] = val.isoformat()
            else:
                if val is not None:
                    form.initial[f'{field.name}'] = val
        context = {'document': Documents.objects.get(pk=id_doc),
                   'form': form,
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/document_adding.html', context=context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def docs_del(request, id_doc):
    try:
        Documents.objects.get(pk=id_doc).delete()
        return redirect('show_docs')
    except:
        return redirect('show_docs')


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def employees(request):
    emps = Employees.objects.all()
    context = {
        'employees' : emps,
        'user': Employees.objects.filter(user=request.user)[0]
    }
    return render(request, 'core/employees.html', context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def division_del(request, id):
    try:
        Divisions.objects.get(pk=id).delete()
        return redirect('divisions')
    except:
        return redirect('divisions')


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def divisions(request):
    divs = Divisions.objects.all()
    form = DivisionForm()

    if request.method == 'POST':
        form = DivisionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('divisions')
    context = {
        'form' : form,
        'divs': divs,
        'user': Employees.objects.filter(user=request.user)[0]
    }
    return render(request, 'core/company_structure.html', context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def employee_edit(request, id):
    if id == 0:
        form = EmployeeForm()
        if request.method == 'POST':
            form = EmployeeForm(request.POST)
            if form.is_valid():
                new_obj = form.save()
                return redirect('employee_edit', id=new_obj.id)
            else:
                print(form.errors)
        context = {'form': form,
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/object_edit.html', context=context)
    else:
        obj = Employees.objects.get(pk=id)
        user_object = obj.user
        form = EmployeeForm()
        form_user = UpdateUserForm()
        if request.method == 'POST' and request.POST['isSaved'] == '1':
            a = Employees.objects.get(pk=id)
            form = EmployeeForm(request.POST, instance=a)
            form_user = UpdateUserForm()
            if form.is_valid():
                form.save()
                return redirect('employee_edit', id=id)
            else:
                print(form.errors)
        elif request.method == 'POST' and request.POST['isSaved'] == '2':
            b = Employees.objects.get(pk=id)
            a = b.user
            form = UpdateUserForm(request.POST, instance=a)
            if form.is_valid():
                form.save()

                if request.POST['password_change']:
                    a.set_password(request.POST['password_change'])
                    a.save()
                return redirect('employee_edit', id=id)
            else:
                print(form.errors)
        for field in obj._meta.fields:
            val = getattr(obj, field.name)
            if 'date' in field.name:
                if val is not None:
                    form.initial[f'{field.name}'] = val.isoformat()
            else:
                if val is not None:
                    form.initial[f'{field.name}'] = val
        for field in user_object._meta.fields:
            val = getattr(user_object, field.name)
            if val is not None:
                form_user.initial[f'{field.name}'] = val
        context = {'form': form,
                   'form_user' : form_user,
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/employee_edit.html', context=context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def employee_add(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            b = form.save()
            a = Employees(user=b, date_of_birth=datetime.date.today(), date_of_start=datetime.date.today(), division_id=1, status=True)
            a.save()
            return redirect('employee_edit', id=a.id)
        else:
            print(form.errors)
    context = {'form': form,
               'user': Employees.objects.filter(user=request.user)[0]}
    return render(request, template_name='core/employee_add.html', context=context)

def loginPage(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            User = authenticate(request, username=username, password=password)

            if User is not None:
                login(request, User)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
                return render(request, 'core/login.html', context=context)

        return render(request, 'core/login.html', context=context)


def logoutUser(request):
    logout(request)
    return redirect('login')


#Useless method
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login.html')
        else:
            form = CreateUserForm()
        return render(request, 'core/register.html', {'form': form,
                                                      'user': Employees.objects.filter(user=request.user)[0]})

#Useless method
def forgot_password(request):
    context = {
        'user': Employees.objects.filter(user=request.user)[0]
    }
    return render(request, 'core/forgot-password.html', context=context)


@login_required(login_url='login')
def mails(request, id):
    rel = {
        '1' : 'EXP',
        '2' : 'TO',
        '3' : 'SMR',
        '4' : 'PRO'
    }
    emp = Employees.objects.get(user=request.user)
    mails = []
    if not request.user.is_superuser:
        mails = emp.mails()
    else:
        mails = Mails.objects.all()
    mailType = ''
    if id == 1:
        mailType = 'Входящие'
    else:
        mailType = 'Исходящие'

    context = {'mails': mails,
               'user': Employees.objects.filter(user=request.user)[0],
               'type' : mailType}
    return render(request, 'core/mails.html', context=context)


@login_required(login_url='login')
def objects(request, id):
    rel = {
        '1' : 'EXP',
        '2' : 'TO',
        '3' : 'SMR',
        '4' : 'PRO'
    }
    emp = Employees.objects.get(user=request.user)
    objects = []
    if not request.user.is_superuser:
        objects = emp.employee_to_project.filter(proj_type=rel[str(id)])
    else:
        objects = Projects.objects.filter(proj_type=rel[str(id)])

    context = {'objects': objects,
               'user': Employees.objects.filter(user=request.user)[0]}
    return render(request, 'core/objects.html', context=context)


@login_required(login_url='login')
def show_tasks(request, id):
    emp = Employees.objects.get(user=request.user)
    proj = Projects.objects.get(pk=id)

    if not request.user.is_superuser and not proj in emp.employee_to_project.all():
        raise 404

    tasks = Tasks.objects.filter(projects__name=proj.name)
    types = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: []
    }

    for task in tasks:
        tp = task.get_type
        types[tp].append(task)

    context = {
        'tasks': tasks,
        't0': len(types[0]),
        't1': len(types[1]),
        't2': len(types[2]),
        't3': len(types[3]),
        't4': len(types[4]),
        't5': len(types[5]),
        't6': len(types[6]),
        't7': len(types[7]),
        't8': len(types[8]),
        'proj_id' : id,
        'user': Employees.objects.filter(user=request.user)[0]
    }
    return render(request, template_name='core/tasks.html', context=context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def employee_project(request, id):
    if request.method == 'POST':
        if request.POST.get('isSaved') != '-1':
            f = request.POST.get('isSaved')
            Worker = Employees.objects.get(pk=int(f))
            Worker.employee_to_project.remove(Projects.objects.get(pk=id))
        else:
            try:
                f = request.POST.get('worker')
                Worker = Employees.objects.get(pk=int(f))
                Worker.employee_to_project.add(Projects.objects.get(pk=id))
            except:
                print('Exception')
                pass
    return redirect('card', id=id)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def employee_task(request, id):
    if request.method == 'POST':
        if request.POST.get('isSaved') != '-1':
            f = request.POST.get('isSaved')
            Worker = Employees.objects.get(pk=int(f))
            Worker.employee_to_task.remove(Tasks.objects.get(pk=id))
        else:
            try:
                f = request.POST.get('worker')
                Worker = Employees.objects.get(pk=int(f))
                Worker.employee_to_task.add(Tasks.objects.get(pk=id))
            except:
                print('Exception')
                pass
    return redirect('task', id=id)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def close_task(request, id):
    if request.method == 'POST':
        if request.POST.get('Close') == '1':
            task = Tasks.objects.get(pk=id)
            task.done = datetime.datetime.now()
            task.save()
    return redirect('task', id=id)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def document_del(request, id_doc, id_proj):
    try:
        Documents.objects.get(pk=id_doc).delete()
        return redirect('card', id=id_proj)
    except:
        return redirect('card', id=id_proj)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def document_edit(request, id_doc, id_proj):
    if id_doc == 0:
        form = DocumentForm()
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                print('OK')
                saved_doc = form.save()
                Projects.objects.get(pk=id_proj).project_to_document.add(Documents.objects.get(pk=saved_doc.pk))
                return redirect('card', id=id_proj)
            else:
                print(form.errors)
                print('ERROR')
        context = {'form': form,
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/document_adding.html', context=context)
    else:
        document = Documents.objects.get(pk=id_doc)
        form = DocumentForm()
        if request.method == 'POST':
            a = Documents.objects.get(pk=id_doc)
            form = DocumentForm(request.POST, request.FILES, instance=a)
            if form.is_valid():
                form.save()
                print('OK')
                return redirect('card', id=id_proj)
            else:
                print(form.errors)
                print('ERROR')
        for field in document._meta.fields:
            val = getattr(document, field.name)
            if 'duration' in field.name:
                if val is not None:
                    form.initial[f'{field.name}'] = val.isoformat()
            else:
                if val is not None:
                    form.initial[f'{field.name}'] = val
        context = {'document': Documents.objects.get(pk=id_doc),
                   'form': form,
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/document_adding.html', context=context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def object_del(request, id):
    rel = {
        'EXP' : '1',
        'TO' : '2',
        'SMR' : '3',
        'PRO' : '4'
    }
    try:
        proj = Projects.objects.get(pk=id)
        ret_id = proj.proj_type
        Projects.objects.get(pk=id).delete()
        return redirect('objects', id=rel[ret_id])
    except:
        return redirect('card', id=id)


@login_required(login_url='login')
def object_edit(request, id):
    if id == 0:
        form = ProjectForm()
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            if form.is_valid():
                new_obj = form.save()
                return redirect('card', id=new_obj.id)
            else:
                print(form.errors)
        context = {'form': form,
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/object_edit.html', context=context)
    else:
        emp = Employees.objects.get(user=request.user)
        obj = Projects.objects.get(pk=id)
        if not request.user.is_superuser and not obj in emp.employee_to_project.all():
            raise Http404
        form = ProjectForm()
        if request.method == 'POST':
            a = Projects.objects.get(pk=id)
            form = ProjectForm(request.POST, instance=a)
            if form.is_valid():
                form.save()
                return redirect('card', id=id)
            else:
                print(form.errors)
        for field in obj._meta.fields:
            val = getattr(obj, field.name)
            if 'date' in field.name:
                if val is not None:
                    form.initial[f'{field.name}'] = val.isoformat()
            else:
                if val is not None:
                    form.initial[f'{field.name}'] = val
        roles = {
            'DI': 'Директор',
            'ME': 'Менеджер/Инженер',
            'RA': 'Работник',
            'BU': 'Бухгалтер',
            'RN': 'Руководитель направления',
            'KS': 'Кадровый специалист'
        }
        context = {'object': Projects.objects.get(pk=id),
                   'form': form,
                   'roles': roles,
                   'employees': Employees.objects.all(),
                   'documents': Projects.objects.get(pk=id).project_to_document.all(),
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/object_edit.html', context=context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def task_edit(request, proj_id, id):
    if id == 0:
        form = TaskForm()
        if request.method == 'POST':
            form = TaskForm(request.POST, project=Projects.objects.get(pk=proj_id), author=Employees.objects.get(user=request.user))
            if form.is_valid():
                new_task = form.save()
                return redirect('card_task', proj_id=proj_id, id=new_task.id)
            else:
                print(form.errors)
        context = {'form': form,
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/task_edit.html', context=context)
    else:
        task = Tasks.objects.get(pk=id)
        form = TaskForm()
        if request.method == 'POST':
            form = TaskForm(request.POST, project=Projects.objects.get(pk=proj_id), author=task.author, instance=task)
            if form.is_valid():
                form.save()
                return redirect('card_task', proj_id=proj_id, id=id)
            else:
                print(form.errors)
        for field in task._meta.fields:
            val = getattr(task, field.name)
            if 'created' in field.name or 'done' in field.name or 'completion' in field.name:
                if val is not None:
                    form.initial[f'{field.name}'] = val.isoformat()
            elif 'name' in field.name:
                if val is not None:
                    form.initial[f'{field.name}'] = val
        context = {'task': Tasks.objects.get(pk=id),
                   'form': form,
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/task_edit.html', context=context)

@login_required(login_url='login')
def get_task_by_id(request, id):
    emp = Employees.objects.get(user=request.user)
    task = Tasks.objects.get(id=id)
    if not request.user.is_superuser and task not in emp.employee_to_task.all():
        raise Http404
    members = task.employees
    messages = task.messages
    proj_id = task.projects.id
    form = MessageForm()

    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES, task=Tasks.objects.get(id=id),
                           author=Employees.objects.get(user=request.user))
        if form.is_valid():
            print('OK')
            form.save()
            return redirect('task', id=id)
    context = {
        'form': form,
        'task': task,
        'employees': Employees.objects.all(),
        'members': members,
        'messages': messages.all().order_by('time'),
        'proj_id': proj_id,
        'user': Employees.objects.filter(user=request.user)[0]
    }
    return render(request, template_name='core/task.html', context=context)


@login_required(login_url='login')
def get_mail_by_id(request, id):
    emp = Employees.objects.get(user=request.user)
    mail = Mails.objects.get(id=id)
    if not request.user.is_superuser and mail not in emp.employee_to_mail.all():
        raise Http404
    members = mail.employees
    messages = mail.messages
    proj_id = None if mail.projects_to_mails is None else mail.projects_to_mails.id
    form = MessageMailForm()

    if request.method == "POST":
        form = MessageMailForm(request.POST, request.FILES, mails_tag=Mails.objects.get(id=id),
                           author=Employees.objects.get(user=request.user))
        if form.is_valid():
            print('OK')
            form.save()
            return redirect('get_mail_by_id', id=id)
    context = {
        'form': form,
        'mail': mail,
        'employees': Employees.objects.all(),
        'members': members,
        'messages': messages.all().order_by('time'),
        'proj_id': proj_id,
        'user': Employees.objects.filter(user=request.user)[0]
    }
    return render(request, template_name='core/mail.html', context=context)

def employee_mail(request, id):
    if request.method == 'POST':
        if request.POST.get('isSaved') == '-2':
            mail = Mails.objects.get(pk=id)
            mail.done = datetime.datetime.now()
            mail.save()
        elif request.POST.get('isSaved') != '-1':
            f = request.POST.get('isSaved')
            Worker = Employees.objects.get(pk=int(f))
            Worker.employee_to_mail.remove(Mails.objects.get(pk=id))
        else:
            try:
                f = request.POST.get('worker')
                Worker = Employees.objects.get(pk=int(f))
                Worker.employee_to_mail.add(Mails.objects.get(pk=id))
            except Exception as e:
               print(str(e))
               pass
    return redirect('get_mail_by_id', id=id)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def mail_edit(request, id):
    if id == 0:
        form = MailForm()
        if request.method == 'POST':
            form = MailForm(request.POST)
            if form.is_valid():
                new_task = form.save()
                return redirect('mail_edit', id=new_task.id)
            else:
                print(form.errors)
        context = {'form': form,
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/mail_edit.html', context=context)
    else:
        mail = Mails.objects.get(pk=id)
        form = MailForm()
        if request.method == 'POST':
            form = MailForm(request.POST, created=mail.created, author=mail.author, completion=mail.completion,
                            type=mail.type, done=mail.done, instance=mail)
            if form.is_valid():
                form.save()
                print('OK')
                return redirect('mail_edit', id=id)
            else:
                print(form.errors)
        for field in mail._meta.fields:
            val = getattr(mail, field.name)
            if 'created' in field.name or 'done' in field.name or 'completion' in field.name or 'date' in field.name:
                if val is not None:
                    form.initial[f'{field.name}'] = val.isoformat()
            else:
                if val is not None:
                    form.initial[f'{field.name}'] = val
        context = {'mail': Mails.objects.get(pk=id),
                   'form': form,
                   'employees': Employees.objects.all(),
                   'user': Employees.objects.filter(user=request.user)[0]}
        return render(request, template_name='core/mail_edit.html', context=context)


@login_required(login_url='login')
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/adminupload")
            response['Content-Disposition'] = 'inline; filename=' + os.path.base_name(file_path)
            return response
    raise Http404
