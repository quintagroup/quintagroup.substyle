# -*- coding: utf-8 -*-
import unittest
import os
import sys
import new
from random import randint
import base64
import json
import httplib
from selenium import webdriver

from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.interfaces import (PLONE_SITE_ID,
                                          SITE_OWNER_NAME,
                                          SITE_OWNER_PASSWORD)
from zope.configuration import xmlconfig


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

SUBSTYLE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(SUBSTYLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="Substyle:Acceptance")


class TestSubstyle(unittest.TestCase):
    layer = SUBSTYLE_ACCEPTANCE_TESTING

    __test__ = False

    def setUp(self):
        self.caps['name'] = 'quintagroup.substyle'
        if os.environ.get('TRAVIS'):
            self.caps['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
            self.caps['build'] = os.environ['TRAVIS_BUILD_NUMBER']
            self.caps['tags'] = [os.environ['TRAVIS_PYTHON_VERSION'], os.environ['PLONE'], 'CI']

        self.username = os.environ['SAUCE_USERNAME']
        self.key = os.environ['SAUCE_ACCESS_KEY']
        hub_url = "%s:%s@ondemand.saucelabs.com:80" % (self.username, self.key)
        self.wd = webdriver.Remote(desired_capabilities=self.caps,
                                   command_executor="http://%s/wd/hub" % hub_url)
        self.jobid = self.wd.session_id
        self.wd.implicitly_wait(30)

    def report_test_result(self):
        base64string = base64.encodestring('%s:%s'
                                           % (self.username, self.key))[:-1]
        result = json.dumps({'passed': sys.exc_info() == (None, None, None)})
        connection = httplib.HTTPConnection("saucelabs.com")
        connection.request('PUT',
                           '/rest/v1/%s/jobs/%s' % (self.username, self.jobid),
                           result,
                           headers={"Authorization": "Basic %s" % base64string})
        result = connection.getresponse()
        return result.status == 200

    def tearDown(self):
        self.wd.quit()
        self.report_test_result()

    def test_substyle(self):
        success = True
        wd = self.wd
        plone_url = "http://localhost:55001/%s" % PLONE_SITE_ID
        site_properties_url = "%s/portal_properties/site_properties/manage_propertiesForm" % plone_url
        wd.get(plone_url)
        wd.find_element_by_id("personaltools-login").click()
        wd.find_element_by_id("__ac_name").click()
        wd.find_element_by_id("__ac_name").clear()
        wd.find_element_by_id("__ac_name").send_keys(SITE_OWNER_NAME)
        wd.find_element_by_id("__ac_password").click()
        wd.find_element_by_id("__ac_password").clear()
        wd.find_element_by_id("__ac_password").send_keys(SITE_OWNER_PASSWORD)
        wd.find_element_by_name("submit").click()
        wd.get(site_properties_url)
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
        wd.get(plone_url)
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
        wd.get(site_properties_url)
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


PLATFORMS = [
    {
        'browserName': 'firefox',
    },
    {
        'browserName': 'chrome',
    },
]


def test_suite():
    suite = unittest.TestSuite()
    for platform in PLATFORMS:
        d = dict(TestSubstyle.__dict__)
        name = "%s_%s_%s_%s" % (TestSubstyle.__name__,
                                platform['browserName'],
                                platform.get('platform', 'ANY'),
                                randint(0, 999))
        name = name.replace(" ", "").replace(".", "")
        d.update({'__test__': True, 'caps': platform})
        suite.addTest(unittest.makeSuite(new.classobj(name, (TestSubstyle,), d)))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
