try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from Products.CMFCore.utils import getToolByName

from rer.portlet.advanced_static.utility.utils import getVocabulary
from rer.portlet.advanced_static import RERPortletAdvancedStaticMessageFactory as _

class CSSVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = []
        styles = getVocabulary(context)
        charset = self._charset(context)
        for value, title in styles:
            if not isinstance(title, unicode):
                title = title.decode(charset)
            if not isinstance(value, unicode):
                value = value.decode(charset)
            items.append(SimpleTerm(value, value, _(title)))
        items.sort(lambda x,y:cmp(x.title,y.title))
        return SimpleVocabulary(items)

    def _charset(self, context):
        pp = getToolByName(context, 'portal_properties', None)
        if pp is not None:
            site_properties = getattr(pp, 'site_properties', None)
            if site_properties is not None:
                return site_properties.getProperty('default_charset', 'utf-8')
        return 'utf-8'

CSSVocabulary = CSSVocabulary()
