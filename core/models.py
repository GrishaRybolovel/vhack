from django.db import models
from django.conf import settings
import datetime

# Create your models here.

#One to many(Project might have multiple tasks, but task must have only one project)
from django.db.models import QuerySet


class Employees(models.Model):
    name = models.CharField(max_length=63, blank=True, verbose_name='Имя')
    surname = models.CharField(max_length=63, blank=True, verbose_name='Фамилия')
    last_name = models.CharField(max_length=63, blank=True, verbose_name='Отчество')
    phone = models.CharField(max_length=255, blank=True, verbose_name='Телефон')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    date_of_birth = models.DateField(verbose_name='Дата рождения', null=True)
    date_of_start = models.DateField(verbose_name='Дата начала', blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE, null=True)
    ROLE_IN_SYSTEM_CHOICES = [
        ('DI', 'Директор'),
        ('ME', 'Менеджер/Инженер'),
        ('RA', 'Работник'),
        ('BU', 'Бухгалтер'),
        ('RN', 'Руководитель направления'),
        ('KS', 'Кадровый специалист')
    ]
    role = models.CharField(max_length=3,
                            choices=ROLE_IN_SYSTEM_CHOICES,
                            default='RA',
                            verbose_name='Роль',
                            blank=True)
    inn = models.CharField(max_length=256, blank=True, verbose_name='ИНН')
    snils = models.CharField(max_length=256, blank=True, verbose_name='СНИЛС')
    passport = models.TextField(max_length=256, blank=True, verbose_name='Паспорт')
    COMPANY_CHOICES = [
        ('GP', 'ГАЗСПЕЦПРОЕКТ'),
        ('NG', 'Не ГАЗСПЕЦПРОЕКТ')
    ]
    company = models.CharField(max_length=3,
                            choices=COMPANY_CHOICES,
                            default='GP',
                            verbose_name='Компания',
                            blank=True)
    DIVISION_CHOICES = [
        ('GSP', 'ГАЗСПЕЦПРОЕКТ'),
        ('PTO', 'Производственно-технический отдел (ПТО)'),
        ('WGP', 'Водгазпроект')
    ]
    division = models.ForeignKey(
        "Divisions",
        on_delete=models.deletion.PROTECT,
        related_name="employee_to_div",
        null=True,
        blank=True,
        verbose_name='Подразделение'
    )
    leader = models.ForeignKey(
        "self",
        on_delete=models.deletion.CASCADE,
        null=True,
        blank=True,
        verbose_name='Начальник'
    )
    post = models.CharField(max_length=255, blank=True, verbose_name='Должность')
    info_about_relocate = models.TextField(max_length=511, blank=True, verbose_name='Информация о переводе')
    attestation = models.CharField(max_length=255, blank=True, verbose_name='Аттестация')
    qualification = models.CharField(max_length=255, blank=True, verbose_name='Повышение квалификации')
    retraining = models.CharField(max_length=255, blank=True, verbose_name='Проф. подготовка')
    status = models.BooleanField(verbose_name='Статус')


    employee_to_task = models.ManyToManyField(
        "Tasks",
        related_name="employees",
        blank=True,
        verbose_name='Задания'
    )
    employee_to_project = models.ManyToManyField(
        "Projects",
        related_name="projects",
        blank=True,
        verbose_name='Объекты'
    )

    employee_to_document = models.ManyToManyField(
        "Documents",
        related_name="employee_to_doc",
        blank=True,
        verbose_name='Документы'
    )

    employee_to_mail = models.ManyToManyField(
        "Mails",
        related_name="employee_to_mail",
        blank=True,
        verbose_name='Письма'
    )

    @property
    def mails(self) -> QuerySet['Mails']:
        return Mails.objects.filter(employees_to_mails__name=self.name)

    def __str__(self):
        return self.surname + " " + self.name + " " + self.last_name

    def get_role(self):

        if self.role == 'DI':
            return 'Директор'
        if self.role == 'ME':
            return 'Менеджер/Инженер'
        if self.role == 'RA':
            return 'Работник'
        if self.role == 'BU':
            return 'Бухгалтер'
        if self.role == 'RN':
            return 'Руководитель направления'
        if self.role == 'KS':
            return 'Кадровый специалист'

    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Сотрудники'



