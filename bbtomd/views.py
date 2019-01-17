from django.shortcuts import render
import jiphy
import execjs
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django import forms
import sqlite3
import string
import random
from . import models

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
            jsfile = open("static/js/bbtomd.js").read()
            ctx = execjs.compile(jsfile)
            mybbcodes = request.POST['bbcodes']
            mymdcodes = ctx.call("convert", mybbcodes)

        return render(request, self.template_name, {'converter_form': form, 'mdcodestring': mymdcodes})

