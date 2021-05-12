XMLX - a simple and compact XML parser.

XMLX = XML eXtras

To initialize an element object from a string:

``>>> xmlx.Element('<html>hello!</html>')``

``<html>..</html at 0x...>``

If you prefer dictionaries, simply use ``xmlx.elemdict(text)``:

``>>> xmlx.elemdict('<html>hello!</html>')``

``{'?':{},'@':'hello!','*':'<html>hello!</html>'}``

``?`` is the element's attributes, ``@`` is its content (JS innerHTML), and ``*`` is its text (JS outerHTML).

See help(xmlx) for further documentation.


