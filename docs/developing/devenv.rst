.. developing_devenv

===============
Dev Environment
===============

First, install Typerighter from source and the packages we use for development.

::

  $ git clone https://github.com/jmsdnns/typerighter
  $ cd typerighter
  $ pip install -e .[dev,docs]

Verify all tests are passing

::

  $ pytest tests
  =============================== test session starts ================================
  ...
  ================================ 69 passed in 0.16s ================================

Nice.
