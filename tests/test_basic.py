# -*- coding: utf-8 -*-

import os
import sys
from pkgutil import walk_packages

from sphinx_testing import with_app

if sys.version_info[:2] > (3, 0):
    # Make sure that the other sphinxcontrib packages can be loaded
    import sphinxcontrib.jinja
    if 'site-packages' not in sphinxcontrib.__path__:
        sys.path.remove(os.path.dirname(sphinxcontrib.__path__[0]))
        del sys.modules['sphinxcontrib']
        for path in filter(lambda p: 'site-packages' in p, sys.path):
            contrib = os.path.join(path, 'sphinxcontrib')
            for minfo in walk_packages([contrib], prefix='sphinxcontrib.'):
                spec = minfo.module_finder.find_spec(minfo.name)
                spec.loader.load_module(minfo.name)


@with_app(buildername='html', srcdir='tests/docs/basic/')
def test_build_html(app, status, warning):
    app.builder.build_all()


@with_app(buildername='singlehtml', srcdir='tests/docs/basic/')
def test_build_singlehtml(app, status, warning):
    app.builder.build_all()
    html = (app.outdir / 'index.html').read_text()
    assert ('<p>A sphinx extension to include jinja based templates based '
            'documentation into a sphinx doc</p>') in html
    assert '<p>b</p>' in html
    assert '<p>second:a = b</p>' in html


@with_app(buildername='latex', srcdir='tests/docs/basic/')
def test_build_latex(app, status, warning):
    app.builder.build_all()


@with_app(buildername='epub', srcdir='tests/docs/basic/')
def test_build_epub(app, status, warning):
    app.builder.build_all()


@with_app(buildername='json', srcdir='tests/docs/basic/')
def test_build_json(app, status, warning):
    app.builder.build_all()
