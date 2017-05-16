import codecs
import os
import sys
import urllib

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from jinja2 import FileSystemLoader, Environment


class JinjaDirective(Directive):
    has_content = True
    required_arguments = 1
    option_spec = {
        "file": directives.path,
        "header_char": directives.unchanged,
        "debug": directives.unchanged,
    }
    app = None

    def run(self):
        node = nodes.Element()
        node.document = self.state.document
        jinja_context_name = self.arguments[0]
        env = self.state.document.settings.env
        docname = env.docname
        template_filename = self.options.get("file")
        debug_template = self.options.get("debug")
        cxt = self.app.config.jinja_contexts[jinja_context_name]
        cxt["options"] = {
            "header_char": self.options.get("header_char")
        }
        if template_filename:
            if debug_template is not None:
                print('')
                print('********** Begin Jinja Debug Output: Template Before Processing **********')
                print('********** From {} **********'.format(docname))
                reference_uri = directives.uri(os.path.join('source', template_filename))
                template_path = urllib.url2pathname(reference_uri)
                encoded_path = template_path.encode(sys.getfilesystemencoding())
                imagerealpath = os.path.abspath(encoded_path)
                with codecs.open(imagerealpath, encoding='utf-8') as f:
                    print(f.read())
                print('********** End Jinja Debug Output: Template Before Processing **********')
                print('')
            tpl = Environment(
                          loader=FileSystemLoader(
                              self.app.config.jinja_base, followlinks=True)
                      ).get_template(template_filename)
        else:
            if debug_template is not None:
                print('')
                print('********** Begin Jinja Debug Output: Template Before Processing **********')
                print('********** From {} **********'.format(docname))
                print('\n'.join(self.content))
                print('********** End Jinja Debug Output: Template Before Processing **********')
                print('')
            tpl = Environment(
                      loader=FileSystemLoader(
                          self.app.config.jinja_base, followlinks=True)
                  ).from_string('\n'.join(self.content))
        new_content = tpl.render(**cxt)
        if debug_template is not None:
            print('')
            print('********** Begin Jinja Debug Output: Template After Processing **********')
            print(new_content)
            print('********** End Jinja Debug Output: Template After Processing **********')
            print('')
        new_content = StringList(new_content.splitlines())
        self.state.nested_parse(new_content, self.content_offset,
                                node, match_titles=1)
        return node.children


def setup(app):
    JinjaDirective.app = app
    app.add_directive('jinja', JinjaDirective)
    app.add_config_value('jinja_contexts', {}, 'env')
    app.add_config_value('jinja_base', os.path.abspath('.'), 'env')
