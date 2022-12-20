from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
import xlwt
import pandas as pd

from core.forms import MemberForm, AnswerForm, UpdateForm
from core.models import ColorTable, ColorSample, Member, ColorOrder, Answer, Update, ColorBook, ImgSample


# Create your views here.

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def experiments(request):
    return render(request, 'experiments.html')


def start_img(request):
    """Начать тестирование с картинками"""
    message = "Для начала эксперимента введите имя"
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)  # Выгрузить
        if form.is_valid():
            member = Member(name=request.POST['name'], duration=request.POST['duration'], experiment="Картинки")
            member.save()  # Сохранить

            first_table = ImgSample.objects.get(num=1, first=True)
            return redirect('img_table', img_pk=first_table.num, member_pk=member.pk)
        else:
            message = 'Форма не корректна. Пожалуйста, исправьте ошибки'
    else:
        form = MemberForm()  # Пустая, незаполненная форма

    context = {'form': form, 'message': message}
    return render(request, 'start_img.html', context)


def start_test(request):
    """Начать тестирование с таблицами"""
    message = "Для начала эксперимента введите имя"
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)  # Выгрузить
        if form.is_valid():
            member = Member(name=request.POST['name'], duration=request.POST['duration'], experiment="Таблицы")
            member.save()  # Сохранить

            tables = list(ColorTable.objects.all())  # Получить все таблицы
            random_tables = random.sample(tables, 17)  # Выбрать из всех 17 случайных таблиц

            for i in range(len(random_tables)):
                table = random_tables[i]
                order = ColorOrder(member=member, table=table, position=i + 1)  # Элемент последовательности
                order.save()  # Сохранить

            return redirect('color_table', table_pk=1, member_pk=member.pk)
        else:
            message = 'Форма не корректна. Пожалуйста, исправьте ошибки'
    else:
        form = MemberForm()  # Пустая, незаполненная форма

    context = {'form': form, 'message': message}
    return render(request, 'start_matyushin.html', context)


def img_table(request, img_pk, member_pk):
    """Таблица с картинками"""
    duration = Member.objects.get(pk=member_pk).duration
    img_pk = int(img_pk)
    if img_pk <= 36:
        img = ImgSample.objects.get(num=img_pk, first=True)
        next_position = img_pk + 1
        context = {'member_pk': member_pk, 'duration': duration, 'img': img, 'next_position': next_position}
        return render(request, 'img.html', context=context)
    else:
        context = {'next_table': 1, 'member_pk': member_pk}
        return render(request, 'faq_img.html', context)


def color_table(request, table_pk, member_pk):
    """Показать таблицу Матюшина"""
    table = ColorTable.objects.get(pk=table_pk)
    duration = Member.objects.get(pk=member_pk).duration

    sample_up = ColorSample.objects.get(table=table, position='верх')
    sample_mid = ColorSample.objects.get(table=table, position='центр')
    sample_down = ColorSample.objects.get(table=table, position='низ')

    hex_up = rgb_to_hex((sample_up.R, sample_up.G, sample_up.B))
    hex_mid = rgb_to_hex((sample_mid.R, sample_mid.G, sample_mid.B))
    hex_down = rgb_to_hex((sample_down.R, sample_down.G, sample_down.B))

    cur_position = ColorOrder.objects.get(member=member_pk, table=table_pk).position
    next_position = cur_position + 1
    if next_position <= 17:
        next_table = ColorOrder.objects.get(member=member_pk, position=next_position).table.pk

        context = {'hex_up': hex_up, 'hex_mid': hex_mid, 'hex_down': hex_down, 'next_table': next_table,
                   'member_pk': member_pk, 'duration': duration}

        return render(request, 'color.html', context)

    else:
        context = {'next_table': 1, 'member_pk': member_pk}
        return render(request, 'faq.html', context)


