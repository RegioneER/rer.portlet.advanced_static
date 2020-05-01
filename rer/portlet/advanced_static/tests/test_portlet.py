from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.app.portlets.storage import PortletAssignmentMapping
from rer.portlet.advanced_static import rerportletadvancedstatic
from rer.portlet.advanced_static.tests.base import (
    RER_PORTLET_ADVANDED_STATIC_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from rer.portlet.advanced_static import registry_key
import unittest


class PortletIntegrationTest(unittest.TestCase):

    layer = RER_PORTLET_ADVANDED_STATIC_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.app = self.layer["app"]
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name="rer.portlet.advanced_static.RERPortletAdvancedStatic",
        )
        self.assertEquals(
            portlet.addview,
            "rer.portlet.advanced_static.RERPortletAdvancedStatic",
        )

    def test_interfaces(self):
        # TODO: Pass any keyword arguments to the Assignment constructor
        portlet = rerportletadvancedstatic.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name="rer.portlet.advanced_static.RERPortletAdvancedStatic",
        )
        mapping = self.portal.restrictedTraverse(
            "++contextportlets++plone.leftcolumn"
        )
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse("+/" + portlet.addview)

        # TODO: Pass a dictionary containing dummy form inputs from the add
        # form.
        # Note: if the portlet has a NullAddForm, simply call
        # addview() instead of the next line.
        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(
            isinstance(
                list(mapping.values())[0], rerportletadvancedstatic.Assignment
            )
        )

    def test_invoke_edit_view(self):
        # NOTE: This test can be removed if the portlet has no edit form
        mapping = PortletAssignmentMapping()
        request = self.portal.REQUEST

        mapping["foo"] = rerportletadvancedstatic.Assignment()
        editview = getMultiAdapter((mapping["foo"], request), name="edit")
        self.failUnless(
            isinstance(editview, rerportletadvancedstatic.EditForm)
        )

    def test_obtain_renderer(self):
        context = self.portal
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse("@@plone")
        manager = getUtility(
            IPortletManager, name="plone.rightcolumn", context=self.portal
        )

        # TODO: Pass any keyword arguments to the Assignment constructor
        assignment = rerportletadvancedstatic.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer
        )
        self.failUnless(
            isinstance(renderer, rerportletadvancedstatic.Renderer)
        )

    def test_setup(self):
        registry = getUtility(IRegistry)
        self.assertTrue(registry_key in registry)


class TestRenderer(unittest.TestCase):

    layer = RER_PORTLET_ADVANDED_STATIC_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.app = self.layer["app"]
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def renderer(
        self,
        context=None,
        request=None,
        view=None,
        manager=None,
        assignment=None,
    ):
        context = context or self.portal
        request = request or self.portal.REQUEST
        view = view or self.portal.restrictedTraverse("@@plone")
        manager = manager or getUtility(
            IPortletManager, name="plone.rightcolumn", context=self.portal
        )

        # TODO: Pass any default keyword arguments to the Assignment
        # constructor.
        assignment = assignment or rerportletadvancedstatic.Assignment()
        return getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer
        )

    def test_render(self):
        context = self.portal
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse("@@plone")
        manager = getUtility(
            IPortletManager, name="plone.leftcolumn", context=self.portal
        )
        assignment = rerportletadvancedstatic.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer
        )
        self.assertTrue(
            isinstance(renderer, rerportletadvancedstatic.Renderer)
        )
