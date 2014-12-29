Introduction
============

This package aims to provide a simple way to make some fields on a dexterity
content type multilingual.
It tries to do what raptus.multilanguagefields does for Archetypes content
types.


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


Making Title field multilingual
-------------------------------

You cant use the default ``plone.app.content.interfaces.INameFromTitle``
behavior.
Instead, use ``collective.multilanguagefields.interfaces.INameFromMultiLanguageTitle``

In addition, your content type needs to implement its own ``Title()`` method
which takes into account that the title attribute conatins a dictionary.
