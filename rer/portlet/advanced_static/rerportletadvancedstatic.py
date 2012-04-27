from Products.ATContentTypes.interface import IATImage
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.portlet.static import static
from rer.portlet.advanced_static import \
    RERPortletAdvancedStaticMessageFactory as _
from zope import schema
from zope.app.form.browser.itemswidgets import SelectWidget
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter
import sys

SelectWidget._messageNoValue = _("vocabulary-missing-single-value-for-edit",
                      "-- select a value --")


class IRERPortletAdvancedStatic(static.IStaticPortlet):
    """
    A custom static text portlet
    """
    text = schema.Text(
        title=_(u"Text"),
        description=_(u"The text to render"),
        required=False)

    image_ref = schema.Choice(title=_(u"Background image"),
                                description=_(u"Insert an image that will be shown as background of the header"),
                                required=False,
                                source=SearchableTextSourceBinder({'object_provides': IATImage.__identifier__},
                                                                    default_query='path:'))

    internal_url = schema.Choice(title=_(u"Internal link"),
                                description=_(u"Insert an internal link. This field override external link field"),
                                required=False,
                                source=SearchableTextSourceBinder({'sort_on': 'getObjPositionInParent'}, default_query='path:'))

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

    image_ref = ''
    assignment_context_path = None
    internal_url = ''
    portlet_class = ''
    css_style = ''

    def __init__(self, header=u"", text=u"", omit_border=False, footer=u"",
                 more_url='', hide=False, assignment_context_path=None,
                 image_ref='', internal_url='', portlet_class='', css_style=''):
        self.header = header
        self.text = text
        self.omit_border = omit_border
        self.footer = footer
        self.more_url = more_url
        self.image_ref = image_ref
        self.assignment_context_path = assignment_context_path
        self.internal_url = internal_url
        self.portlet_class = portlet_class
        self.css_style = css_style
        if sys.version_info < (2, 6):
            self.hide = hide

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
        classes = "portlet rerPortletAdvancedStatic"
        if self.data.portlet_class:
            classes += " %s" % self.data.portlet_class
        if self.data.css_style:
            classes += " %s" % self.data.css_style
        return classes

    def getImgUrl(self):
        """
        return the image url
        """
        image = self.getImageObject(self.data.image_ref)
        if image:
            return image.absolute_url()
        else:
            return ""

    def getImageObject(self, img_path):
        """
        get the image object
        """
        root = self.context.portal_url.getPortalObject()
        return root.restrictedTraverse(img_path.strip('/'), None)

    def getImgHeight(self):
        """
        return the image height
        """
        image = self.getImageObject(self.data.image_ref)
        if not image:
            return ""
        return str(image.getImage().height)

    def getImageStyle(self):
        """
        set background image, if present
        """
        #get a string that define if there is an old-version image,
        #and manage the background with the two cases
        portlet_image = self.getRightImageVersion()
        if not portlet_image:
            return ''
        elif portlet_image == 'new':
            img_url = self.getImgUrl()
            height = self.getImgHeight()
        elif portlet_image == 'old':
            img_url = self.getOldImgUrl()
            height = self.getOldImgHeight()

        style = "background-image:url(%s)" % img_url
        if height:
            style += ";height:%spx" % height
        return style

    def getRightImageVersion(self):
        """
        if the image_ref is set, return 'new'.
        If the image_ref is not set, check if there is an old-type image and return 'old'
        """
        if self.data.image_ref:
            return 'new'
        image_old = getattr(self.data, 'image', None)
        if image_old:
            return 'old'
        return ''

    def getOldImgUrl(self):
        """
        old method that returns image url
        """
        # BBB
        if isinstance(self.data.image, basestring):
            return "%s/image" % self.getImageObject(self.data.image).absolute_url()
        else:
            state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
            portal = state.portal()
            assignment_url = portal.unrestrictedTraverse(self.data.assignment_context_path).absolute_url()
            return "%s/%s/@@image" % (assignment_url, self.data.__name__)

    def getOldImgHeight(self):
        """
        old method that returns image height
        """
        # BBB
        if isinstance(self.data.image, basestring):
            return str(self.getImageObject(self.data.image).height)
        else:
            return str(self.data.image.height)

    def getPortletLink(self):
        if self.data.internal_url:
            root = self.context.portal_url.getPortalObject()
            item = root.restrictedTraverse(self.data.internal_url.strip('/'), None)
            if item:
                return item.absolute_url()
            else:
                return ''
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
    form_fields['image_ref'].custom_widget = UberSelectionWidget
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
    form_fields['image_ref'].custom_widget = UberSelectionWidget
    form_fields['internal_url'].custom_widget = UberSelectionWidget

    @form.action(_(u"label_save", default=u"Save"),
                 condition=form.haveInputWidgets,
                 name=u'save')
    def handle_save_action(self, action, data):
        """
        override of action, to remove old image reference, when a new image is selected
        """
        if data.get('image_ref', '') and getattr(self.context.data, 'image', None):
            self.context.data.image = None
        return super(EditForm, self).actions.byname['form.actions.save'].success_handler(self, action, data)
