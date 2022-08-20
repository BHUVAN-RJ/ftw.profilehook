import re

import six
from ftw.profilehook.interfaces import IBeforeImportHook, IProfileHook
from zope.component import queryAdapter
from zope.component.hooks import getSite


def profile_imported(event):
    if not event.full_import:
        return

    if not isinstance(event.profile_id, (str, six.text_type)):
        return

    trigger_hook_for(event.profile_id, IProfileHook)


def before_profile_import(event):
    if not event.full_import:
        return

    if not isinstance(event.profile_id, (str, six.text_type)):
        return

    trigger_hook_for(event.profile_id, IBeforeImportHook)


def trigger_hook_for(profile, providing):
    profile = re.sub('^profile-', '', profile)
    site = getSite()
    hook = queryAdapter(site, providing, name=profile)
    if hook:
        hook(site)
