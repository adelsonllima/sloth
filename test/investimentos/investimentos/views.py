# -*- coding: utf-8 -*-
from decimal import Decimal
from .models import Ciclo, Mensagem
from sloth.admin.gadgets import Cards, Gadget


class Instrucoes(Gadget):

    def __init__(self, request):
        super().__init__(request)
        if request.user.roles.filter(name='Gestor').exists():
            self.mensagem = Mensagem.objects.filter(perfil='Gestor').first()
        else:
            self.mensagem = Mensagem.objects.filter(perfil='Administrador').first()


class Cartoes(Cards):
    pass


class CiclosAbertos(Gadget):
    class Meta:
        can_view = 'Gestor',

    def __init__(self, request):
        super().__init__(request)
        self.ciclos = []
        for ciclo in Ciclo.objects.abertos():
            demandas = ciclo.demanda_set.all().contextualize(request)
            utilizado = Decimal(sum([demanda.valor for demanda in demandas if demanda.valor]))
            self.ciclos.append(
                dict(
                    id=ciclo.id, descricao=ciclo.descricao, maximo=ciclo.teto,
                    utilizado=utilizado, disponivel=ciclo.teto - utilizado,
                    inicio=ciclo.inicio, fim=ciclo.fim, limites=ciclo.limites.all()
                )
            )
