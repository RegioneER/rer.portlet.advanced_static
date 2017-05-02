from Products.CMFCore.utils import getToolByName


def import_various(context):
    if context.readDataFile('advanced_static-various.txt') is None:
        return

    portal = context.getSite()