class Messages(models.Model):
    message = models.TextField(max_length=1024, verbose_name='Сообщение')
    author = models.ForeignKey(
        "Employees",
        on_delete=models.deletion.PROTECT,
        verbose_name='Автор'
    )
    task = models.ForeignKey(
        "Tasks",
        on_delete=models.deletion.PROTECT,
        related_name="messages",
        verbose_name='Задание',
        null=True
    )
    mails_tag = models.ForeignKey(
        "Mails",
        on_delete=models.deletion.PROTECT,
        related_name="messages_to_mails",
        verbose_name='Письмо',
        null=True
    )

    time = models.DateTimeField(auto_now=True)

    doc = models.FileField(null=True, blank=True, upload_to='upload_messages', verbose_name='Документ')

    def __str__(self):
        return self.message

    def has_file(self):
        return bool(self.doc)

    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'



class Tasks(models.Model):
    name = models.CharField(max_length=1023, verbose_name='Задание', blank=True)
    author = models.ForeignKey(
        "Employees",
        on_delete=models.deletion.CASCADE,
        verbose_name='Автор'
    )
    created = models.DateField(verbose_name='Дата создания')
    completion = models.DateField(verbose_name='Срок выполнения')
    done = models.DateTimeField(verbose_name='Дата выполнения', null=True, blank=True)
    projects = models.ForeignKey(
        "Projects",
        on_delete=models.deletion.PROTECT,
        related_name="tasks",
        verbose_name='Проект'
    )

    @property
    def messages(self) -> QuerySet[Messages]:
        return Messages.objects.filter(task__name=self.name).order_by('-author__date_of_birth')

    @property
    def employees(self) -> QuerySet[Employees]:
        return Employees.objects.filter(employee_to_task__name=self.name)

    @property
    def get_type(self):
        if self.done:
            return 0
        if self.projects.proj_type == 'EXP':
            if self.completion >= datetime.date.today():
                return 1
            else:
                return 2

        if self.projects.proj_type == 'TO':
            if self.completion >= datetime.date.today():
                return 3
            else:
                return 4

        if self.projects.proj_type == 'SMR':
            if self.completion >= datetime.date.today():
                return 5
            else:
                return 6

        if self.projects.proj_type == 'PRO':
            if self.completion >= datetime.date.today():
                return 7
            else:
                return 8

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Задачи'
        verbose_name_plural = 'Задачи'



