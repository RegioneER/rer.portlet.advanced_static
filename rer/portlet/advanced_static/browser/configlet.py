from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope import schema
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget
from zope.app.form.browser import ListSequenceWidget
from zope.formlib import form

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.form import ControlPanelForm

from rer.portlet.advanced_static import RERPortletAdvancedStaticMessageFactory as _
from rer.portlet.advanced_static.utility.utils import getVocabulary


class IValueTitlePair(Interface):
    value = schema.TextLine(title=u"value", required=True)
    title = schema.TextLine(title=u"title", required=False)

class ValueTitlePair(object):
    implements(IValueTitlePair)
    def __init__(self, value='', title=''):
        self.value = value
        self.title = title

class IRERAdvancedStaticPortletControlPanelSchema(Interface):

    portlet_styles_menu = schema.List(
        title=_(u'Dropdown select'),
        description=_(u"These entries are used for generating dropdown select "
                      "for advanced static portlet. Note: pipe (|) "
                      "symbol is not allowed in the value field."),
        value_type=schema.Object(IValueTitlePair, title=u"entry"),
        required=True
    )

class RERAdvancedStaticPortletControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IRERAdvancedStaticPortletControlPanelSchema)

    def __init__(self, context):
        super(RERAdvancedStaticPortletControlPanelAdapter, self).__init__(context)
        self.context = context
        self.pp = getToolByName(context, 'portal_properties', None)

    def get_portlet_styles_menu(self):
        return  [ValueTitlePair(v,t) for (v,t) in getVocabulary(self.context)]

    def set_portlet_styles_menu(self, value):
        dropdown_list = []
        for vt in value:
            value = vt.value
            title = vt.title or value
            dropdown_list.append('%s|%s' % (value.encode('utf-8'), title.encode('utf-8')))
        self.setValue(dropdown_list)

    portlet_styles_menu = property(get_portlet_styles_menu, set_portlet_styles_menu)

    def setValue(self, value):
        if self.pp is not None:
            if getattr(self.pp, 'rer_staticportlet_properties', None) is None:
                self.pp.addPropertySheet(
                    'rer_staticportlet_properties',
                    'RER Advanced static portlet properties'
                )
            sheet = getattr(self.pp, 'rer_staticportlet_properties', None)
            if not sheet.hasProperty('portlet_styles_menu'):
                sheet.manage_addProperty('portlet_styles_menu', value, 'lines')
            else:
                sheet.manage_changeProperties(portlet_styles_menu=value)

valuetitle_widget = CustomWidgetFactory(ObjectWidget, ValueTitlePair)
combination_widget = CustomWidgetFactory(ListSequenceWidget,
                                         subwidget=valuetitle_widget)

class RERAdvancedStaticPortletControlPanel(ControlPanelForm):

    form_fields = form.FormFields(IRERAdvancedStaticPortletControlPanelSchema)
    form_fields['portlet_styles_menu'].custom_widget = combination_widget

    label = _("RER Advanced static portlet settings")
    description = _("This form is for managing RER Advanced static portlet "
                     "classes available on portlet add/edit form.")
    form_name = _("RER Advanced static portlet settings")

