from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('collective.multilanguagefields')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
