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

js = r"""

function convert(bbcodes) {

  //preprocessing for tf2toolbox BBCode
  if(bbcodes.search(/TF2Toolbox/gmi) != -1) {
    bbcodes = bbcodes
    .replace(/(\(List generated at .+?\[\/URL\]\))((?:.|\n)+)/gmi, '$2\n\n\n$1') //Move TF2Toolbox link to bottom
    .replace('(List generated at', '(List generated from')
    .replace(/[^\S\n]+\(List/gmi,'(List')
    .replace(/\[b\]\[u\](.+?)\[\/u\]\[\/b\]/gmi,'[b]$1[/b]\n') //Fix double emphasized titles
    .replace(/(\n)\[\*\]\[b\](.+?)\[\/b\]/gmi, '$1\[\*\] $2');
  }

  //general BBcode conversion
  bbcodes = bbcodes
    .replace(/\[b\]((?:.|\n)+?)\[\/b\]/gmi, '**$1**') //bold; replace [b] $1 [/b] with ** $1 **
    .replace(/\[\i\]((?:.|\n)+?)\[\/\i\]/gmi, '*$1*')  //italics; replace [i] $1 [/u] with * $1 *
    .replace(/\[\u\]((?:.|\n)+?)\[\/\u\]/gmi, '$1')  //remove underline;
    .replace(/\[s\]((?:.|\n)+?)\[\/s\]/gmi, '~~ $1~~') //strikethrough; replace [s] $1 [/s] with ~~ $1 ~~
    .replace(/\[center\]((?:.|\n)+?)\[\/center\]/gmi, '$1') //remove center;
    .replace(/\[quote\=.+?\]((?:.|\n)+?)\[\/quote\]/gmi, '$1') //remove [quote=] tags
    .replace(/\[size\=.+?\]((?:.|\n)+?)\[\/size\]/gmi, '## $1') //Size [size=] tags
    .replace(/\[color\=.+?\]((?:.|\n)+?)\[\/color\]/gmi, '$1') //remove [color] tags
    .replace(/\[list\=1\]((?:.|\n)+?)\[\/list\]/gmi, function (match, p1, offset, string) {return p1.replace(/\[\*\]/gmi, '1. ');})
    .replace(/(\n)\[\*\]/gmi, '$1* ') //lists; replcae lists with + unordered lists.
    .replace(/\[\/*list\]/gmi, '')
    .replace(/\[img\]((?:.|\n)+?)\[\/img\]/gmi,'![$1]($1)')
    .replace(/\[url=(.+?)\]((?:.|\n)+?)\[\/url\]/gmi,'[$2]($1)')
    .replace(/\[code\](.*?)\[\/code\]/gmi, '`$1`')
    .replace(/\[code\]((?:.|\n)+?)\[\/code\]/gmi, function (match, p1, offset, string) {return p1.replace(/^/gmi, '    ');})
    .replace(/\[php\](.*?)\[\/php\]/gmi, '`$1`')
    .replace(/\[php\]((?:.|\n)+?)\[\/php\]/gmi, function (match, p1, offset, string) {return p1.replace(/^/gmi, '    ');})
    .replace(/\[pawn\](.*?)\[\/pawn\]/gmi, '`$1`')
    .replace(/\[pawn\]((?:.|\n)+?)\[\/pawn\]/gmi, function (match, p1, offset, string) {return p1.replace(/^/gmi, '    ');});

  //post processing for tf2toolbox BBCode
  if(bbcodes.search(/TF2Toolbox/gmi) != -1) {
    bbcodes = bbcodes
    .replace('/bbcode_lookup.php))', '/bbcode_lookup.php) and converted to /r/tf2trade ready Markdown by Dum\'s [converter](http://jondum.github.com/BBCode-To-Markdown-Converter/)).') //add a linkback
    .replace(/\*\*.+?\*\*[\s]+?None[\s]{2}/gmi, ''); //remove empty sections

  }

  return bbcodes;

}
"""


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
            ctx = execjs.compile(js)
            mybbcodes = request.POST['bbcodes']
            mymdcodes = ctx.call("convert", mybbcodes)

        return render(request, self.template_name, {'converter_form': form, 'mdcodestring': mymdcodes})


# Create your views here.
def index(request):
    return render(request, 'index.html')