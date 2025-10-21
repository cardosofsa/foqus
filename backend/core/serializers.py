from rest_framework import serializers
from .models import PerfilUsuario, Cronograma, Materia, Assunto, Tarefa

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = [
            'id', 'usuario', 'data_inicio_estudos', 'data_prova', 'horas_por_dia'
        ]
        read_only_fields = ['id', 'usuario']

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ['id', 'nome']

class AssuntoSerializer(serializers.ModelSerializer):
    materia_nome = serializers.CharField(source='materia.nome', read_only=True)
    
    class Meta:
        model = Assunto
        fields = ['id', 'nome', 'materia', 'materia_nome', 'incidencia']

class TarefaSerializer(serializers.ModelSerializer):
    assunto_nome = serializers.CharField(source='assunto.nome', read_only=True)
    
    class Meta:
        model = Tarefa
        fields = [
            'id', 'assunto', 'assunto_nome', 'usuario', 
            'data_prevista', 'status', 'data_criacao'
        ]
        read_only_fields = ['id', 'usuario', 'data_criacao']

class CronogramaSerializer(serializers.ModelSerializer):
    perfil_info = PerfilUsuarioSerializer(source='perfil', read_only=True)
    
    class Meta:
        model = Cronograma
        fields = [
            'id', 'titulo', 'dados', 'data_geracao', 
            'data_inicio', 'data_fim', 'ativo', 'perfil_info'
        ]
        read_only_fields = ['id', 'data_geracao', 'perfil_info']

class GerarCronogramaSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=255, required=False, default="Novo Cronograma")
    data_inicio = serializers.DateField(required=False)
    data_fim = serializers.DateField(required=False)
    configuracoes = serializers.JSONField(required=False, default=dict)
    
    def validate(self, data):
        data_inicio = data.get('data_inicio')
        data_fim = data.get('data_fim')
        
        if data_inicio and data_fim:
            if data_inicio > data_fim:
                raise serializers.ValidationError({
                    "error": "Data de início não pode ser posterior à data de fim",
                    "codigo": "DATA_INVALIDA"
                })
        
        return data