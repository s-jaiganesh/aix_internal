#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'none'
}
DOCUMENTATION = '''
---
module: aix_list_devices
short_description: lsdev command module

version_added: "1.0"

description:
    - "This is a custom module for lsdev -C command"

author:
    - Jai Ganesh
'''

EXAMPLES = '''
- name: List disks from Lsdev command
  aix_list_devices:
    name: disk

- name: List fcs from Lsdev command
  aix_list_devices:
    name: fcs    

- name: List ethernet from Lsdev command
  aix_list_devices:
    name: ent    

- name: List eth channel from Lsdev command
  aix_list_devices:
    name: port
'''

from ansible.module_utils.basic import AnsibleModule

def _list_devices(module, _device):

    lsdev_cmd = module.get_bin_path('lsdev', True)
    rc, out, err = module.run_command("%s '-C'" % (lsdev_cmd)
    if rc is 0:        
        _devices = []
        for line in out.splitlines():
            if _device in line:
                _devices.append(line)
            if len(_devices) is 0:
                result = { 'stdout':'', 'stderr':'', 'rc':rc, 'changed':False, 'msg': "Device not found" }
                module.exit_json(**result)
            else:
                result = { 'stdout':_devices, 'stderr':'', 'rc':rc, 'changed':False, 'msg': "command successful" }
                module.exit_json(**result)
                
    if rc != 0:
        result = { 'stdout': '', 'stderr':out, 'rc':rc, 'changed':False, 'msg': "Failed to execute the command" }
        module.exit_json(**result)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )
    name = module.params['name']
    if name == 'disk':
        _list_devices(module, 'hdisk')
    elif name == 'fcs':
        _list_devices(module, 'fcs')
    elif name == 'ent':
        _list_devices(module, 'ent')
    elif name == 'port':
        _list_devices(module, 'EtherChannel')
    else
        module.fail_json(msg="Invalid input")
        
if __name__ == '__main__':
    main()
