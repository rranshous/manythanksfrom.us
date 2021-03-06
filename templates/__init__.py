from mako.template import Template
from mako.lookup import TemplateLookup
import helpers as h
import cherrypy
import os
import objects as o

here = os.path.abspath(os.path.dirname(__file__))
lookup = TemplateLookup(directories=[here],format_exceptions=True,
                        output_encoding='utf-8', encoding_errors='replace')

def render(path,**kwargs):
    cherrypy.log('debug','rendering: %s' % path)
    template = lookup.get_template(path)
    kwargs.update({'session':cherrypy.session,
                   'request':cherrypy.request,
                   'o':o,
                   'h':h})
    s = template.render_unicode(**kwargs)
    return s

