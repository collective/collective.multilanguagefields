from plone.dexterity.interfaces import IDexterityContent
from zope.interface import implements, Interface


class IHasMultiLanguageFields(IDexterityContent):
    """Marker interface for multilanguage fields behavior
    """


class INameFromTitle(Interface):
    """Marker interface
    """


class NameFromMultiLanguageTitle(object):
    implements(INameFromTitle)

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
