from Products.CMFCore.utils import getToolByName

def import_various(context):
    if context.readDataFile('advanced_static-various.txt') is None:
        return
    
    portal = context.getSite()
    addPropertySheet(portal)
    
def addPropertySheet(portal):
    portal_properties = getToolByName(portal, 'portal_properties')
    rer_staticportlet_properties = getattr(portal_properties, 'rer_staticportlet_properties',None)
    if not rer_staticportlet_properties:
        portal_properties.addPropertySheet(id='rer_staticportlet_properties',title='RER Advanced static portlet properties')
        portal.plone_log("Added RER Advanced static portlet properties property-sheet")
        rer_staticportlet_properties = getattr(portal_properties, 'rer_staticportlet_properties',None)
    if not rer_staticportlet_properties.hasProperty('portlet_styles_menu'):
        rer_staticportlet_properties.manage_addProperty('portlet_styles_menu', "", 'lines')