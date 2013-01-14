# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from rer.portlet.advanced_static import logger

default_profile = 'profile-rer.portlet.advanced_static:default'


def upgrade(upgrade_product, version):
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context, *args):
            p = getToolByName(context, 'portal_quickinstaller').get(upgrade_product)
            setattr(p, 'installedversion', version)
            return fn(context, *args)
        return wrap_func_args
    return wrap_func


@upgrade('rer.portlet.advanced_static', '1.3.0')
def to_1_3_0(context):
    """
    Add css stylesheet
    """
    logger.info('Upgrading rer.portlet.advanced_static to version 1.3.0')
    context.runImportStepFromProfile(default_profile, 'cssregistry')
    logger.info('Upgrade done: added cssregistry')
