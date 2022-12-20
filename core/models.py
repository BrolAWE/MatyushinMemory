from django.db import models

POSITION = (
    ('верх', 'верх'),
    ('центр', 'центр'),
    ('низ', 'низ'),
)

ANSWER = (
    ('да', 'да'),
    ('нет', 'нет'),
)

TYP = (
    ('И', 'И'),
    ('Е', 'Е'),
    ('А', 'А'),
    ('П', 'П'),
)

ZV = (
    ('Ц', 'Ц'),
    ('Б', 'Б')
)

VID = (
    ('Садово-парковая архитектура', 'Садово-парковая архитектура'),
    ('Русские усадьбы', 'Русские усадьбы'),
    ('Мозаики', 'Мозаики'),
    ('Городская скульптура', 'Городская скульптура'),
    ('Поток машин', 'Поток машин'),
    ('Праздничное оформление', 'Праздничное оформление'),
    ('Городская реклама', 'Городская реклама'),
    ('Индустриальный пейзаж', 'Индустриальный пейзаж'),
    ('Панельные дома', 'Панельные дома'),
    ('Граффити', 'Граффити'),
    ('Рисовые террасы', 'Рисовые террасы'),
    ('Возделанные поля', 'Возделанные поля'),
    ('Деревня', 'Деревня'),
    ('Город с зеленью', 'Город с зеленью'),
    ('Северный поселок', 'Северный поселок'),
    ('Панорама города', 'Панорама города'),
    ('Исторический центр', 'Исторический центр'),
    ('Мекка', 'Мекка'),
    ('Бородинское поле', 'Бородинское поле'),
    ('Церковь', 'Церковь'),
    ('Рядовая застройка', 'Рядовая застройка'),
    ('Портреты зданий', 'Портреты зданий'),
)

PRIZ = (
    ('Основной', 'Основной'),
    ('Дублёр', 'Дублёр'),
)


# Create your models here.


class ColorBook(models.Model):
    """Цветовая книга"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{0}".format(self.name)


class ColorTable(models.Model):
    """Цветовая таблица"""
    book = models.ForeignKey(ColorBook, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{0}".format(self.name)


class ImgSample(models.Model):
    """Образец с картинкой"""
    num = models.IntegerField()
    zv = models.CharField(max_length=50, choices=ZV, null=True, blank=True)
    typ = models.CharField(max_length=50, choices=TYP)
    vid = models.CharField(max_length=50, choices=VID)
    priz = models.CharField(max_length=50, choices=PRIZ)
    url = models.URLField()
    first = models.BooleanField(null=True, blank=True)
    second = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{0} {1}".format(self.num, self.zv)


class ColorSample(models.Model):
    """Цветовой образец"""
    table = models.ForeignKey(ColorTable, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=50, choices=POSITION)
    R = models.IntegerField()
    G = models.IntegerField()
    B = models.IntegerField()

    def __str__(self):
        return "{0} {1}".format(self.table, self.position)


class Member(models.Model):
    """Участник эксперимента"""
    name = models.CharField(max_length=50)
    duration = models.IntegerField(verbose_name="Длительность в мс", default=2000)
    experiment = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "{0} {1} {2}".format(self.name, self.pk, self.experiment)


class ColorOrder(models.Model):
    """Порядок цветов"""
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey(ColorTable, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.IntegerField()

    def __str__(self):
        return "{0} {1}".format(self.member, self.position)


class Answer(models.Model):
    """Ответ участника"""
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey(ColorTable, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ForeignKey(ImgSample, on_delete=models.SET_NULL, null=True, blank=True)
    answer = models.BooleanField()
    was_shown = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.member, self.table, self.answer, self.was_shown)


class Update(models.Model):
    """Обновление таблиц"""
    docfile = models.FileField(upload_to='update/%Y/%m/%d',
                               verbose_name="Файл обновления", null=True, blank=True)
