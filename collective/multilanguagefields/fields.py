from Products.CMFPlone.utils import getToolByName
from collective.multilanguagefields import MessageFactory as _
from z3c.form.converter import DictMultiConverter
from z3c.form.widget import MultiWidget
from zope import schema
from zope.component import adapts

language_choice = schema.Choice(
    title=_(u"Language"),
    vocabulary="plone.app.vocabularies.SupportedContentLanguages",
)


class MultiLanguageTextLine(schema.Dict):

    def __init__(self, key_type=None, value_type=None, **kw):
        super(MultiLanguageTextLine, self).__init__(**kw)
        self.key_type = language_choice
        self.value_type = schema.TextLine(
            title=kw.get('title'),
            required=kw.get('required'),
        )
        self.key_type._init_field = True
        self.default = kw.get('default', {})
        self.key_type._init_field = False


class MultiLanguageText(schema.Dict):

    def __init__(self, key_type=None, value_type=None, **kw):
        super(MultiLanguageText, self).__init__(**kw)
        self.key_type = language_choice
        self.value_type = schema.Text(
            title=kw.get('title'),
            max_length=kw.get('max_length'),
            required=kw.get('required'),
        )


class MultiLanguageTextFieldDataConverter(DictMultiConverter):
    """A data converter that fills the dictionary with a key for each language
    """
    adapts(schema.interfaces.IDict, MultiWidget)

    def __init__(self, field, widget):
        super(MultiLanguageTextFieldDataConverter, self).__init__(
            field, widget)

    def toWidgetValue(self, value):
        """Include items for each language in the site.
        """
        if value is self.field.missing_value:
            return {}
        converter = self._getConverter(self.field.value_type)
        key_converter = self._getConverter(self.field.key_type)

        # update values to include languages hat aren't set
        ltool = getToolByName(self.widget.context, 'portal_languages')
        for language in ltool.supported_langs:
            if language not in value:
                value[language] = ''

        # we always return a list of values for the widget
        values = [(key_converter.toWidgetValue(k), converter.toWidgetValue(v))
                  for k, v in value.items()]
        return values
