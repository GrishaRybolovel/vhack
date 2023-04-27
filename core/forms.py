from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Projects, Employees, Documents, Messages, Divisions, Tasks, Mails

class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control form-control-user'}), max_length=255)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                          'class': 'form-control form-control-user'}), max_length=255)
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password',
                                                              'class': 'form-control form-control-user'}), max_length=255)
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Repeat Password',
                                                              'class': 'form-control form-control-user'}), max_length=255)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.project = kwargs.pop('project', None)
        super(TaskForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(TaskForm, self).save(commit=False)

        obj.projects = self.project
        obj.author = self.author
        if commit:
            obj.save()
        return obj

    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Название',
                                                                         'class': 'form-control'}), max_length=255)
    created = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y',
                                                                           attrs={'class' : 'form-control icon-calendar',
                                                                                  'type' : 'date'}))
    completion = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y',
                                                                           attrs={'class' : 'form-control icon-calendar',
                                                                                  'type' : 'date'}))
    done = forms.DateTimeField(required=False, widget=forms.DateInput(format='%d/%m/%Y',
                                                          attrs={'class': 'form-control icon-calendar',
                                                                 'type': 'date'}))
    class Meta:
        model = Tasks
        fields = ['name', 'created', 'completion', 'done']


class ProjectForm(ModelForm):
    STATUS_CHOICES = [
        ('IWrk', 'В работе'),
        ('PNR', 'ПНР'),
        ('SOff', 'Сезон откл.'),
        ('SMR', 'СМР'),
        ('AOff', 'Аварийное откл.')
    ]
    SEASONING_CHOICES = [
        ('Seas', 'Сезонная'),
        ('Fyea', 'Круглогодичная')
    ]
    TYPE_CHOICES = [
        ('EXP', 'Эксплуатация'),
        ('TO', 'Техническое обслуживание'),
        ('SMR', 'СМР'),
        ('PRO', 'Производство')
    ]
    proj_type = forms.ChoiceField(required=False, choices=TYPE_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Название',
                                                             'class': 'form-control'}), max_length=255)
    reg_num = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Регистрационный № ОПО',
                                                                         'class': 'form-control'}), max_length=255)
    contract = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Договор',
                                                             'class': 'form-control'}), max_length=255)
    date_creation = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y',
                                                                           attrs={'class' : 'form-control icon-calendar',
                                                                                  'type' : 'date'}))
    date_notification = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y',
                                                                               attrs={'class' : 'form-control',
                                                                                      'type' : 'date'}))
    object_type = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Тип объекта',
                                                             'class': 'form-control'}), max_length=255)
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Адрес',
                                                             'class': 'form-control'}), max_length=255)
    contact = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Контактный человек',
                                                             'class': 'form-control'}), max_length=255)
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Контактный телефон',
                                                             'class': 'form-control'}), max_length=255)
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Контактный e-mail',
                                                             'class': 'form-control'}), max_length=255)
    status = forms.ChoiceField(required=False, choices=STATUS_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    seasoning = forms.ChoiceField(required=False, choices=SEASONING_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    cost = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Цена обслуживания',
                                                             'class': 'form-control'}))
    class Meta:
        model = Projects
        fields = ['name', 'proj_type', 'contract', 'date_creation', 'date_notification', 'object_type', 'address',
                  'contact', 'phone', 'email', 'status', 'seasoning', 'cost']


class DocumentForm(ModelForm):
    ROLE_IN_SYSTEM_CHOICES = [
        ('WO', 'Без статуса'),
        ('CH', 'Черновик'),
        ('NS', 'На согласовании'),
        ('CU', 'Действующий'),
        ('CO', 'Завершённый'),
        ('RA', 'Расторгнутый'),
        ('AN', 'Аннулированный')
    ]
    TYPE_CHOICES = [
        ('01', 'Договор'),
        ('02', 'Регистрация объекта в государственном реестре'),
        ('03', 'Правоустанавливающие документы'),
        ('04', 'Проектные документы'),
        ('05', 'Экспертиза'),
        ('06', 'Страхование'),
        ('07', 'Разрешительные документы и акты ввода в эксплуатацию'),
        ('08', 'Исполнительно-техническая документация по строительству'),
        ('09', 'Эксплуатационные документы'),
        ('10', 'Обучение персонала'),
        ('11', 'Документы сезонные в эксплуатационный период'),
        ('12', 'Нормативно-правовые акты'),
        ('13', 'Иные документы')
    ]

    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Наименование документа',
                                                             'class': 'form-control'}), max_length=255)
    status = forms.ChoiceField(required=False, choices=ROLE_IN_SYSTEM_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    doc_type = forms.ChoiceField(required=False, choices=TYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    duration = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y',
                                                                               attrs={'class' : 'form-control',
                                                                                      'type' : 'date'}))
    doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = Documents
        fields = ['name', 'status', 'doc_type', 'duration', 'doc']