def memory_test(request, table_pk, member_pk):
    """Тест с картинками"""
    tables = list(ColorTable.objects.all())
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)  # Выгрузить
        if form.is_valid():
            member = Member.objects.get(pk=member_pk)

            table = ColorTable.objects.get(name=tables[int(table_pk) - 1])
            was_shown = ColorOrder.objects.filter(member=member_pk, table=table_pk).exists()
            answer = Answer(answer=request.POST['answer'],
                            member=member,
                            table=table,
                            was_shown=was_shown)  # Заполнить
            answer.save()  # Сохранить

            next_table = int(table_pk) + 1
            if next_table <= 34:
                return redirect('memory_test', table_pk=next_table, member_pk=member_pk)
            else:
                return render(request, 'end.html')
    else:
        form = AnswerForm()

    table = ColorTable.objects.get(name=tables[int(table_pk) - 1])

    sample_up = ColorSample.objects.get(table=table, position='верх')
    sample_mid = ColorSample.objects.get(table=table, position='центр')
    sample_down = ColorSample.objects.get(table=table, position='низ')

    hex_up = rgb_to_hex((sample_up.R, sample_up.G, sample_up.B))
    hex_mid = rgb_to_hex((sample_mid.R, sample_mid.G, sample_mid.B))
    hex_down = rgb_to_hex((sample_down.R, sample_down.G, sample_down.B))

    context = {'hex_up': hex_up, 'hex_mid': hex_mid, 'hex_down': hex_down,
               'member_pk': member_pk, 'form': form, 'table_pk': table_pk}

    return render(request, 'memory_test.html', context)


def img_test(request, table_pk, member_pk):
    """Тест на память"""
    member = Member.objects.get(pk=member_pk)
    table_pk = int(table_pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)  # Выгрузить
        if form.is_valid():
            img = ImgSample.objects.get(num=table_pk, second=True)
            was_shown = (table_pk <= 36)
            answer = Answer(answer=request.POST['answer'],
                            member=member,
                            image=img,
                            was_shown=was_shown)  # Заполнить
            answer.save()  # Сохранить

            next_table = table_pk + 1
            if next_table <= 72:
                return redirect('img_test', table_pk=next_table, member_pk=member_pk)
            else:
                return render(request, 'end.html')
    else:
        form = AnswerForm()

    img = ImgSample.objects.get(num=table_pk, second=True)

    context = {'img': img, 'member_pk': member_pk, 'form': form, 'table_pk': table_pk}

    return render(request, 'img_test.html', context)


def export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Canvas.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('canvas list')  # this will make a sheet named Users Data
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['id ответа', 'id участника', 'Имя участника', 'Название таблицы', 'Ответ участника', 'Был показан']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Answer.objects.values_list('pk', 'member_id', 'member__name', 'table__name', 'answer', 'was_shown')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


def update_database(request):
    """Обновить базу данных"""
    if not request.user.is_authenticated:
        return redirect("index")

    message = 'Выберите файл обновления'
    # Обработка загрузки файла
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES)  # Получение данных с формы
        if form.is_valid():
            newdoc = Update(docfile=request.FILES['docfile'])  # Создание объекта обновления

            book_df = pd.read_excel(newdoc.docfile, "Тетради")
            table_df = pd.read_excel(newdoc.docfile, "Таблицы")
            sample_df = pd.read_excel(newdoc.docfile, "Образцы")
            img_df = pd.read_excel(newdoc.docfile, "Картинки")
            img_df["Первые"] = img_df["Первые"].replace({1: True, 0: False})
            img_df["Вторые"] = img_df["Вторые"].replace({1: True, 0: False})

            for i in range(book_df.shape[0]):
                """Загружаем тетради"""
                book = ColorBook(name=book_df.iloc[i]["Название"])
                book.save()

            for i in range(table_df.shape[0]):
                """Загружаем таблицы"""
                qu = table_df.iloc[i]
                book = ColorBook.objects.get(name=qu["Тетрадь"])
                table = ColorTable(name=qu["Название"], book=book)
                table.save()

            for i in range(sample_df.shape[0]):
                """Загружаем Образцы"""
                qu = sample_df.iloc[i]
                table = ColorTable.objects.get(name=qu["Таблица"])
                sample = ColorSample(table=table, position=qu["Позиция"].strip(), R=qu["R"], G=qu["G"], B=qu["B"])
                sample.save()

            for i in range(img_df.shape[0]):
                """Загружаем Картинки"""
                qu = img_df.iloc[i]
                img = ImgSample(num=qu["ID"], zv=qu["Цвет"], typ=qu["Тип"], vid=qu["Вид"], priz=qu["Признак"],
                                url=qu["Ссылка"], first=qu["Первые"], second=qu["Вторые"])
                img.save()

            newdoc.save()  # Сохранение тренировки

            # Перенаправление на главную страницу
            return redirect('start_test')
        else:
            message = 'Форма не корректна. Пожалуйста исправьте следующие ошибки:'
    else:
        form = UpdateForm()  # Пустая незаполненная форма

    count_books = ColorBook.objects.all().count()
    # Отображение страницы обновления
    context = {'form': form, 'message': message, 'count_books': count_books}
    return render(request, 'update_database.html', context)
