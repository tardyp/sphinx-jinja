.. image:: https://github.com/tardyp/sphinx-jinja/actions/workflows/ci.yml/badge.svg

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

Alternatively, you can use the `inline-ctx` option to define the context directly within the RST file:

.. code:: rst

    .. jinja::
       :inline-ctx: { "topics": { "foo": "bar", "baz": "qux" } }

        {% for k, v in topics.items() %}

        {{k}}
        ~~~~~
        {{v}}
        {% endfor %}

In your sphinx ``conf.py`` file, you can create or load the contexts needed for your jinja templates

.. code:: python

    extensions = ['sphinx_jinja']

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

- ``header_char``: character to use for the headers. You can use it in your template to set your
  own title character:

  For example:

  .. code:: rst

      Title
      {{ options.header_char * 5 }}

- ``header_update_levels``: If set, a header in the template will appear as the same level as a
  header of the same style in the source document, equivalent to when you use the ``include``
  directive. If not set, headers from the template will be in levels below whatever level is active
  in the source document.

- ``debug``: print debugging information during sphinx-build. This allows you to see the generated
  rst before sphinx builds it into another format.

- ``inline-ctx``: define the context directly within the RST file as a JSON-formatted string. This
  context will be merged with any existing context from the ``jinja_contexts`` dictionary.

Example of declaration in your RST file:

.. code:: rst
    
      .. jinja:: approval_checks_api
         :file: relative/path/to/template.jinja
         :header_char: -
         :inline-ctx: { "additional_key": "additional_value" }

Each element of the ``jinja_contexts`` dictionary is a context dict for use in your jinja templates.

Running tests
=============

* pip install tox
* tox
