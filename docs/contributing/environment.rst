.. contributing_environment

===========
Environment
===========

I like to use simple setups, so I use a virtualenv and install a development
copy of TypeRighter into that, along with the tools I use for dev and building
the docs.

Get Repo
========

Get the source. ::

  $ cd ~/Code
  $ git clone https://github.com/jmsdnns/typerighter
  $ cd typerighter

Virtual Env
-----------

If you dont have an environment setup already, create one in the project
directory. ::

  $ python3 -m venv venv
  $ source venv/bin/activate

Install w/ Extras
=================

Install typerighter into the virtualenv as a pointer to this working
directory. ::

  $ git clone https://github.com/jmsdnns/typerighter
  $ cd typerighter
  $ pip install -e .[dev,docs]

