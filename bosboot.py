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
        return False        
    else:             
        out = out.rstrip(b"\r\n")
        stdout=out
        rc=rc
        changed = True
        bosboot_msg = "bosboot to executed"
        return True
    
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
            return False
        else:
            out = out.rstrip(b"\r\n")
            stdout=out
            rc=rc
            changed = True
            bootlist_msg = "Bootlist has been set successfully"
            return True

    elif len(pvs_to_set_bootlist) == 1:
        
        rc, out, err = module.run_command("%s -m normal %s" % (bootlist_cmd, pvs_to_set_bootlist[0]))
        if rc != 0:
            changed = False
            err = err.rstrip(b"\r\n")
            stderr=err
            rc=rc
            diskname = pvs_to_set_bootlist[0]
            bootlist_msg = "Bootlist not set successfully"
            out_value = False
            return changed, diskname, out, out_value
        else:
            out = out.rstrip(b"\r\n")
            diskname = pvs_to_set_bootlist[0]
            stdout=out
            rc=rc
            changed = True
            bootlist_msg = "Bootlist has been set successfully"
            out_value = True
            return changed, diskname, out, out_value
    else:
        changed = False
        bootlist_msg = "No Boot image present on any PV"
        module.fail_json(msg="114:Failing to execute '%s' command." % lslv_cmd)         
    
def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', required=True),
            bootlist=dict(type='bool',default=False),
        ),
        supports_check_mode=True,
    )
    if module.params['state'] == 'present':
        bosboot_return = bosboot(module)
        if module.params['bootlist'] is True and bosboot_return:
            changed, diskname, out, out_value = bootlist(module)
            #out_value, out, diskname = bootlist(module)
            if out_value:
                msg = "bosboot command executed and bootlist set successfully" 
                result = {"msg": msg, "changed": changed}
                module.exit_json(**result)
            else:
                msg = "bosboot command executed and bootlist not set successfully"
                result = {"msg": msg, "changed": changed}
                module.fail_json(**result)
        elif bosboot_return == 'False':
            module.fail_json(msg="bosboot command not executed successfully")
        else:
            module.fail_json(msg="unknown error")
    else:
        module.fail_json(msg="Not valid input")
        
if __name__ == '__main__':
    main()
