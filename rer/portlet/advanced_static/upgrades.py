# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from rer.portlet.advanced_static import logger
from rer.portlet.advanced_static import registry_key
from plone import api


default_profile = "profile-rer.portlet.advanced_static:default"


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """

    def wrap_func(fn):
        def wrap_func_args(context, *args):
            p = getToolByName(context, "portal_quickinstaller").get(
                upgrade_product
            )
            setattr(p, "installedversion", version)
            return fn(context, *args)

        return wrap_func_args

    return wrap_func


@upgrade("rer.portlet.advanced_static", "1.3.0")
def to_1_3_0(context):
    """
    Add css stylesheet
    """
    logger.info("Upgrading rer.portlet.advanced_static to version 1.3.0")
    context.runImportStepFromProfile(default_profile, "cssregistry")
    logger.info("Upgrade done: added cssregistry")


@upgrade("rer.portlet.advanced_static", "3.0.0")
def migrate_to_3000(context):
    """
    """
    logger.info("Upgrading rer.portlet.advanced_static to version 3.0.0")
    context.runImportStepFromProfile(default_profile, "plone.app.registry")

    values = api.portal.get_registry_record(
        "collective.tiles.advancedstatic.css_styles"
    )
    api.portal.set_registry_record(registry_key, values)

    logger.info(
        "Upgrade done: upgrade registry moving tile styles on new registry"
        " record specific for rer.portlet.advanced_static"
    )
