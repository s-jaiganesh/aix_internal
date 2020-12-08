#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'none'
}

DOCUMENTATION = r'''
---
author:
- Jai Ganesh
module: install_all_updates
short_description: update all packages
description:
- This module perform update all packages from the given repository path
version_added: '1.0'
'''

EXAMPLES = r'''
- name: Preview update
  install_all_updates:
    path: /mnt/foo
    preview: True

- name: Update
  install_all_updates:
    path: /mnt/foo
    preview: False
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule

cmd = module.get_bin_path('install_all_updates', True)
def _update_all(module, preview, path):

    if preview is False:
        udpate_all_cmd = "%s '%s' %s '%s' " % (cmd, '-d', path, '-Y')
    else:
        udpate_all_cmd = "%s '%s' %s '%s' " % (cmd, '-d', path, '-pY')

    rc, out, err = module.run_command("%s" % (udpate_all_cmd))    
    if rc is 0:
        msg = "command: %s preview: %s has completed successfully" % (udpate_all_cmd, preview)
        result = { 'stdout' : out, 'stderr' : err, 'rc' : rc, 'changed' : True, 'msg' : msg }
        module.exit_json(**result)
    else:
        msg = "command: %s preview: %s has completed successfully" % (udpate_all_cmd, preview)
        result = { 'stdout' : out, 'stderr' : err, 'rc' : rc, 'changed' : False, 'msg' : msg }
        module.exit_json(**result)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', required=True),
            preview=dict(type='bool',default=False),
        ),
        supports_check_mode=True,
    )
    path = module.params['path']
    preview = module.params['preview']

    _update_all(module, preview, path)    

if __name__ == '__main__':
    main()
