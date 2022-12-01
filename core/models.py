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

    def __str__(self):
        return "{0} {1}".format(self.name, self.pk)


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
    answer = models.BooleanField()
    was_shown = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.member, self.table, self.answer, self.was_shown)


class Update(models.Model):
    """Обновление таблиц"""
    docfile = models.FileField(upload_to='update/%Y/%m/%d',
                               verbose_name="Файл обновления", null=True, blank=True)
