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
    backgroundcontentcolor = schema.TextLine(
        title=_(u'Background Content Color'),
        description=_(u"This value is directly inserted into css styles, so "
                       "be careful and enter valid css colour."),
        required=False,
        )
    backgroundhovercolor = schema.TextLine(
        title=_(u'Background Hover Color'),
        description=_(u"This value is directly inserted into css styles, so "
                       "be careful and enter valid css colour."),
        required=False,
        )


class SetStyleAdapter(SchemaAdapterBase):
    adapts(IATFolder)
    implements(ISetStyleSchema)

    backgroundcolor = ProxyFieldProperty(ISetStyleSchema['backgroundcolor'])
    backgroundcontentcolor = ProxyFieldProperty(ISetStyleSchema['backgroundcontentcolor'])
    backgroundhovercolor = ProxyFieldProperty(ISetStyleSchema['backgroundhovercolor'])


class SetStyleForm(EditForm):

    form_fields = form.FormFields(ISetStyleSchema)

    label = _("Edit style form")
    description = _("This form is for managing colour for current folder.")