class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.task = kwargs.pop('task', None)
        self.author = kwargs.pop('author', None)
        super(MessageForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(MessageForm, self).save(commit=False)
        obj.task = self.task
        obj.author = self.author
        if commit:
            obj.save()
        return obj

    message = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Текст сообщения',
                                                                  'class': 'form-control'}), max_length=1024)
    doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Messages
        fields = ['message', 'doc']


class MessageMailForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.mails_tag = kwargs.pop('mails_tag', None)
        self.author = kwargs.pop('author', None)
        super(MessageMailForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(MessageMailForm, self).save(commit=False)
        obj.mails_tag = self.mails_tag
        obj.author = self.author
        if commit:
            obj.save()
        return obj

    message = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Текст сообщения',
                                                                  'class': 'form-control'}), max_length=1024)
    doc = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Messages
        fields = ['message', 'doc']


class MailForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.created = kwargs.pop('created', None)
        self.author = kwargs.pop('author', None)
        self.completion = kwargs.pop('completion', None)
        self.type = kwargs.pop('type', None)
        self.done = kwargs.pop('done', None)
        super(MailForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super(MailForm, self).save(commit=False)
        obj.created = self.created
        obj.author = self.author
        obj.completion = self.completion
        obj.type = self.type
        obj.done = self.done

        if commit:
            obj.save()
        return obj

    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Название',
                                                             'class': 'form-control'}), max_length=255)
    naming = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Наименование отправителя/получателя',
                                                                         'class': 'form-control'}), max_length=255)
    date_reg = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y',
                                                                     attrs={'class': 'form-control icon-calendar',
                                                                            'type': 'date'}))
    number = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Номер',
                                                             'class': 'form-control'}), max_length=255)

    class Meta:
        model = Mails
        fields = ['name', 'naming', 'date_reg', 'number']


class EmployeeForm(ModelForm):
    ROLE_IN_SYSTEM_CHOICES = [
        ('DI', 'Директор'),
        ('ME', 'Менеджер/Инженер'),
        ('RA', 'Работник'),
        ('BU', 'Бухгалтер'),
        ('RN', 'Руководитель направления'),
        ('KS', 'Кадровый специалист')
    ]
    COMPANY_CHOICES = [
        ('GP', 'ГАЗСПЕЦПРОЕКТ'),
        ('NG', 'Не ГАЗСПЕЦПРОЕКТ')
    ]
    DIVISION_CHOICES = [
        ('GSP', 'ГАЗСПЕЦПРОЕКТ'),
        ('PTO', 'Производственно-технический отдел (ПТО)'),
        ('WGP', 'Водгазпроект')
    ]
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Имя',
                                                             'class': 'form-control'}), max_length=255)
    surname = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Фамилия',
                                                                         'class': 'form-control'}), max_length=255)
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Отчество',
                                                                         'class': 'form-control'}), max_length=255)
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Номер телефона',
                                                                         'class': 'form-control'}), max_length=255)
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Адрес',
                                                                          'class': 'form-control'}), max_length=255)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(format='%d/%m/%Y',
                                                                           attrs={'class' : 'form-control icon-calendar',
                                                                                  'type' : 'date'}))
    date_of_start = forms.DateField(required=False, widget=forms.DateInput(format='%d/%m/%Y',
                                                                               attrs={'class' : 'form-control',
                                                                                      'type' : 'date'}))
    role = forms.ChoiceField(required=False, choices=ROLE_IN_SYSTEM_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    inn = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'ИНН',
                                                             'class': 'form-control'}), max_length=255)
    snils = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'СНИЛС',
                                                             'class': 'form-control'}), max_length=255)
    passport = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Паспорт',
                                                             'class': 'form-control'}), max_length=255)
    company = forms.ChoiceField(required=False, choices=COMPANY_CHOICES,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    division = forms.ModelChoiceField(required=False, queryset=Divisions.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    post = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Должность',
                                                                            'class': 'form-control'}), max_length=255)
    info_about_relocate = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Информация о переводе',
                                                                            'class': 'form-control'}), max_length=255)
    attestation = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Аттестация',
                                                                            'class': 'form-control'}), max_length=255)
    qualification = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Повышение квалификации',
                                                                            'class': 'form-control'}), max_length=255)
    retraining = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Проф. подготовка',
                                                                            'class': 'form-control'}), max_length=255)
    status = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'placeholder': 'Статус',
                                                                            'class': 'form-control'}))
    class Meta:
        model = Employees
        fields = ['name', 'surname', 'last_name', 'phone', 'address', 'date_of_birth', 'date_of_start',
                  'role', 'inn', 'snils', 'passport', 'company', 'division', 'leader', 'post', 'info_about_relocate',
                  'attestation', 'qualification', 'retraining', 'status']
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'Повышение квалификации',
                                                                  'class': 'form-control'}), max_length=255)
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Проф. подготовка',
                                                                               'class': 'form-control'}),
                                 max_length=255)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class DivisionForm(forms.ModelForm):
    name = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': 'Повышение квалификации',
                                                                  'class': 'form-control'}), max_length=255)
    parent_division = forms.ModelChoiceField(required=False, queryset=Divisions.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Divisions
        fields = ['name', 'parent_division']