from Products.CMFCore.utils import getToolByName


def ml_field(context, fieldname):
    """Retrieve a single field value for the current language
    """
    values = getattr(context, fieldname, None)
    if not values:
        return ''
    ltool = getToolByName(context, 'portal_languages')
    default_language = ltool.getDefaultLanguage()
    # use request language or site default language
    language = context.REQUEST.get('LANGUAGE', default_language)
    value = values.get(language, '')
    if not value:
        # return site default language
        value = values.get(default_language)
        if not value:
            # return random language
            value = values.values()[0]
    return value
