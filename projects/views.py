from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template import loader


class ProjectsIndexView(View):
    def get(self, *args, **kwargs):
        template = loader.get_template('projects_list.html')
        context = {}
        return HttpResponse(
            template.render(context, self.request)
        )


