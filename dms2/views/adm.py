# -*- coding: utf-8 -*-
import time

from django.apps import apps
from django.contrib import auth
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from .. import views
from ..forms import FormMixin
from ..utils.icons import bootstrap
from ..exceptions import ReadyResponseException, HtmlReadyResponseException


def view(func):
    def decorate(request, *args, **kwargs):
        try:
            time.sleep(0.5)
            if views.is_authenticated(request):
                response = func(request, *args, **kwargs)
                response["X-Frame-Options"] = "SAMEORIGIN"
                return response
            else:
                return HttpResponseForbidden()
        except ReadyResponseException as e:
            return JsonResponse(e.data)
        except HtmlReadyResponseException as e:
            return HttpResponse(e.html)
        except PermissionDenied:
            return HttpResponseForbidden()
        except BaseException as e:
            raise e

    return decorate


@view
def icons(request):
    return render(request, ['adm/icons.html'], dict(bootstrap=bootstrap.ICONS))


def login(request, username):
    if settings.DEBUG and request.get_host() == 'localhost:8000':
        user = apps.get_model(
            settings.AUTH_USER_MODEL
        ).objects.get(username=username)
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return index(request)


def index(request):
    return render(request, ['adm/index.html'], dict())


@view
def add_view(request, app_label, model_name):
    form = views.add_view(request, app_label, model_name)
    return render(request, ['adm/add.html'], dict(form=form))


@view
def edit_view(request, app_label, model_name, pk):
    form = views.edit_view(request, app_label, model_name, pk)
    print(form.serialize())
    if form.message:
        pass
    return render(request, ['adm/add.html'], dict(form=form))


@view
def delete_view(request, app_label, model_name, pk):
    data = views.delete_view(request, app_label, model_name, pk)
    return render(request, ['adm/delete.html'], dict(data=data))


@view
def list_view(request, app_label, model_name, method=None, pks=None, action=None):
    context = {}
    data = views.list_view(request, app_label, model_name, method=method, pks=pks, action=action)
    if isinstance(data, FormMixin):
        context.update(form=data)
    else:
        context.update(data=data)
    return render(request, ['adm/list.html'], context)


@view
def obj_view(request, app_label, model_name, pk, method=None, pks=None, action=None):
    context = {}
    data = views.obj_view(request, app_label, model_name, pk, method=method, pks=pks, action=action)
    if isinstance(data, FormMixin):
        context.update(form=data)
        if data.message:
            return HttpResponse('<script>window.parent.close_fancybox();</script>')
    else:
        context.update(data=data)
    return render(request, ['adm/view.html'], context)
