from collective.multilanguagefields import MessageFactory as _
from zope import schema


class TextLine(schema.Dict):

    def __init__(self, key_type=None, value_type=None, **kw):
        super(TextLine, self).__init__(**kw)
        self.key_type = schema.Choice(
            title=_(u"Language"),
            vocabulary="plone.app.vocabularies.SupportedContentLanguages",
        )
        self.value_type = schema.TextLine(
            title=kw.get('title'),
        )
