from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='perfil'
    )
    data_inicio_estudos = models.DateField(default=timezone.now)
    data_prova = models.DateField(default=timezone.now)
    horas_por_dia = models.IntegerField(default=1)
    
    def __str__(self):
        return f"Perfil de {self.usuario.username}"

class Materia(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Assunto(models.Model):
    nome = models.CharField(max_length=100)
    materia = models.ForeignKey(
        Materia, 
        on_delete=models.CASCADE, 
        related_name='assuntos'
    )
    incidencia = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.nome} ({self.materia.nome})"

class Tarefa(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluido', 'Concluído'),
    ]
    
    assunto = models.ForeignKey(
        Assunto, 
        on_delete=models.CASCADE, 
        related_name='tarefas'
    )
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tarefas'
    )
    data_prevista = models.DateField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pendente'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.assunto.nome} - {self.usuario.username}"

class Cronograma(models.Model):
    usuario = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='cronogramas'
    )
    perfil = models.ForeignKey(
        PerfilUsuario, 
        on_delete=models.CASCADE, 
        related_name='cronogramas'
    )
    titulo = models.CharField(max_length=255, default="Novo Cronograma")
    dados = models.JSONField(default=dict)
    data_geracao = models.DateTimeField(default=timezone.now)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-data_geracao']
    
    def __str__(self):
        return f"Cronograma {self.titulo} - {self.usuario.username}"