# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import rer.portlet.advanced_static


class RerPortletAdvancedStaticLayer(PloneSandboxLayer):
    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=rer.portlet.advanced_static)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "rer.portlet.advanced_static:default")


RER_PORTLET_ADVANDED_STATIC_FIXTURE = RerPortletAdvancedStaticLayer()


RER_PORTLET_ADVANDED_STATIC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(RER_PORTLET_ADVANDED_STATIC_FIXTURE,),
    name="RerPortletAdvancedStaticLayer:IntegrationTesting",
)
