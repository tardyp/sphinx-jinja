.. image:: https://img.shields.io/travis/tardyp/sphinx-jinja.svg?maxAge=2592000
    :target: https://travis-ci.org/tardyp/sphinx-jinja

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

.. code:: python

    extensions = ['sphinxcontrib.jinja']

    jinja_contexts = {
        'first_ctx': {'topics': {'a': 'b', 'c': 'd'}}
    }

You can also customize the jinja ``Environment`` by passing custom kwargs, adding filters, tests, and globals, and setting policies:

.. code:: python

    jinja_env_kwargs = {
        'lstrip_blocks': True,
    }

    jinja_filters = {
        'bold': lambda value: f'**{value}**',
    }

    jinja_tests = {
        'instanceof': lambda value, type: isinstance(value, type),
    }

    jinja_globals = {
        'list': list,
    }

    jinja_policies = {
        'compiler.ascii_str': False,
    }

Which can then be used in the templates:

.. code:: rst

    Lists
    -----

    {% for o in objects -%}
        {%- if o is instanceof list -%}
            {%- for x in o -%}
                - {{ x|bold }}
            {% endfor -%}
        {%- endif -%}
    {%- endfor %}


Available options
=================

- ``file``: allow to specify a path to Jinja instead of writing it into the content of the
  directive. Path is relative to the current directory of sphinx-build tool, typically the directory
  where the ``conf.py`` file is located.

- ``header_char``: character to use for the the headers. You can use it in your template to set your
  own title character:

  For example:

  .. code:: rst

      Title
      {{ options.header_char * 5 }}

- ``debug``: print debugging information during sphinx-build. This allows you to see the generated
  rst before sphinx builds it into another format.

Example of declaration in your RST file:

.. code:: rst

      .. jinja:: approval_checks_api
         :file: relative/path/to/template.jinja
         :header_char: -

Each element of the ``jinja_contexts`` dictionary is a context dict for use in your jinja templates.


Running tests
=============

* pip install tox
* tox
