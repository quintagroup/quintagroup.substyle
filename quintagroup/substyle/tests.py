# -*- coding: utf-8 -*-
import unittest

from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.interfaces import (PLONE_SITE_ID,
                                          SITE_OWNER_NAME,
                                          SITE_OWNER_PASSWORD)
from zope.configuration import xmlconfig
from selenium.webdriver.firefox.webdriver import WebDriver


class Substyle(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import quintagroup.substyle
        xmlconfig.file(
            'configure.zcml', quintagroup.substyle, context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'quintagroup.substyle:default')

    def setUp(self):
        super(Substyle, self).setUp()

    def tearDown(self):
        super(Substyle, self).tearDown()

SUBSTYLE_FIXTURE = Substyle()

EMBEDLY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(SUBSTYLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="Substyle:Acceptance")


class TestConfiglet(unittest.TestCase):
    layer = EMBEDLY_ACCEPTANCE_TESTING

    def setUp(self):
        self.wd = WebDriver()
        self.wd.implicitly_wait(10)

    def tearDown(self):
        self.wd.quit()

    def test_test3(self):
        success = True
        wd = self.wd
        page_url = "http://localhost:55001/%s" % PLONE_SITE_ID
        wd.get(page_url)
        wd.find_element_by_id("personaltools-login").click()
        wd.find_element_by_id("__ac_name").click()
        wd.find_element_by_id("__ac_name").clear()
        wd.find_element_by_id("__ac_name").send_keys(SITE_OWNER_NAME)
        wd.find_element_by_id("__ac_password").click()
        wd.find_element_by_id("__ac_password").clear()
        wd.find_element_by_id("__ac_password").send_keys(SITE_OWNER_PASSWORD)
        wd.find_element_by_name("submit").click()
        wd.find_element_by_id("user-name").click()
        wd.find_element_by_link_text("Site Setup").click()
        wd.find_element_by_link_text("Zope Management Interface").click()
        wd.find_element_by_link_text(
            "portal_properties (General settings registry)").click()
        wd.find_element_by_link_text(
            "site_properties (Site wide properties)").click()
        wd.find_element_by_name("id:string").click()
        wd.find_element_by_name("id:string").clear()
        wd.find_element_by_name("id:string").send_keys("customsubstyles")
        if not wd.find_element_by_xpath("//form[2]/table/tbody/tr[1]/td[4]/div/select/option[5]").is_selected():
            wd.find_element_by_xpath(
                "//form[2]/table/tbody/tr[1]/td[4]/div/select/option[5]").click()
        wd.find_element_by_name("submit").click()
        wd.find_element_by_name("customsubstyles:lines").click()
        wd.find_element_by_name("customsubstyles:lines").clear()
        wd.find_element_by_name("customsubstyles:lines").send_keys(
            "style_id:style_title:style_description")
        wd.find_element_by_name("manage_editProperties:method").click()
        wd.get(page_url)
        wd.find_element_by_xpath(
            "//dl[@id='plone-contentmenu-factories']//span[.='Add new…']").click()
        wd.find_element_by_xpath("//a[@id='document']//span[.='Page']").click()
        wd.find_element_by_id("title").click()
        wd.find_element_by_id("title").clear()
        wd.find_element_by_id("title").send_keys("Page")
        wd.find_element_by_name("form.button.save").click()
        page_url = wd.current_url
        wd.find_element_by_link_text("Set Style").click()
        if not ("style_title" in wd.find_element_by_tag_name("html").text):
            success = False
            print("verifyTextPresent failed")
        if not ("style_description" in wd.find_element_by_tag_name("html").text):
            success = False
            print("verifyTextPresent failed")
        wd.find_element_by_id("form.style_id").click()
        wd.find_element_by_id("form.style_id").clear()
        wd.find_element_by_id("form.style_id").send_keys("test")
        wd.find_element_by_id("form.actions.save").click()
        wd.find_element_by_id("user-name").click()
        wd.find_element_by_link_text("Site Setup").click()
        wd.find_element_by_link_text("Zope Management Interface").click()
        wd.find_element_by_link_text(
            "portal_properties (General settings registry)").click()
        wd.find_element_by_link_text(
            "site_properties (Site wide properties)").click()
        wd.find_element_by_name("customsubstyles:lines").click()
        wd.find_element_by_name("customsubstyles:lines").clear()
        wd.find_element_by_name("customsubstyles:lines").send_keys(
            "style_id:style_title:style_description\nbackgroundcolor:background color:background")
        wd.find_element_by_name("manage_editProperties:method").click()
        wd.get(page_url)
        wd.find_element_by_link_text("Set Style").click()
        wd.find_element_by_id("form.backgroundcolor").click()
        wd.find_element_by_id("form.backgroundcolor").clear()
        wd.find_element_by_id("form.backgroundcolor").send_keys("red")
        wd.find_element_by_id("form.actions.save").click()
        self.assertTrue(success)


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestConfiglet),

        # Unit tests
        # doctestunit.DocFileSuite(
        #    'README.txt', package='quintagroup.substyle',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        # doctestunit.DocTestSuite(
        #    module='quintagroup.substyle.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        # ztc.ZopeDocFileSuite(
        #    'README.txt', package='quintagroup.substyle',
        #    test_class=TestCase),

        # ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='quintagroup.substyle',
        #    test_class=TestCase),

    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
