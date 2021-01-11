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
module: GPC_bosboot
short_description: Create boot image and set boot list
description:
- This module creates boot image on disks
version_added: '1.0'
'''

EXAMPLES = r'''
- name: Create a volume group datavg
  GPC_bosboot:
    state: present
    bootlist: True
    
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule

def bosboot(module):
    
    bosboot_cmd = module.get_bin_path('bosboot', True)
    rc, out, err = module.run_command("%s -a" % (bosboot_cmd))
    if rc != 0:
        changed = False
        err = err.rstrip(b"\r\n")
        stderr=err
        rc=rc
        module.exit_json(msg="unable to run %s command." % bosboot_cmd)
    else:             
        out = out.rstrip(b"\r\n")
        stdout=out
        rc=rc
        changed = True
        bosboot_msg = "bosboot to executed"
        module.exit_json(msg="successfully executed")
    
def bootlist(module):      
        
    lslv_cmd = module.get_bin_path('lslv', True)
    rc, hd5_pvs, err = module.run_command("%s -l '%s'" % (lslv_cmd, 'hd5'))
    if rc != 0:
        changed = False
        module.fail_json(msg="67:Failing to execute '%s' command." % lslv_cmd)

    pvs_to_set_bootlist = []
    for line in hd5_pvs.splitlines():
        if 'hdisk' in line:
            fields = line.strip().split()
            pvs_to_set_bootlist.append(fields[0])
            hdisk = fields[0]
            state = fields[1]
    
    bootlist_cmd = module.get_bin_path('bootlist', True)
    
    if len(pvs_to_set_bootlist) == 2:

        rc, out, err = module.run_command("%s -m normal %s %s" % (bootlist_cmd, (pvs_to_set_bootlist[0]), (pvs_to_set_bootlist[1])))
        if rc != 0:
            changed = False
            err = err.rstrip(b"\r\n")
            stderr=err
            rc=rc
            module.fail_json(msg="88:Failing to execute '%s' command." % bootlist_cmd)
        else:
            out = out.rstrip(b"\r\n")
            stdout=out
            rc=rc
            changed = True
            bootlist_msg = "Bootlist has been set successfully"
            module.exit_json(msg="bootlist set successfully")

    elif len(pvs_to_set_bootlist) == 1:
        
        rc, out, err = module.run_command("%s -m normal %s" % (bootlist_cmd, pvs_to_set_bootlist[0]))
        if rc != 0:
            changed = False
            err = err.rstrip(b"\r\n")
            stderr=err
            rc=rc
            module.fail_json(msg="104:Failing to execute '%s' command." % bootlist_cmd)
        else:
            out = out.rstrip(b"\r\n")
            stdout=out
            rc=rc
            changed = True
            bootlist_msg = "Bootlist has been set successfully"
            module.exit_json(msg="bootlist set successfully")
    else:
        changed = False
        bootlist_msg = "No Boot image present on any PV"
        module.fail_json(msg="114:Failing to execute '%s' command." % lslv_cmd)

    msg = bootlist_msg
    return changed, msg
           
    
def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', required=True),
            bootlist=dict(type='bool',default=False),
        ),
        supports_check_mode=True,
    )
    if module.params['state'] == 'present':
        bosboot(module)
        if module.params['bootlist'] is True:
            bootlist(module)
        else:
            module.fail_json(msg="Not valid input")
    else:
        module.fail_json(msg="Not valid input")
        
if __name__ == '__main__':
    main()
