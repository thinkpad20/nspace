# nspace

#### Smart namespacing for python

Note that this is currently vaporware. It's just some ideas, and more to follow. In other words, "nothing to see here, folks"... yet.

### A few features we want to have:

#### Method hiding

Initially only module scope, but eventually in classes too. We want to choose
exactly which methods we will export, and hide the rest. For example:

foo.py:

```python
from nspace import *

def bar(x):
    return x + 1

@export
def baz(y):
    return bar(y) * 3
```

In the interpreter:

```
>>> from nspace import *
>>> include("foo")
>>> foo.baz(3)
12
>>> foo.bar(3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'module' object has no attribute 'bar'
```

We can expand this to allow method hiding for classes.

```python
from nspace import *

@export
class Foo(object):
    @export
    def __init__(self, x):
        self.x = x

    def bar(self, y):
        return self.x + y

    @export
    def baz(self, z):
        return self.bar(z) * self.x
```

Test:

```
>>> from nspace import *
>>> include("foo")
>>> my_foo = foo.Foo(10)
>>> my_foo.baz(11)
210
>>> my_foo.bar(4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Foo' object has no attribute 'bar'
```

#### Coherent namespacing

Only the top-most module is "sealed;" all others can be expanded, using a
java-style package system. Details to come.
