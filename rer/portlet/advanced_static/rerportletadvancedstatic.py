from Products.ATContentTypes.interface import IATImage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.portlet.static import static
from plone.portlets.interfaces import IPortletDataProvider
from rer.portlet.advanced_static import \
    RERPortletAdvancedStaticMessageFactory as _
from zope import schema
from zope.app.form.browser.itemswidgets import SelectWidget
from zope.formlib import form
from zope.interface import implements
from plone.memoize import ram
from time import time

SelectWidget._messageNoValue = _("vocabulary-missing-single-value-for-edit",
                      "-- select a value --")

def _advstatic_cachekey(method, self,img_path):
    """
    method for ramcache that store time and searched userid
    """
    timestamp = time() // (60 * 30 * 1)
    return "%s:%s" % (timestamp,img_path)

class IRERPortletAdvancedStatic(static.IStaticPortlet):
    """
    A custom static text portlet
    """
    text = schema.Text(
        title=_(u"Text"),
        description=_(u"The text to render"),
        required=False)
    
    image= schema.Choice(title=_(u"Background image"),
                                description=_(u"Insert an image that will be shown as background of the header"),
                                required=False,
                                source=SearchableTextSourceBinder({'object_provides' : IATImage.__identifier__},
                                                                    default_query='path:'))
    
    internal_url= schema.Choice(title=_(u"Internal link"),
                                description=_(u"Insert an internal link. This field override external link field"),
                                required=False,
                                source=SearchableTextSourceBinder({'sort_on':'getObjPositionInParent'}, default_query='path:'))

    portlet_class = schema.TextLine(title=_(u"Portlet class"),
                                    required=False,
                                    description=_(u"CSS class to add at the portlet"))
    
    css_style = schema.Choice(title=_(u"Portlet style"),
                              description=_(u"Choose a CSS style for the portlet"),
                              required=False,
                              vocabulary='rer.portlet.advanced_static.CSSVocabulary',)

class Assignment(static.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IRERPortletAdvancedStatic)

    image = ''
    assignment_context_path = None
    internal_url = ''
    portlet_class= ''
    css_style = ''
        
    def __init__(self, header=u"", text=u"", omit_border=False, footer=u"",
                 more_url='', hide=False,assignment_context_path = None,
                 image = '', internal_url = '', portlet_class= '', css_style = ''):
        super(Assignment, self).__init__(header=header,
                                         text=text,
                                         omit_border=omit_border,
                                         footer=footer,
                                         more_url=more_url)
        
        self.image = image
        self.assignment_context_path = assignment_context_path
        self.internal_url = internal_url
        self.portlet_class= portlet_class
        self.css_style = css_style

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        if self.header:
            return self.header
        else:
            return "RER portlet advanced static"


class Renderer(static.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('rerportletadvancedstatic.pt')
    
    def getPortletClass(self):
        classes="portlet rerPortletAdvancedStatic"
        if self.data.portlet_class:
            classes +=" %s" %self.data.portlet_class
        if self.data.css_style:
            classes +=" %s" %self.data.css_style
        return classes
    
    def getImgUrl(self):
        root=self.context.portal_url()
        return "%s%s" %(root,self.data.image)
    
    @ram.cache(_advstatic_cachekey)
    def getImgHeight(self,img_path):
        self.context.plone_log('------------QUI----------------')
        root='/'.join(self.context.portal_url.getPortalObject().getPhysicalPath())
        img_obj=self.context.restrictedTraverse("%s%s" %(root,img_path))
        if not img_obj:
            return ""
        return str(img_obj.getImage().height)
    
    @property
    def getImageStyle(self):
        img_url=self.getImgUrl()
        height=self.getImgHeight(self.data.image)
        style="background-image:url(%s)" %img_url
        if height:
            style += ";height:%spx" %height
        return style
    
    def getPortletLink(self):
        if self.data.internal_url:
            root_path= self.context.portal_url.getPortalObject().getPhysicalPath()
            item_url= '/'.join(root_path) + self.data.internal_url
            return item_url
        else:
            return self.data.more_url or ""
            
class AddForm(static.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IRERPortletAdvancedStatic)
    form_fields['text'].custom_widget = WYSIWYGWidget
    form_fields['image'].custom_widget = UberSelectionWidget
    form_fields['internal_url'].custom_widget = UberSelectionWidget
    def create(self, data):
        assignment_context_path = \
                    '/'.join(self.context.__parent__.getPhysicalPath())
        return Assignment(assignment_context_path=assignment_context_path,
                          **data)


class EditForm(static.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IRERPortletAdvancedStatic)
    form_fields['text'].custom_widget = WYSIWYGWidget
    form_fields['image'].custom_widget = UberSelectionWidget
    form_fields['internal_url'].custom_widget = UberSelectionWidget