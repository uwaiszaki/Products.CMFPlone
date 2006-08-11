from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.migrations.v2_1.alphas import reindexCatalog, \
     indexMembersFolder

def final_two51(portal):
    """2.5-final -> 2.5.1
    """
    out = []
    removePloneCssFromRR(portal, out)

    # add event_registration.js
    addEventRegistrationJS(portal, out)

    # Required for #5569 (is_folderish needs reindexing) and #5231 (all text
    # indices need to be reindexed so they are split properly)
    reindexCatalog(portal, out)

    # FIXME: *Must* be called after reindexCatalog.
    # In tests, reindexing loses the folders for some reason...

    # Make sure the Members folder is cataloged
    indexMembersFolder(portal, out)

    return out

def removePloneCssFromRR(portal, out):
    """Removes the redundant, deprecated, and failing plone.css from portal_css.
       It is a python script now and just calls portal_css itself."""
    css_reg = getToolByName(portal, 'portal_css', None)
    if css_reg is not None:
        stylesheet_ids = css_reg.getResourceIds()
        if 'plone.css' in stylesheet_ids:
            css_reg.unregisterResource('plone.css')
            out.append('Unregistered deprecated plone.css')

def addEventRegistrationJS(portal, out):
    """Add event-registration.js to ResourceRegistries.
    """
    jsreg = getToolByName(portal, 'portal_javascripts', None)
    script = 'event-registration.js'
    if jsreg is not None:
        script_ids = jsreg.getResourceIds()
        # Failsafe: first make sure the stylesheet doesn't exist in the list
        if script not in script_ids:
            jsreg.registerScript(script)
            # put it at the top of the stack
            jsreg.moveResourceToTop(script)
            out.append("Added " + script + " to portal_javascipt")

