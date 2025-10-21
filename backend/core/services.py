import logging
from datetime import timedelta
from django.utils import timezone
from .models import PerfilUsuario, Tarefa, Assunto, Materia

logger = logging.getLogger(__name__)

def gerar_cronograma_para_usuario(usuario):
    """
    Gera um cronograma personalizado para o usuário baseado em:
    - Data da prova
    - Horas disponíveis por dia
    - Assuntos por matéria
    - Princípio de Pareto (80/20)
    """
    try:
        # Verificar se o usuário tem perfil
        try:
            perfil = usuario.perfil
        except PerfilUsuario.DoesNotExist:
            return {
                "sucesso": False,
                "mensagem": "Perfil do usuário não encontrado. Complete o onboarding primeiro.",
                "detalhes": {"codigo": "PERFIL_NAO_ENCONTRADO"}
            }

        # Validar dados necessários
        if not perfil.data_prova:
            return {
                "sucesso": False,
                "mensagem": "Data da prova não definida.",
                "detalhes": {"codigo": "DATA_PROVA_NAO_DEFINIDA"}
            }

        # Calcular dias disponíveis
        hoje = timezone.now().date()
        dias_para_prova = (perfil.data_prova - hoje).days
        
        if dias_para_prova <= 0:
            return {
                "sucesso": False,
                "mensagem": "A data da prova já passou ou é hoje.",
                "detalhes": {"codigo": "DATA_PROVA_INVALIDA"}
            }

        # Obter todos os assuntos ordenados por incidência (Pareto)
        assuntos = Assunto.objects.all().order_by('-incidencia')
        
        if not assuntos.exists():
            return {
                "sucesso": False,
                "mensagem": "Nenhum assunto cadastrado no sistema.",
                "detalhes": {"codigo": "ASSUNTOS_NAO_ENCONTRADOS"}
            }

        # Limpar tarefas existentes do usuário
        Tarefa.objects.filter(usuario=usuario).delete()

        # Lógica simplificada de distribuição (implementar algoritmo mais sofisticado depois)
        tarefas_criadas = []
        data_atual = hoje
        
        for assunto in assuntos[:20]:  # Limitar aos 20 assuntos mais importantes
            # Criar tarefa para este assunto
            tarefa = Tarefa.objects.create(
                usuario=usuario,
                assunto=assunto,
                data_prevista=data_atual,
                prioridade=5 - (assunto.incidencia // 20)  # Prioridade baseada na incidência
            )
            tarefas_criadas.append({
                'id': tarefa.id,
                'assunto': assunto.nome,
                'materia': assunto.materia.nome,
                'data': data_atual.isoformat(),
                'prioridade': tarefa.prioridade
            })
            
            # Avançar data considerando o tempo estimado
            data_atual += timedelta(days=1)
            
            # Se ultrapassar a data da prova, parar
            if data_atual > perfil.data_prova:
                break

        return {
            "sucesso": True,
            "mensagem": f"Cronograma gerado com sucesso! {len(tarefas_criadas)} tarefas criadas.",
            "cronograma": {
                "tarefas": tarefas_criadas,
                "dias_para_prova": dias_para_prova,
                "total_tarefas": len(tarefas_criadas)
            }
        }

    except Exception as e:
        logger.error(f"Erro ao gerar cronograma para {usuario.username}: {e}")
        return {
            "sucesso": False,
            "mensagem": "Erro interno ao gerar cronograma.",
            "detalhes": {"erro": str(e)}
        }