from collective.multilanguagefields import MessageFactory as _
from z3c.form.datamanager import AttributeField
from zope import schema
from zope.component import adapts
from zope.interface import Interface


class MultiLanguageTextLine(schema.Dict):

    def __init__(self, key_type=None, value_type=None, **kw):
        super(MultiLanguageTextLine, self).__init__(**kw)
        self.key_type = schema.Choice(
            title=_(u"Language"),
            vocabulary="plone.app.vocabularies.SupportedContentLanguages",
        )
        self.value_type = schema.TextLine(
            title=kw.get('title'),
        )


class MultiLanguageDataManager(AttributeField):

    """Custom DataManager to store field value in dictionary with prefix
    """

    adapts(Interface, MultiLanguageTextLine)

    def __init__(self, context, field):
        """Set attribute name.
        """
        super(MultiLanguageDataManager, self).__init__(context, field)
        ML_PREFIX = '_ml_'  # prefix for attribute to store dictionary in
        self.attribute_name = "%s%s" % (ML_PREFIX, self.field.__name__)

    def get(self):
        value = ''
        values = getattr(self.adapted_context, self.attribute_name, '')
        if values:
            default_language = self.ltool.getDefaultLanguage()
            # use request language or site default language
            language = self.context.REQUEST.get('LANGUAGE',
                                                default_language)
            value = values.get(language, '')
            if not value:
                # return site default language
                value = values.get(default_language)
                if not value:
                    # return random language
                    value = values.values()[0]
        return value

    def set(self, value):
        setattr(self.adapted_context, self.attribute_name, value)