class Mails(models.Model):
    name = models.CharField(max_length=1023, verbose_name='Описание')
    naming = models.CharField(max_length=1023, verbose_name='Наименование отправителя/получателя')
    created = models.DateField(verbose_name='Дата создания', auto_now=True)
    date_reg = models.DateField(verbose_name='Дата регистрации')
    number = models.CharField(max_length=1023, verbose_name='Номер')
    author = models.ForeignKey(
        "Employees",
        on_delete=models.deletion.CASCADE,
        verbose_name='Автор'
    )
    completion = models.DateField(verbose_name='Срок выполнения', null=True, blank=True)
    done = models.DateField(verbose_name='Дата выполнения', null=True, blank=True)
    type = models.CharField(max_length=256, verbose_name='Тип')
    projects_to_mails = models.ForeignKey(
        "Projects",
        on_delete=models.deletion.CASCADE,
        related_name="projects_to_mails",
        null=True,
        blank=True,
        verbose_name="Объект"
    )

    @property
    def messages(self) -> QuerySet[Messages]:
        return Messages.objects.filter(mails_tag__name=self.name)

    @property
    def employees(self) -> QuerySet[Employees]:
        return Employees.objects.filter(employee_to_mail__name=self.name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Письма'
        verbose_name_plural = 'Письма'



class Projects(models.Model):
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
    proj_type = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        default='EXP',
        verbose_name='Статус объекта'
    )

    name = models.CharField(max_length=255, verbose_name='Название')
    reg_num = models.CharField(max_length=255, verbose_name='Регистрационный № ОПО')
    contract = models.CharField(max_length=255, blank=True, verbose_name='Договор')
    date_creation = models.DateField(verbose_name='Дата договора')
    date_notification = models.DateField(verbose_name='Дата(для оповещения)')
    object_type = models.CharField(max_length=255, blank=True, verbose_name='Тип объекта')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    contact = models.CharField(max_length=255, blank=True, verbose_name='Контактный человек')
    phone = models.CharField(max_length=255, blank=True, verbose_name='Контактный телефон')
    email = models.CharField(max_length=255, blank=True, verbose_name='Контактный e-mail')
    status = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default='IWrk',
        verbose_name='Статус объекта'
    )
    seasoning = models.CharField(
        max_length=4,
        choices=SEASONING_CHOICES,
        default='Seas',
        verbose_name='Сезонность'
    )
    cost = models.IntegerField(blank=True, null=True, verbose_name='Цена обслуживания')

    project_to_document = models.ManyToManyField(
        "Documents",
        related_name="project_to_doc",
        blank=True,
        verbose_name='Документы'
    )

    def __str__(self):
        return self.name

    #One to many Tasks
    #Many to many Employees
    @property
    def tasks(self) -> QuerySet[Tasks]:
        f = Tasks.objects.filter(projects__name=self.name)
        return f

    @property
    def employee(self) -> QuerySet[Tasks]:
        f = Employees.objects.filter(employee_to_project__name=self.name)
        return f

    @property
    def mail(self) -> QuerySet[Tasks]:
        f = Mails.objects.filter(projects_to_mails__name=self.name)
        return f

    class Meta:
        verbose_name = 'Объекты'
        verbose_name_plural = 'Объекты'


class Documents(models.Model):

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

    name = models.CharField(max_length=255, verbose_name='Наименование документа')
    status = models.CharField(max_length=4,
                              choices=ROLE_IN_SYSTEM_CHOICES,
                              default='CU',
                              verbose_name='Статус')
    doc_type = models.CharField(max_length=100,
                                choices=TYPE_CHOICES,
                                default='01',
                                verbose_name='Тип')
    duration = models.DateField(verbose_name='Срок действия')
    doc = models.FileField(upload_to='uploads/', verbose_name='Документ')

    def __str__(self):
        return self.name

    @property
    def employees(self) -> QuerySet['Employees']:
        return self.employee_to_doc.all()

    @property
    def projects(self) -> QuerySet['Projects']:
        return self.project_to_doc.all()

    class Meta:
        verbose_name = 'Документы'
        verbose_name_plural = 'Документы'


class Divisions(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название подразделения')
    parent_division = models.ForeignKey(
        "Divisions",
        on_delete=models.deletion.PROTECT,
        blank=True,
        null=True,
        related_name="parent_div",
        verbose_name='Родительское подразделение'
    )

    @property
    def divis(self) -> QuerySet['Divisions']:
        return Divisions.objects.filter(parent_div__name=self.name)

    @property
    def del_check(self) -> QuerySet['Divisions']:
        return Divisions.objects.filter(parent_division=self)

    @property
    def employees(self) -> QuerySet['Employees']:
        return Employees.objects.filter(division__name=self.name)

    @property
    def employees_amount(self) -> QuerySet['Employees']:
        return Employees.objects.filter(division__name=self.name).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

class CompanyDocuments(models.Model):
    company_to_document = models.ManyToManyField(
        "Documents",
        related_name="company_to_doc",
        blank=True,
        verbose_name='Документы'
    )

    class Meta:
        verbose_name = 'Документация компании'
        verbose_name_plural = 'Документация компании'