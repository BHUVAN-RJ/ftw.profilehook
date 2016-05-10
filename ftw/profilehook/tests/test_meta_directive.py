from ftw.profilehook.interfaces import IProfileHook
from unittest2 import TestCase
from ftw.profilehook.testing import PROFILEHOOK_INTEGRATION_TESTING
from zope.component import getAdapter


def hook(site):
    pass


class TestMetaDirective(TestCase):
    layer = PROFILEHOOK_INTEGRATION_TESTING

    def test_registering_hook_registers_adapter(self):
        self.layer['load_zcml_string'](
            '<configure'
            '   xmlns="http://namespaces.zope.org/zope"'
            '   xmlns:five="http://namespaces.zope.org/five"'
            '   xmlns:profilehook="http://namespaces.zope.org/profilehook">'

            ' <include package="ftw.profilehook" />'
            ' <profilehook:hook'
            '     profile="ftw.profilehook.tests:foo"'
            '     handler="{0}.hook"'
            '     />'

            '</configure>'.format(self.__module__))


        self.assertEquals(hook, getAdapter(self.layer['portal'],
                                           IProfileHook,
                                           name='ftw.profilehook.tests:foo'))
