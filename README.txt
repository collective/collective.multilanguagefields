Introduction
============

.. Caution::

  This package is still in a public experimentation phase.


This package aims to provide a simple way to make some fields on a dexterity
content type available in more than one language ("multilanguage").
It tries to do what raptus.multilanguagefields does for Archetypes content
types.


Assumptions
-----------

* It should be possible for a site to add a new supported language without
  having to migrate content.
  (A modification in the code for your customer-specific package would be ok.)


Usage
-----

Multilanguage text line::

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


Making Title field multilanguage
--------------------------------

You cant use the default ``plone.app.content.interfaces.INameFromTitle``
behavior.
Instead, use ``collective.multilanguagefields.interfaces.INameFromMultiLanguageTitle``

In addition, your content type needs to implement its own ``Title()`` method
which takes into account that the title attribute contains a dictionary.
The ``ml_value`` method from ``utils.py`` might be helpful.


Using multilanguage fields in templates
---------------------------------------

You can do this as follows::

    <span tal:content="context/ml_value/my_field" />

You can also specify a default value::

    <span tal:define="ml_value context/ml_value"
          tal:content="python: ml_value('my_field', 'no translation found')" />
