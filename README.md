# nspace

#### Smart namespacing for python

Note that this is currently vaporware. It's just some ideas, and more to follow. In other words, "nothing to see here, folks"... yet.

### A few features we want to have:

#### Method hiding

Initially only module scope, but eventually in classes too. We want to choose
exactly which methods we will export, and hide the rest (we can also have the opposite
default, and use a `@hidden` decorator for functions we want to hide). For example:

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

#### More powerful imports

We introduce some alternatives to traditional python `import`: `include`, `include_from` and `include_all`.

This is similar to `import foo`:
```python
foo = include('foo')
```

The following two are both similar to 'from foo import bar'

```python
bar = include('foo.bar')
include_from('foo', 'bar')
```

We can give aliases like with python `as`. The following are equivalent:

```python
cool = include('foo.bar')
include_from('foo', ('bar', 'cool'))
```

We can include multiple things

```python
foo, bar = include('foo', 'bar')
include_from('foo', 'bar', 'baz', ('qux', 'super_cool'))
```

Similar to `from foo import *`

```python
include_all('foo')
```

Sometimes we only need to use something once in a module. We don't need to pollute the namespace just for that. Why not a `with` statement?

```python
# `join` and `up` are only defined inside the with statement
with include_from('os.path', 'join', ('dirname', 'up')):
    filename = join(up(__file__), 'my_file.txt')

def random_name():
    names = ['Tom', 'Dick', 'Harry']
    with include('random.choice') as choice:
         return choice(names)
```

We will also throw an error if attempting to include a hidden method.

#### Package system

nspace expands on the basic python module system, giving it the ability to combine modules into other modules and form Java-style package hierarchies. More on this to come later :-)
