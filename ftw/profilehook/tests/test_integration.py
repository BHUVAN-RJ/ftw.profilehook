from plone.app.testing import applyProfile
from ftw.profilehook.testing import PROFILEHOOK_INTEGRATION_TESTING
from ftw.profilehook.tests.base import ZCMLIsolationTestCase


class CallCounter(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.calls = 0

    def __call__(self, site):
        self.calls += 1


call_counter = CallCounter()


class TestIntegration(ZCMLIsolationTestCase):
    layer = PROFILEHOOK_INTEGRATION_TESTING

    def tearDown(self):
        super(TestIntegration, self).tearDown()
        call_counter.reset()

    def test_hook_is_called_when_profile_is_imported(self):
        self.load_zcml_string(
            '<configure xmlns="http://namespaces.zope.org/zope"'
            '           xmlns:five="http://namespaces.zope.org/five"'
            '           xmlns:profilehook="http://namespaces.zope.org/profilehook">'
            ' <include package="ftw.profilehook" />'
            ' <profilehook:hook'
            '     profile="ftw.profilehook.tests:foo"'
            '     handler="{0}.call_counter"'
            '     />'
            '</configure>'.format(self.__module__))

        applyProfile(
            self.layer['portal'], 'ftw.profilehook.tests:foo')

        self.assertEquals(1, call_counter.calls)

    def test_hook_is_not_called_when_other_objects_are_imported(self):
        self.load_zcml_string(
            '<configure xmlns="http://namespaces.zope.org/zope"'
            '           xmlns:five="http://namespaces.zope.org/five"'
            '           xmlns:profilehook="http://namespaces.zope.org/profilehook">'
            ' <include package="ftw.profilehook" />'
            ' <profilehook:hook'
            '     profile="ftw.profilehook.tests:bar"'
            '     handler="{0}.call_counter"'
            '     />'
            '</configure>'.format(self.__module__))

        applyProfile(
            self.layer['portal'], 'ftw.profilehook.tests:foo')

        self.assertEquals(0, call_counter.calls)
