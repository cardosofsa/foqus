from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import PerfilUsuario, Cronograma, Materia, Assunto, Tarefa
from .serializers import CronogramaSerializer, GerarCronogramaSerializer, PerfilUsuarioSerializer, TarefaSerializer

class GerarCronogramaView(APIView):
    """
    Endpoint para gerar um cronograma para o usuário autenticado.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Gera um novo cronograma para o usuário autenticado
        """
        try:
            # Verifica se o perfil do usuário existe
            try:
                perfil = PerfilUsuario.objects.get(usuario=request.user)
            except PerfilUsuario.DoesNotExist:
                return Response(
                    {
                        "error": "Perfil do usuário não encontrado. Complete o cadastro primeiro.",
                        "detalhes": {
                            "codigo": "PERFIL_NAO_ENCONTRADO"
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Valida os dados de entrada
            serializer = GerarCronogramaSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {
                        "error": "Dados de entrada inválidos",
                        "detalhes": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Gera o cronograma
            dados_validados = serializer.validated_data
            cronograma = self._criar_cronograma(request.user, perfil, dados_validados)
            
            # Serializa e retorna o cronograma criado
            response_serializer = CronogramaSerializer(cronograma)
            
            return Response(
                {
                    "message": "Cronograma gerado com sucesso",
                    "cronograma": response_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {
                    "error": "Erro interno ao gerar cronograma",
                    "detalhes": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _criar_cronograma(self, usuario, perfil, dados):
        """Método auxiliar para criar o cronograma"""
        return Cronograma.objects.create(
            usuario=usuario,
            perfil=perfil,
            titulo=dados.get('titulo', 'Novo Cronograma'),
            dados=dados.get('configuracoes', {}),
            data_inicio=dados.get('data_inicio'),
            data_fim=dados.get('data_fim'),
            data_geracao=timezone.now()
        )

    def options(self, request, *args, **kwargs):
        """
        Handler para método OPTIONS
        """
        response = Response()
        response['Allow'] = 'POST, OPTIONS'
        response['Content-Type'] = 'application/json'
        response['Vary'] = 'Accept'
        return response


class ListarCronogramasView(APIView):
    """
    Endpoint para listar cronogramas do usuário autenticado.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cronogramas = Cronograma.objects.filter(usuario=request.user)
        serializer = CronogramaSerializer(cronogramas, many=True)
        return Response({
            "count": cronogramas.count(),
            "cronogramas": serializer.data
        })


class PerfilUsuarioView(APIView):
    """
    Endpoint para gerenciar o perfil do usuário.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            perfil = PerfilUsuario.objects.get(usuario=request.user)
            serializer = PerfilUsuarioSerializer(perfil)
            return Response(serializer.data)
        except PerfilUsuario.DoesNotExist:
            return Response(
                {
                    "error": "Perfil não encontrado",
                    "detalhes": {
                        "codigo": "PERFIL_NAO_ENCONTRADO"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    def post(self, request):
        try:
            perfil = PerfilUsuario.objects.get(usuario=request.user)
            serializer = PerfilUsuarioSerializer(perfil, data=request.data, partial=True)
        except PerfilUsuario.DoesNotExist:
            serializer = PerfilUsuarioSerializer(data=request.data)
        
        if serializer.is_valid():
            perfil = serializer.save(usuario=request.user)
            return Response(PerfilUsuarioSerializer(perfil).data)
        
        return Response(
            {
                "error": "Dados inválidos",
                "detalhes": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class TarefasView(APIView):
    """
    Endpoint para gerenciar tarefas do usuário.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tarefas = Tarefa.objects.filter(usuario=request.user)
        serializer = TarefaSerializer(tarefas, many=True)
        return Response({
            "count": tarefas.count(),
            "tarefas": serializer.data
        })


class MateriasView(APIView):
    """
    Endpoint para listar matérias e assuntos.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from .serializers import MateriaSerializer, AssuntoSerializer
        
        materias = Materia.objects.all()
        assuntos = Assunto.objects.all()
        
        materia_serializer = MateriaSerializer(materias, many=True)
        assunto_serializer = AssuntoSerializer(assuntos, many=True)
        
        return Response({
            "materias": materia_serializer.data,
            "assuntos": assunto_serializer.data
        })