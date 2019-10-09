.. developing_testing

=======
Testing
=======

Typerighter uses `pytest`.

::

  $ pytest tests
  =============================== test session starts ================================
  platform darwin -- Python 3.7.4, pytest-5.2.1, py-1.8.0, pluggy-0.13.0
  rootdir: ...
  plugins: cov-2.8.1
  collected 69 items                                                                 

  tests/test_booleantypes.py ....                                              [  5%]
  tests/test_cache.py .                                                        [  7%]
  tests/test_datetimetypes.py ..                                               [ 10%]
  tests/test_emailtype.py ..                                                   [ 13%]
  tests/test_ipaddresstypes.py ....                                            [ 18%]
  tests/test_listtypes.py ......                                               [ 27%]
  tests/test_macaddresses.py ..                                                [ 30%]
  tests/test_primitives.py .........                                           [ 43%]
  tests/test_records.py ............                                           [ 60%]
  tests/test_schematics.py .                                                   [ 62%]
  tests/test_stringtypes.py .......                                            [ 72%]
  tests/test_sumtypes.py ....                                                  [ 78%]
  tests/test_types.py ..........                                               [ 92%]
  tests/test_urltypes.py ..                                                    [ 95%]
  tests/test_views.py ...                                                      [100%]

  ================================ 69 passed in 0.16s ================================

Nice.
