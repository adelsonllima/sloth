import inspect

from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from sloth.app.templatetags.tags import mobile
from sloth.db import models
from sloth.exceptions import ReadyResponseException
from sloth.utils import pretty


DASHBOARDS = []


class DashboardType(type):

    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)
        DASHBOARDS.append(cls)
        return cls


class Dashboard(metaclass=DashboardType):

    def __init__(self, request):
        self.request = request
        self.data = dict(
            info=[], warning=[], search=[], menu=[], links=[], shortcuts=[], cards=[],
            floating=[], navigation=[], settings=[], center=[], right=[], actions=[], grids=[]
        )
        self.defined_apps = {}
        self.enabled_apps = set()
        if self.request.user.is_authenticated:
            self.load(request)

    def to_item(self, model, count=True):
        return

    def _load(self, key, models, app=None):
        allways = 'floating', 'navigation', 'settings', 'actions', 'menu', 'links'
        for model in models:
            if model().has_list_permission(self.request.user) or model().has_permission(self.request.user):
                if key in allways or self.request.path == '/app/':
                    url = model.get_list_url('/app')
                    add_item = True
                    if app:
                        self.enabled_apps.add(app)
                        add_item = self.request.session.get('app_name') == app
                    for item in self.data[key]:
                        add_item = add_item and not item['url'] == url
                    if add_item:
                        self.data[key].append(
                            dict(
                                url=url,
                                label=model.metaclass().verbose_name_plural,
                                count=model.objects.all().apply_role_lookups(self.request.user).count(),
                                icon=getattr(model.metaclass(), 'icon', None),
                                app=app
                            )
                        )

    def _item(self, key, url, label, icon, count=None, app=None):
        self.data[key].append(
            dict(url=url, label=label, count=count, icon=icon, app=app)
        )

    def info(self, *models, app=None):
        self._load('info', models, app=app)

    def warning(self, *models, app=None):
        self._load('warning', models, app=app)

    def search(self, *models, app=None):
        self._load('search', models, app=app)

    def menu(self, *models, app=None):
        if mobile(self.request):
            self._load('search', models, app=app)
        else:
            self._load('menu', models, app=app)

    def links(self, *models, app=None):
        self._load('links', models, app=app)

    def add_link(self, url, label, app=None):
        self._item(self, 'links', url, label, app=app)

    def shortcuts(self, *models, app=None):
        self._load('shortcuts', models, app=app)

    def add_shortcut(self, url, label, icon, app=None):
        self._item(self, 'shortcut', url, label, icon, app=app)

    def actions(self, *models, app=None):
        if mobile(self.request):
            self._load('search', models, app=app)
        else:
            self._load('actions', models, app=app)

    def add_action(self, url, label, icon, app=None):
        if mobile(self.request):
            self._item(self, 'search', url, label, icon, app=app)
        else:
            self._item(self, 'actions', url, label, icon, app=app)

    def add_app(self, label, icon, hide=False):
        url = '/app/?activate-application={}'.format(label)
        self.defined_apps[label] = dict(label=label, icon=icon, hide=hide, url=url, enabled=False)

    def grids(self, *grids):
        for grid in grids:
            self.add_grid(grid)

    def add_grid(self, grid, template=None, size=1):
        key = 'grids'
        if isinstance(grid, (list, tuple)):
            html = mark_safe(render_to_string(grid[1], grid[0], request=self.request))
            self.data[key].append(
                dict(
                    html=html,
                    size=size,
                )
            )
        elif isinstance(grid, dict):
            html = mark_safe(render_to_string(template, grid, request=self.request))
            self.data[key].append(
                dict(
                    html=html,
                    size=size,
                )
            )
        elif inspect.isclass(grid) and issubclass(grid, models.Model):
            model = grid
            if model().has_list_permission(self.request.user) or model().has_permission(self.request.user):
                if self.request.path == '/app/':
                    url = model.get_list_url('/app')
                    add_item = True
                    # for item in self.data[key]:
                    #     add_item = add_item and not item.get('url') == url
                    if add_item:
                        self.data[key].append(
                            dict(
                                url=url,
                                label=model.metaclass().verbose_name_plural,
                                count=model.objects.all().apply_role_lookups(self.request.user).count(),
                                icon=getattr(model.metaclass(), 'icon', None),
                                size=size,
                            )
                        )
        elif isinstance(grid, models.QuerySet):
            if self.request.path == '/app/':
                self.data[key].append(
                    dict(
                        html=str(grid.contextualize(self.request)),
                        size=size,
                    )
                )

    def cards(self, *models, app=None):
        self._load('cards', models, app=app)

    def floating(self, *models, app=None):
        self._load('floating', models, app=app)

    def navigation(self, *models, app=None):
        if mobile(self.request):
            self._load('floating', models, app=app)
        else:
            self._load('navigation', models, app=app)

    def add_navigation(self, url, label, icon, app=None):
        if mobile(self.request):
            self._item('floating', url, label, icon, app=app)
        else:
            self._item('navigation', url, label, icon, app=app)

    def settings(self, *models, app=None):
        self._load('settings', models, app=app)

    def append(self, data, aside=False, top=False):
        if aside and hasattr(data, 'compact'):
            data.compact()
        if self.request.path == '/app/':
            html = str(data.contextualize(self.request))
            if aside:
                self.data['right'].append(html)
            elif top:
                self.data['top'].append(html)
            else:
                self.data['center'].append(html)

    def extend(self, data, template, aside=False, top=False):
        if self.request.path == '/app/':
            html = mark_safe(render_to_string(template, data, request=self.request))
            if aside:
                self.data['right'].append(html)
            elif top:
                self.data['top'].append(html)
            else:
                self.data['center'].append(html)

    def load(self, request):
        pass

    def get_qtd_grid(self):
        return 3

    def get_grid_size(self):
        qtd_grid = self.get_qtd_grid()
        return 12//qtd_grid


