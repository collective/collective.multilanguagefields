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
        values = getattr(self.adapted_context, self.attribute_name)
        return_value = ''
        # if we are rendering the widget, we should return the whole dictionary
        edit_mode = self.context.REQUEST.getURL().endswith('@@edit')
        if edit_mode:
            return_value = values
        else:
            if values:
                default_language = self.ltool.getDefaultLanguage()
                # use request language or site default language
                language = self.context.REQUEST.get('LANGUAGE',
                                                    default_language)
                return_value = values.get(language, '')
                if not return_value:
                    # return site default language
                    return_value = values.get(default_language)
                    if not return_value:
                        # return random language
                        return_value = values.values()[0]
        return return_value

    def set(self, value):
        setattr(self.adapted_context, self.attribute_name, value)
