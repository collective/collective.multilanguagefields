from Products.CMFCore.utils import getToolByName


def ml_value(context, fieldname, default=None):
    """Retrieve a field value for the current language
    """
    values = getattr(context, fieldname)
    if not values and default is not None:
        return default
    ltool = getToolByName(context, 'portal_languages')
    default_language = ltool.getDefaultLanguage()
    # use request language or site default language
    language = context.REQUEST.get('LANGUAGE', default_language)
    value = values.get(language, values.get(default_language, None))
    if value is not None:
        return value
    # fall back to default language if preferred langiage is unavailable
    value = values.get(default_language, None)
    if value is not None:
        return value
    # return default value parameter, if set
    if default is not None:
        return default
    message = "No translation available for fieldname %s in language %s " \
              "nor in default language %s. (%r)"
    raise ValueError(
        message % (fieldname, language, default_language, context))
