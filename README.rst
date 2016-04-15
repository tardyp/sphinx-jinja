sphinx-jinja
============

A sphinx extension to include jinja based templates based documentation into a sphinx doc

Usage
=====

In your rst doc, you can use the following snippet to use a jinja template to generate your doc

.. code:: rst

    .. jinja:: first_ctx

        {% for k, v in topics.items() %}

        {{k}}
        ~~~~~
        {{v}}
        {% endfor %}

In your sphinx ``conf.py`` file, you can create or load the contexts needed for your jinja templates

::
    extensions = ['sphinxcontrib.jinja']

    jinja_contexts = {
        'first_ctx': {'topics': {'a': 'b', 'c': 'd'}}
    }


Each element of the `jinja_contexts` dictionary is a context dict for use in your jinja templates

Running tests
=============

* pip install tox
* tox

