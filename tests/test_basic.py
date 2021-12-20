# -*- coding: utf-8 -*-

import os
import sys
from pkgutil import walk_packages
from sphinx.testing.fixtures import make_app, test_params
from sphinx.testing.util import path as Path

if sys.version_info[:2] > (3, 8):
    import collections
    import collections.abc
    collections.Mapping = collections.abc.Mapping
    collections.MutableMapping = collections.abc.MutableMapping

SRCDIR = Path(__file__).parent / "docs/basic"

def test_build_html(make_app):
    app = make_app(buildername='html', srcdir=SRCDIR)
    app.builder.build_all()


def test_build_singlehtml(make_app):
    app = make_app(buildername='singlehtml', srcdir=SRCDIR)
    app.builder.build_all()
    html = (app.outdir / 'index.html').read_text()
    assert ('<p>A sphinx extension to include jinja based templates based '
            'documentation into a sphinx doc</p>') in html
    assert '<p>b</p>' in html
    assert '<p>second:a = b</p>' in html


def test_build_latex(make_app):
    app = make_app(buildername='latex', srcdir=SRCDIR)
    app.builder.build_all()


def test_build_epub(make_app):
    app = make_app(buildername='epub', srcdir=SRCDIR)
    app.builder.build_all()


def test_build_json(make_app):
    app = make_app(buildername='json', srcdir=SRCDIR)
    app.builder.build_all()


def test_customize_env(make_app):
    app = make_app(buildername='singlehtml', srcdir=SRCDIR)
    app.builder.build_all()
    html = (app.outdir / 'index.html').read_text()
    assert '<h2>Lists' in html
    assert 'skipped_string' not in html
    for x in [1, 2, 3, 'a', 'b']:
        # I have no idea why the <p> tags are missing on 2.7...
        if sys.version_info[:2] < (3, 0):
            assert '<li><strong>{}</strong></li>'.format(x) in html
        else:
            assert '<li><p><strong>{}</strong></p></li>'.format(x) in html
