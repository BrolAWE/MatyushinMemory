from django.http import HttpResponse
from django.shortcuts import render, redirect
import random
import xlwt

from core.forms import MemberForm, AnswerForm
from core.models import ColorTable, ColorSample, Member, ColorOrder, Answer


# Create your views here.

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def start_test(request):
    """Начать тестирование"""
    message = "Для начала эксперимента введите имя"
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)  # Выгрузить
        if form.is_valid():
            member = Member(name=request.POST['name'])  # Заполнить
            member.save()  # Сохранить

            tables = list(ColorTable.objects.all())  # Получить все таблицы
            random_tables = random.sample(tables, 17)  # Выбрать из всех 17 случайных таблиц

            for i in range(len(random_tables)):
                table = random_tables[i]
                order = ColorOrder(member=member, table=table, position=i + 1)  # Элемент последовательности
                order.save()  # Сохранить

            first_table = ColorTable.objects.get(name=random_tables[0])
            return redirect('color_table', table_pk=first_table.pk, member_pk=member.pk)
        else:
            message = 'Форма не корректна. Пожалуйста, исправьте ошибки'
    else:
        form = MemberForm()  # Пустая, незаполненная форма

    context = {'form': form, 'message': message}
    return render(request, 'start.html', context)


def color_table(request, table_pk, member_pk):
    """Показать таблицу Матюшина"""
    table = ColorTable.objects.get(pk=table_pk)

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
                   'member_pk': member_pk}

        return render(request, 'color.html', context)

    else:
        context = {'next_table': 1, 'member_pk': member_pk}
        return render(request, 'faq.html', context)


def memory_test(request, table_pk, member_pk):
    """Тест на память"""
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)  # Выгрузить
        if form.is_valid():
            member = Member.objects.get(pk=member_pk)
            table = ColorTable.objects.get(pk=table_pk)
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

    table = ColorTable.objects.get(pk=table_pk)

    sample_up = ColorSample.objects.get(table=table, position='верх')
    sample_mid = ColorSample.objects.get(table=table, position='центр')
    sample_down = ColorSample.objects.get(table=table, position='низ')

    hex_up = rgb_to_hex((sample_up.R, sample_up.G, sample_up.B))
    hex_mid = rgb_to_hex((sample_mid.R, sample_mid.G, sample_mid.B))
    hex_down = rgb_to_hex((sample_down.R, sample_down.G, sample_down.B))

    context = {'hex_up': hex_up, 'hex_mid': hex_mid, 'hex_down': hex_down,
               'member_pk': member_pk, 'form': form, 'table_pk': table_pk}

    return render(request, 'memory_test.html', context)


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
