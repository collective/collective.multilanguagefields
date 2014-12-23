from plone.app.content.interfaces import INameFromTitle as Base


class INameFromMultiLanguageTitle(Base):

    def title():
        """Return a title from a dictionary"""
