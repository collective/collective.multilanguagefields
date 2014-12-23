Introduction
============

This package aims to provide a simple way to make some fields on a dexterity content type multilingual.
It tries to do what raptus.multilanguagefields does for Archetypes content types.


Usage
-----

Multilingual text line::

    from collective.multilanguagefields.fields import TextLine as MLTextLine
    from plone.supermodel import model

    class IMyType(model.Schema):

        some_text = MLTextLine(
            title=_(u"Fieldname"),
            required=True,
        )


Features
--------


Compatibility
-------------

Plone 4.3 and upwards.


Caveats
-------

You cannot currently make the title field multilingual.
Upon saving, you'll get::

    Module plone.dexterity.utils, line 176, in addContentToContainer
    Module plone.app.content.namechooser, line 46, in chooseName
    TypeError: coercing to Unicode: need string or buffer, dict found

We'll need to register our own INameFromTitle behavior / adapter.
