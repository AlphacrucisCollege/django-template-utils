from django.contrib.auth.models import User
from django.template import Template, Context
from django.test import TestCase
from django.conf import settings
from django.core.serializers import deserialize

from template_utils import functions

def render(src, ctx=None):
    return Template(src).render(Context(ctx))

class SimpleTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username='tester',email='test')
    
    def test_load(self):
        render("{% load func_tools comparison %}")
        
    def test_set_tag(self):
        t = "{% load func_tools %}{% set src='import this' %}{{ src }}"
        self.assertEquals(render(t), u'import this')
        
    def test_del_tag(self):
        t = "{% load func_tools %}{% del 'test' %}{{ test }}"
        self.assertEquals(render(t,{'test': 'yup'}), u'')

    def test_serialize(self):
        t = "{% load func_tools %}{% serialize json users %}"
        json = render(t, {'users':User.objects.all()})
        self.assertEquals(deserialize('json', json).next().object.username, 'tester')
        
    def test_matches(self):
        t = "{% load comparison %}{% if_matches 'hiya' '.{4}' %}yup{% endif_matches %}"
        self.assertEquals(render(t), u'yup')

    def test_contains(self):
        t = "{% load comparison %}{% if_contains 'team' 'i' %}yup{% endif_contains %}"
        self.assertEquals(render(t), u'')
        
    def test_divisible_by(self):
        t = "{% load comparison %}{% if_divisible_by 150 5 %}buzz{% endif_divisible_by %}"
        self.assertEquals(render(t), u'buzz')

    def test_startswith(self):
        t = "{% load comparison %}{% if_startswith 'python' 'p' %}yup{% endif_startswith %}"
        self.assertEquals(render(t), u'yup')

    def test_subset(self):
        t = "{% load comparison %}{% if_subset l1 l2 %}yup{% endif_subset %}"
        self.assertEquals(render(t, {'l1':[2,3], 'l2':range(5)}), u'yup')
    
    def test_defaults(self):
        if hasattr(settings, 'DEFAULT_BUILTIN_TAGS'):
            t = "{{ src|markdown }}"
            self.assertEquals(render(t, {'src':'`i`'}), u'<p><code>i</code></p>')
        else:
            print 'You really should set DEFAULT_BUILTIN_TAGS to test this properly'
 
    def test_negate(self):
        t = "{% load comparison %}{% if_startswith 'python' 'p' negate %}yup{% endif_startswith %}"
        self.assertEquals(render(t), u'')
        
    def test_negate_else(self):
        t = "{% load comparison %}{% if_startswith 'python' 'p' negate %}yup{% else %}nope{% endif_startswith %}"
        self.assertEquals(render(t), u'nope')

    def test_ctx_varname(self):
        t = "{% load func_tools %}{% serialize json users as jsoncontent %}{{ jsoncontent|safe }}"
        json = render(t, {'users':User.objects.all()})
        self.assertEquals(deserialize('json', json).next().object.username, 'tester')