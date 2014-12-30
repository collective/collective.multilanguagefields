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

    """Custom DataManager to store field value as dictionary
    """

    adapts(Interface, MultiLanguageTextLine)

    def get(self):
        values = getattr(self.adapted_context, self.field.__name__)
        return_value = ''
        # if we are rendering the widget, we should return the whole dictionary
        url = self.context.REQUEST.getURL()
        edit_mode = url.endswith('/@@edit') or url.endswith('/edit')
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
