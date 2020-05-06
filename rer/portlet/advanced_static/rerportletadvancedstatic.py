# -*- coding: utf-8 -*-
from plone.app.vocabularies.catalog import CatalogSource
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlet.static import static
from rer.portlet.advanced_static import (
    RERPortletAdvancedStaticMessageFactory as _,
)
from zope import schema
from zope.interface import implementer
import sys
from plone.memoize import view
from plone import api


class IRERPortletAdvancedStatic(static.IStaticPortlet):
    """
    A custom static text portlet
    """

    target_attr = schema.Bool(
        title=_(u"Open links in a new window"),
        description=_(
            u"Tick this box if you want to open the header "
            "and footer links in a new window"
        ),
        required=False,
        default=False,
    )

    image_ref = schema.Choice(
        title=_(u"Background image"),
        description=_(
            u"Insert an image that will be shown as background of the header"
        ),
        required=False,
        source=CatalogSource(portal_type="Image"),
    )

    image_ref_height = schema.Int(
        title=_(u"Background image height"),
        description=_(
            u"Specify image background's height (in pixels). If empty will"
            " be used image's height."
        ),
        required=False,
    )

    internal_url = schema.Choice(
        title=_(u"Internal link"),
        description=_(
            u"Insert an internal link. This field override external link field"
        ),
        required=False,
        source=CatalogSource(),
    )

    portlet_class = schema.TextLine(
        title=_(u"Portlet class"),
        required=False,
        description=_(u"CSS class to add at the portlet"),
    )

    css_style = schema.Choice(
        title=_(u"Portlet style"),
        description=_(u"Choose a CSS style for the portlet"),
        required=False,
        vocabulary="rer.portlet.advanced_static.CSSVocabulary",
    )


@implementer(IRERPortletAdvancedStatic)
class Assignment(static.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    target_attr = False
    image_ref = ""
    image_ref_height = None
    assignment_context_path = None
    internal_url = ""
    portlet_class = ""
    css_style = ""

    def __init__(
        self,
        header=u"",
        text=u"",
        omit_border=False,
        footer=u"",
        more_url="",
        target_attr=False,
        hide=False,
        assignment_context_path=None,
        image_ref="",
        image_ref_height=None,
        internal_url="",
        portlet_class="",
        css_style="",
    ):
        self.header = header
        self.text = text
        self.omit_border = omit_border
        self.footer = footer
        self.more_url = more_url
        self.target_attr = target_attr
        self.image_ref = image_ref
        self.image_ref_height = image_ref_height
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

    render = ViewPageTemplateFile("rerportletadvancedstatic.pt")

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
        if not self.image_object:
            return ""
        return self.image_object.absolute_url()

    @property
    @view.memoize
    def image_object(self):
        """
        get the image object
        """
        imageUID = self.data.image_ref
        if not imageUID:
            return ""

        return api.content.get(UID=imageUID)

    def getImgHeight(self):
        """
        return the image height
        """
        image = self.image_object
        if not image:
            return ""
        # compatibility with dexterity images
        blobimage = getattr(image, "image", None)
        if blobimage:
            return blobimage.getImageSize()[1]
        return str(image.getImage().height)

    def getImageStyle(self):
        """
        set background image, if present
        """
        img_url = self.getImgUrl()
        if not img_url:
            return None
        if self.data.image_ref_height:
            height = self.data.image_ref_height
        else:
            height = self.getImgHeight()

        style = "background-image:url(%s)" % img_url
        if height:
            style += ";height:%spx" % height
        return style

    def getPortletLink(self):
        default_link = self.data.more_url or ""
        if not self.data.internal_url:
            return default_link
        item = api.content.get(UID=self.data.internal_url)
        if not item:
            return default_link
        return item.absolute_url()

    def getLinkTitle(self):
        if self.data.target_attr:
            return _(u"Opens in a new window")
        else:
            return ""


class AddForm(static.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    schema = IRERPortletAdvancedStatic

    def create(self, data):
        assignment_context_path = "/".join(
            self.context.__parent__.getPhysicalPath()
        )
        return Assignment(
            assignment_context_path=assignment_context_path, **data
        )


class EditForm(static.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    schema = IRERPortletAdvancedStatic
