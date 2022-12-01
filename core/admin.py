from django.contrib import admin

from core.models import ColorBook, ColorTable, ColorSample, Member, ColorOrder, Answer

# Register your models here.

admin.site.register(ColorBook)
admin.site.register(ColorTable)
admin.site.register(ColorSample)
admin.site.register(Member)
admin.site.register(ColorOrder)
admin.site.register(Answer)
