from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
#from z3c.form.widget import MultiWidget
from zope.component.hooks import getSite
from zope import schema
from collective.multilanguagefields import MessageFactory as _


class MultilanguageField(object):

    security = ClassSecurityInfo()
    _v_lang = None
    reset = True

    def _getTool(self, context):
        try:
            return getToolByName(context, 'portal_languages')
        except:
            try:
                return getToolByName(getSite(), 'portal_languages')
            except:
                pass
        return None

    def _getLangFromStorage(self, instance, lang):
        try:
            return self.getStorage(instance).get(
                '%s___%s___' % (self.__name__, lang), instance)
        except AttributeError:
            return None

    def _getCurrentLanguage(self, context):
        try:
            return self._getTool(context).getPreferredLanguage()
        except AttributeError:
            return 'en'

    security.declarePrivate('set')

    def set(self, instance, value):
        """Language-aware attribute setter.

        Modified from zope.schema._bootstrapfields.Field
        """
        #import ipdb; ipdb.set_trace()
        # do readonly-check (copied from zope.schema._bootstrapfields.Field)
        if self.readonly:
            raise TypeError("Can't set values on read-only fields "
                            "(name=%s, class=%s.%s)"
                            % (self.__name__,
                               object.__class__.__module__,
                               object.__class__.__name__))
        # our language-aware implementation starts here
        #languages = self._getTool(instance).listSupportedLanguages()

        if not isinstance(value, dict):
            if self._v_lang:
                # reset = False
                value = {self._v_lang: value}
            else:
                value = {self._getCurrentLanguage(instance): value}

        setattr(object, self.__name__, value)


class TextLine(schema.Dict):

    def __init__(self, key_type=None, value_type=None, **kw):
        super(TextLine, self).__init__(**kw)
        self.key_type = schema.TextLine(
            title=_(u"Language"),
        )
        self.value_type = schema.TextLine(
            title=kw.get('title'),
        )
