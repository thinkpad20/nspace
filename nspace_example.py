from nspace import *

package("foo.bar.baz")
include("boz", "buzz")
include_from("blooz", "bizzle",
                      alias("foozle", "goozle"),
                      alias("herp", "derp"))
include_all("blargh")

@export
def super_cool_func(floop):
    if boz.func(goozle(floop)) > derp(buzz.YOYO):
        return bizzle.glap(fap)
    else:
        return 5

@export("something")
def foo(glop):
    return [not_exported(x) for x in buzz.dorp(glop)]

def not_exported(glibber):
    return glibber.shiver_me_timbers()
