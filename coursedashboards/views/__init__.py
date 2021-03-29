# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'index.html'


class CoursePageView(TemplateView):
    template_name = 'course-page.html'
