.. notes_schematics

==========
Schematics
==========

I am the original author of `The Schematics Project <https://github.com/schematics/schematics>`_.

The community took over the project many years ago and I spent more time with
languages that weren't Python. My curiosity made me wonder what Schematics
would look like if I built it from scratch today...

In particular, it felt important to me to put all of the type validation and
conversion functions somewhere separate from where all the data is kept. This
could be seen as a thorny opinion with a preference for functional programming
models, which is basically right... But there's more to it, too.

The Schematics project also showed me that programming models can *feel* heavy
from the cognitive load of a namespace that contains everything necessary for
managing a metaprogramming framework & complex data together. I wanted
something that would feel more focused, and thus more straight forward and
simple.

I got started.

Types & Data
============

By the time I had built a rough draft, I started to believe I had found a new
way of thinking about data that deserved to be articulated as code.

TypeRighter would put all of the logic for validating and converting data into
a simple structure, a ``Type``, and types would only *operate* on data, *never*
storing it.

The namespace of a type is concerned just with configuring a type's behavior.

Records took this pretty far. They actually ignore attempts to set attributes
if the name is already associated with a typerighter ``Type``.

Mutability as Views
===================

Schematics structured itself such that it behaved a lot like a typical Python
class. You could store data on the model and then call methods which would
operate on that data.

TypeRighter's approach is to consider any kind of mutable object a ``View``.
It is a way of working with data that will look familiar to both Schematics
users and Python users.

In using different terminology, a *view*, for a familiar concept, a mutable
class instance, we make it clear the structure is just one way of looking at
the data, and this structure can be configured for unique behaviors that other
views of the same data do not have, etc.

Please Try It
=============

If you are here from the Schematics community, please try this library!

I believe it is a significantly better design and I would love to share the
work with anyone interested enough to contribute.
