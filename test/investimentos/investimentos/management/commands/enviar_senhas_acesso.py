from django.core.management import BaseCommand
from ...models import Gestor
from uuid import uuid1
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


MENSAGEM = '''

<b>Senhor(a) gestor(a)</b>,

<p>Seguem as informações de acesso ao <b>Sistema de Coleta de Demandas da Rede Federal de Educação Profissional, Científica e Tecnológica</b>.</p>

<p>
<i>URL</i>: https://coletasetec.ifrn.edu.br/ <br>
<i>Login</i>: {email} <br>
<i>Senha</i>: {senha} <br>
</p>

<p>Por questões de segurança, orienta-se que no primeiro acesso seja feita a alteração da senha. Para isso, no canto superior direito do sistema, clique no e-mail da instituição e selecione a opção “Alterar Senha”.</p>

<p>Para acessar o tutorial do sistema em PDF, acesse https://coletasetec.ifrn.edu.br/tutorial/tutoria.pdf.<br>
Caso prefira o tutorial no formato de vídeo, acesse https://coletasetec.ifrn.edu.br/videos/.</p>

<p>
<b>Diretoria de Desenvolvimento da Rede Federal<br>
Secretaria de Educação Profissional e Tecnológica</b>
</p>
'''


class Command(BaseCommand):
    def handle(self, *args, **options):
        qs = Gestor.objects.filter(user__last_login__isnull=True)
        print(qs.count())
        for gestor in qs:
            senha = uuid1().hex[0:3]
            gestor.user.set_password(senha)
            gestor.user.save()
            subject = '[SETEC] Credenciais de Acesso – Sistema de Coleta de Demandas'
            html_content = MENSAGEM.format(email=gestor.email, senha=senha)
            text_content = strip_tags(html_content)
            from_email = None
            to = [gestor.email]
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
                print(gestor.email)
            except BaseException:
                print('ERROR: ', gestor.email)
