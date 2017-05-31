from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'


class CoursePageView(TemplateView):
    template_name = 'course-page.html'
    