from Acquisition import aq_inner
from plone.app.form.base import EditForm
from Products.ATContentTypes.interface import IATContentType
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from zope import schema
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.interface import implements
from zope.formlib import form

PROJECT_NAME = 'quintagroup.substyle'

_ = MessageFactory(PROJECT_NAME)


def IdTitleDesc(value):
    """ Convert value(id:title:description) to id, title and description
    """
    values = value.split(":")
    if len(values) == 1:
        return value, value, value
    elif len(values) == 2:
        return values[0], values[1], values[1]
    elif len(values) == 3:
        return values[0], values[1], values[2]


class ISetStyleSchema(Interface):
    pass


class SetStyleAdapter(SchemaAdapterBase):
    adapts(IATContentType)
    implements(ISetStyleSchema)

    def __init__(self, context):
        portal_properties = getToolByName(context, 'portal_properties')
        site_props = getattr(portal_properties, 'site_properties')
        self.customsubslyles = site_props.getProperty('customsubstyles', [])
        for v in self.customsubslyles:
            i, j, k = IdTitleDesc(v)

            def get_prop(x, prop=i):
                context = x.context
                if context.hasProperty(prop):
                    return context.getProperty(prop)
                else:
                    return ''

            def set_prop(x, value, prop=i):
                context = x.context
                if value:
                    if not context.hasProperty(prop):
                        context.manage_addProperty(prop, value, 'string')
                    else:
                        context.manage_changeProperties(**{prop: value})
                else:
                    if context.hasProperty(prop):
                        context.manage_delProperties([prop, ])

            setattr(SetStyleAdapter, i, property(get_prop, set_prop))
        super(SetStyleAdapter, self).__init__(context)


class SetStyleForm(EditForm):
    label = _("Edit style form")
    description = _("This form is for managing styles for current item.")

    def __init__(self, context, *a, **b):
        portal_properties = getToolByName(context, 'portal_properties')
        site_props = getattr(portal_properties, 'site_properties')
        self.customsubslyles = site_props.getProperty('customsubstyles', [])
        self.status = site_props.getProperty('substyleshelp', None)
        customsubslylesdict = []
        for v in self.customsubslyles:
            i, j, k = IdTitleDesc(v)
            customsubslylesdict.append(schema.TextLine(title=_(j),
                    description=_(k),
                    __name__=i,
                    required=False,))
            setattr(ISetStyleSchema, i, schema.TextLine(title=_(j),
                    description=_(k),
                    __name__=i,
                    required=False,))
        for i in customsubslylesdict:
            i.interface = ISetStyleSchema
        self.form_fields = form.FormFields(ISetStyleSchema) +\
                           form.FormFields(*customsubslylesdict)
        super(SetStyleForm, self).__init__(context, *a, **b)


class LocalCSS(BrowserView):
    """The local.css
    """

    def getLocalStyleData(self):
        """Get local style data
        """
        context = aq_inner(self.context)
        localStyleData = {}
        portal_properties = getToolByName(context, 'portal_properties')
        site_props = getattr(portal_properties, 'site_properties')
        PROPERTIES = [IdTitleDesc(i)[0]
                      for i in site_props.getProperty('customsubslyles', [])
                      if i]
        for prop in PROPERTIES:
            prop_value = getattr(context, prop, None)
            if prop_value:
                localStyleData[prop] = prop_value
            else:
                localStyleData[prop] = ""
        return localStyleData

    def css(self):
        """css view
            'backgroundcolor':'
.documentFirstHeading {background-color:%(backgroundcolor)s;}
.documentEditable * .standalone {background-color:%(backgroundcolor)s;}
form.searchPage input.searchButton {background:%(backgroundcolor)s;}
#portal-footer {background-color:%(backgroundcolor)s;}
#portal-top {background-color:%(backgroundcolor)s;}
            ',
        """
        css_map = {}

        return ' '.join([v % self.getLocalStyleData()
                         for k, v in css_map.items()
                         if self.getLocalStyleData()[k]])
