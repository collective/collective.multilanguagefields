from collective.multilanguagefields.interfaces import \
    INameFromMultiLanguageTitle
#from plone.app.content.interfaces import INameFromTitle
from zope.interface import implements


class INameFromMultiLanguageTitle(object):
    implements(INameFromMultiLanguageTitle)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        # Default to English title
        title = self.context.title.get('en')
        if not title:
            # Else, pick the first available language
            values = self.context.title.values()
            if not values:
                raise ValueError  # title should be required
            title = values[0]
        return title
