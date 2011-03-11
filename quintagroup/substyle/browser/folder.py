from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope import schema
from zope.formlib import form

from plone.app.form.base import EditForm
from plone.app.controlpanel.form import ControlPanelForm

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.ATContentTypes.interface import IATContentType

from Products.ATContentTypes.interface import IATFolder

from zope.i18nmessageid import MessageFactory

PROJECT_NAME = 'quintagroup.substyle'

_ = qMessageFactory = MessageFactory(PROJECT_NAME)

from Products.Five.browser import BrowserView
from Acquisition import aq_inner

PROPERTIES = {
    'backgroundcolor' :  'Background Color',
    'backgroundcontentcolor' :    'Background Content Color',
    'backgroundhovercolor' :    'Background Hover Color',
    }


class ISetStyleSchema(Interface):
    backgroundcolor = schema.TextLine(
        title=_(u'Background Color'),
        description=_(u"This value is directly inserted into css styles, so "
                       "be careful and enter valid css colour."),
        required=False,
        )
    #backgroundcontentcolor = schema.TextLine(
        #title=_(u'Background Content Color'),
        #description=_(u"This value is directly inserted into css styles, so "
                       #"be careful and enter valid css colour."),
        #required=False,
        #)
    #backgroundhovercolor = schema.TextLine(
        #title=_(u'Background Hover Color'),
        #description=_(u"This value is directly inserted into css styles, so "
                       #"be careful and enter valid css colour."),
        #required=False,
        #)


class SetStyleAdapter(SchemaAdapterBase):
    adapts(IATFolder)
    implements(ISetStyleSchema)

    def __init__(self, context):
        portal_properties = getToolByName(context, 'portal_properties')
        site_properties = getattr(portal_properties, 'site_properties')
        self.customsubslyles = site_properties.getProperty('customsubslyles',[])
        for i in self.customsubslyles:
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
                        context.manage_changeProperties(**{prop:value})
                else:
                    if context.hasProperty(prop):
                        context.manage_delProperties([prop,])

            setattr(SetStyleAdapter, i, property(get_prop, set_prop))
        super(SetStyleAdapter, self).__init__(context)

    backgroundcolor = ProxyFieldProperty(ISetStyleSchema['backgroundcolor'])


class SetStyleForm(EditForm):
    label = _("Edit style form")
    description = _("This form is for managing colour for current folder.")

    def __init__(self, context, *a, **b):
        portal_properties = getToolByName(context, 'portal_properties')
        site_properties = getattr(portal_properties, 'site_properties')
        self.customsubslyles = site_properties.getProperty('customsubslyles',[])
        customsubslylesdict = []
        for i in self.customsubslyles:
            customsubslylesdict.append(schema.TextLine(title=_(i),
                    description=_(u"This value is directly inserted into css styles, so "
                       "be careful and enter valid css colour."),
                    __name__=i,
                    required=False,))
            setattr(ISetStyleSchema, i, schema.TextLine(title=_(i),
                    description=_(u"This value is directly inserted into css styles, so "
                       "be careful and enter valid css colour."),
                    __name__=i,
                    required=False,))
        for i in customsubslylesdict:
            i.interface = ISetStyleSchema
        self.form_fields = form.FormFields(ISetStyleSchema) + form.FormFields(*customsubslylesdict)
        super(SetStyleForm, self).__init__(context, *a, **b)


class LocalCSS(BrowserView):
    """The local.css
    """

    def getLocalStyleData(self):
        """Get local style data
        """
        context = aq_inner(self.context)
        localStyleData={}
        PROPERTIES = ['backgroundcolor']
        portal_properties = getToolByName(context, 'portal_properties')
        site_properties = getattr(portal_properties, 'site_properties')
        PROPERTIES.extend(site_properties.getProperty('customsubslyles',[]))
        defaultImgId = "limage.jpg"
        contextImgId = 'top-image.jpg'

        image_path = '/'.join([context.portal_url(), defaultImgId])
        top_image = getattr(context, contextImgId, None)
        if top_image:
            image_path = top_image.absolute_url()
        localStyleData['topliningImg'] = 'url(%s)' % image_path

        for prop in PROPERTIES:
            prop_value = getattr(context, prop, None)
            if prop_value:
                localStyleData[prop] = prop_value
            else:
                localStyleData[prop] = ""
        return localStyleData

    def css(self):
        """css view
        """
        css_map = {
            'backgroundcolor':"""
.documentFirstHeading {background-color:%(backgroundcolor)s;}
.standalone, .documentEditable * .standalone {background-color:%(backgroundcolor)s;}
form.searchPage input.searchButton {background:%(backgroundcolor)s;}
#portal-footer {background-color:%(backgroundcolor)s;}
#portal-top {background-color:%(backgroundcolor)s;}
            """,
            'backgroundhovercolor':"""
.navTreeLevel1 .navTreeItem a:hover span {color:%(backgroundhovercolor)s;border-color:%(backgroundhovercolor)s;}
.navTreeLevel1 a.navTreeCurrentItem span {color:%(backgroundhovercolor)s;border-color:%(backgroundhovercolor)s;}
a {color:%(backgroundhovercolor)s;}
            """,
            'backgroundcontentcolor':"""
#visual-portal-wrapper {background-color:%(backgroundcontentcolor)s;}
.fieldRequired {color:%(backgroundcontentcolor)s;}
#content {background-color:%(backgroundcontentcolor)s;}
.portletHeader {background-color:%(backgroundcontentcolor)s;}
            """,
            }

        return ' '.join([v % self.getLocalStyleData() for k, v in css_map.items() if self.getLocalStyleData()[k]])
