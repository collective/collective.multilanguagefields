from Products.CMFPlone.utils import getToolByName
from collective.multilanguagefields import MessageFactory as _
from z3c.form.converter import DictMultiConverter
from z3c.form.widget import MultiWidget
from zope import schema
from zope.component import adapts
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.interface import provider
from ordereddict import OrderedDict
from zope.schema._bootstrapinterfaces import RequiredMissing
from zope.schema.interfaces import ValidationError


class DefaultLanguageMissing(RequiredMissing):
    __doc__ = _("""Default site entry language missing (first item)""")


@provider(IContextAwareDefaultFactory)
def languageDefaultFactory(context):
    values = {}
    ltool = getToolByName(context, 'portal_languages')
    values = dict.fromkeys(ltool.getSupportedLanguages(), u'')
    return values

language_choice = schema.Choice(
    title=_(u"Language"),
    vocabulary="plone.app.vocabularies.SupportedContentLanguages",
)


class MultiLanguageTextLine(schema.Dict):

    def __init__(self, key_type=None, value_type=None, **kw):
        defaultFactory = kw.get('defaultFactory', languageDefaultFactory)
        super(MultiLanguageTextLine, self).__init__(**kw)
        self.defaultFactory = defaultFactory
        self.key_type = language_choice
        self.value_type = schema.TextLine(
            title=kw.get('title'),
            required=kw.get('required', False),
        )

    def validate(self, value):
        request = self.context.REQUEST
        if request.method == 'GET':
            return
        super(MultiLanguageTextLine, self).validate(value)

        ltool = getToolByName(self.context, 'portal_languages')
        default_lang = ltool.getDefaultLanguage()

        # check if default language value is given only if
        # there are values given
        if any(value.values()):
            for key, item in value.items():
                try:
                    old_required = self.value_type.required
                    self.value_type.required = key == default_lang
                    self.value_type.validate(item)
                except ValidationError:
                    raise DefaultLanguageMissing(self.__name__)
                finally:
                    self.value_type.required = old_required


class MultiLanguageText(schema.Dict):

    def __init__(self, key_type=None, value_type=None, **kw):
        defaultFactory = kw.get('defaultFactory', languageDefaultFactory)
        super(MultiLanguageText, self).__init__(**kw)
        self.defaultFactory = defaultFactory
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

    def toWidgetValue(self, value):
        """Include items for each language in the site.
        """
        if value is self.field.missing_value:
            return {}
        converter = self._getConverter(self.field.value_type)
        key_converter = self._getConverter(self.field.key_type)

        ltool = getToolByName(self.widget.context, 'portal_languages')
        default_lang = ltool.getDefaultLanguage()

        tmp = OrderedDict()
        tmp[default_lang] = value.get(default_lang, None)
        tmp.update(dict.fromkeys(ltool.getSupportedLanguages(), u''))
        tmp.update(value)

        values = [(key_converter.toWidgetValue(k), converter.toWidgetValue(v))
                  for k, v in tmp.items()]
        return values
