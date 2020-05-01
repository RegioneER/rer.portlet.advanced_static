from zope.i18nmessageid import MessageFactory

RERPortletAdvancedStaticMessageFactory = MessageFactory(
    "rer.portlet.advanced_static"
)

import logging

logger = logging.getLogger("rer.portlet.advanced_static")

registry_key = "rer.portlet.advanced_static.css_styles"


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
