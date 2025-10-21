from django.contrib import admin
from .models import Materia, Assunto, Tarefa, PerfilUsuario

# O decorator @admin.register é uma forma moderna de registrar modelos
@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Assunto)
class AssuntoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'materia', 'incidencia')
    search_fields = ('nome',)
    list_filter = ('materia',)
    list_editable = ('incidencia',)

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('assunto', 'usuario', 'data_prevista', 'status')
    search_fields = ('assunto__nome', 'usuario__username')
    list_filter = ('status', 'data_prevista', 'usuario')
    list_editable = ('status',)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_inicio_estudos', 'data_prova', 'horas_por_dia')
