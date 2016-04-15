import os
import sys
import urllib

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from jinja2 import Template


class JinjaDirective(Directive):

    has_content = True
    required_arguments = 1
    option_spec = {
        "file": directives.path,
        "header_char": directives.unchanged,
    }
    app = None

    def run(self):
        node = nodes.Element()
        node.document = self.state.document
        jinja_context_name = self.arguments[0]
        template_filename = self.options.get("file")
        cxt = self.app.config.jinja_contexts[jinja_context_name]
        cxt["options"] = {
            "header_char": self.options.get("header_char")
        }

        if template_filename:
            reference_uri = directives.uri(template_filename)
            template_path = urllib.url2pathname(reference_uri)
            encoded_path = template_path.encode(sys.getfilesystemencoding())
            imagerealpath = os.path.abspath(encoded_path)
            with open(imagerealpath) as f:
                tpl = Template(f.read())
        else:
            tpl = Template("\n".join(self.content))
        new_content = tpl.render(**cxt)
        # transform the text content into a string_list that the nested_parse
        # can use:
        new_content = StringList(new_content.split("\n"))
        self.state.nested_parse(new_content, self.content_offset,
                                node, match_titles=1)
        return node.children


def setup(app):
    JinjaDirective.app = app
    app.add_directive('jinja', JinjaDirective)
    app.add_config_value('jinja_contexts', {}, 'html')