class Dashboards:

    def __init__(self, request):

        self.request = request
        self.data = dict(
            info=[], warning=[], search=[], menu=[], links=[], shortcuts=[], cards=[],
            floating=[], navigation=[], settings=[], center=[], right=[], actions=[], grids=[]
        )
        self.apps = {}
        self.data['navigation'].append(
            dict(url='/app/', label='Principal', icon='house', app=None)
        )
        for cls in DASHBOARDS:
            dashboard = cls(request)
            self.grid_size = dashboard.get_grid_size()
            for key in dashboard.data:
                self.data[key].extend(dashboard.data[key])
            self.apps.update(dashboard.defined_apps)

        if self.request.user.is_superuser:
            self.superuser_search(self.data['search'])

        for name in dashboard.enabled_apps:
            self.apps[name]['enabled'] = True
        if 'activate-application' in request.GET:
            for name in self.apps:
                if name == request.GET['activate-application']:
                    request.session['app_name'] = name
                    request.session['app_icon'] = self.apps[name]['icon']
                    request.session.save()
            raise ReadyResponseException(HttpResponseRedirect('/app/'))

    def superuser_search(self, items):
        from django.apps import apps
        from .. import PROXIED_MODELS
        for model in apps.get_models():
            if model not in PROXIED_MODELS:
                app_label = model.metaclass().app_label
                model_name = model.metaclass().model_name
                model_verbose_name_plural = model.metaclass().verbose_name_plural
                icon = getattr(model.metaclass(), 'icon', None)
                url = '/app/{}/{}/'.format(app_label, model_name)
                add_item = True
                for item in items:
                    add_item = add_item and not item['url'] == url
                if add_item:
                    item = dict(label=pretty(str(model_verbose_name_plural)), description=None, url=url, icon=icon, subitems=[], app=None)
                    items.append(item)
        return items

    def __str__(self):
        return mark_safe(render_to_string('app/dashboard/dashboards.html', dict(data=self.data, grid_size=self.grid_size), request=self.request))
