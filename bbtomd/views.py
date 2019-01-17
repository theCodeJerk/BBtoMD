from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import sqlite3
import string
import random
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render
from django import forms
from . import models
import bbcode
import html2text


class ConverterForm(forms.ModelForm):
    class Meta:
        model = models.ConversionModel
        fields = '__all__'


class ConverterView(TemplateView):
    form_class = ConverterForm
    initial = {'key': 'value'}
    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'converter_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            mybbcodes = request.POST['bbcodes']
            html = bbcode.render_html(mybbcodes)
            h = html2text.HTML2Text()
            h.body_width = 0
            mymdcodes = h.handle(html)

        return render(request, self.template_name, {'converter_form': form, 'mdcodestring': mymdcodes })

