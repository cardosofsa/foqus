from django.urls import path
from .views import (
    GerarCronogramaView,
    ListarCronogramasView,
    PerfilUsuarioView,
    TarefasView,
    MateriasView
)

app_name = 'core'

urlpatterns = [
    # Cronograma
    path('api/gerar-cronograma/', GerarCronogramaView.as_view(), name='gerar-cronograma'),
    path('api/cronogramas/', ListarCronogramasView.as_view(), name='listar-cronogramas'),
    
    # Perfil
    path('api/perfil/', PerfilUsuarioView.as_view(), name='perfil-usuario'),
    
    # Tarefas
    path('api/tarefas/', TarefasView.as_view(), name='tarefas'),
    
    # Matérias e Assuntos
    path('api/materias/', MateriasView.as_view(), name='materias'),
]