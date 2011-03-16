"""Some utility functions for common use"""

from Products.CMFCore.utils import getToolByName

def getVocabulary(context):
    pp = getToolByName(context, 'portal_properties', None)
    styles = None
    if pp is not None:
        sheet = getattr(pp, 'rer_staticportlet_properties', None)
        if sheet is not None:
            dropdown_list = sheet.getProperty('portlet_styles_menu', None)
            if dropdown_list is not None:
                styles = []
                value_list = []
                for line in dropdown_list:
                    values = filter(lambda x:x.strip(), line.split('|', 1))
                    if len(values) == 0:
                        continue
                    elif len(values) == 1:
                        value = title = values[0]
                    else:
                        value = values[0]
                        title = values[1]
                    if value not in value_list:
                        value_list.append(value)
                        styles.append((value.decode('utf-8'), title.decode('utf-8')))
    return styles