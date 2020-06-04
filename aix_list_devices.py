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
- name: Get disks that are available
  aix_list_devices:
    name: disk
    state: present
    
- name: Get disks that are Defined or unavailable state
  aix_list_devices:
    name: disk
    state: absent
    
- name: Get fcs that are available
  aix_list_devices:
    name: fcs   
    state: present
    
- name: List ethernet from Lsdev command
  aix_list_devices:
    name: ent   
    state: all
    
- name: List eth channel from Lsdev command
  aix_list_devices:
    name: port
    state: all
'''

from ansible.module_utils.basic import AnsibleModule

def _list_devices(module, name, _state):

    if name == 'disk':
        _device = 'hdisk'
    elif name == 'fcs':
        _device = 'fcs'
    elif name == 'ent':
        _device = 'ent'
    elif name == 'port':
        _device = 'EtherChannel'

    lsdev_cmd = module.get_bin_path('lsdev', True)
    rc, out, err = module.run_command("%s '-C'" % (lsdev_cmd))
    if rc is 0:        
        _devices = []
        for line in out.splitlines():
            if _device in line:
                if _state == 'all':
                    _devices.append(line)
                elif _state == 'present':
                    fields = line.strip().split()
                    if fields[1] == 'Available':
                        _devices.append(line)
                elif _state == 'absent':
                    fields = line.strip().split()
                    if fields[1] != 'Available':
                        _devices.append(line)
                else:
                    module.fail_json(msg = "Invalid option")
                
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
            state=dict(type='str', required=True, choices=['present', 'absent', 'all']),
        ),
        supports_check_mode=True,
    )
    name = module.params['name']
    state = module.params['state']
    _list_devices(module, name, state)   
        
if __name__ == '__main__':
    main()
