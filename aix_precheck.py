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
- Mr. Jai
module: aix_precheck
short_description: Collect precheck before patching
description:
- This module creates boot image on disks
version_added: '1.0'
options:
  name:
    description:
    - name of action example, bosboot, bootlist
    type: str
    default: yes
'''

EXAMPLES = r'''
- name: Create a volume group datavg
  aix_precheck:
    name: bosboot
    bootlist: True
    
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule

def bosboot(module, bootlist_bool):

    # Define pvs_to_run_bosboot (list of physical volumes to run bosboot).
    lslv_cmd = module.get_bin_path('lslv', True)
    rc, hd5_pvs, err = module.run_command("%s -l '%s'" % (lslv_cmd, 'hd5'))
    if rc != 0:
        module.fail_json(msg="Failing to execute '%s' command." % lslv_cmd)

    pvs_to_run_bosboot = []
    for line in b.splitlines():
    if 'hdisk' in line:
        fields = line.strip().split()
        pvs_to_run_bosboot.append(fields[0])
        hdisks = fields[0]
        state = fields[1]
    
    length = len(pvs_to_run_bosboot)
    bosboot_cmd = ("%s %s %s" % ('bootlist -m normal', '/dev/' + (hdisk[0]), '/dev/' + (hdisk[1])))
    
    if len(pvs_to_run_bosboot) <= 0:
        changed = False
        bosboot_msg = "No Boot image present on any PV"
        return changed, msg
    elif len(pvs_to_run_bosboot) == 2:
        bosboot_cmd = module.get_bin_path('bosboot', True)
        for disk in pvs_to_run_bosboot:
            rc, stdout, stderr = module.run_command("%s -ad %s" % (bosboot_cmd, 'bosboot', '/dev/' + disk))

        if rc != 0:
            changed = False
            module.fail_json(msg="Unable to run bosboot")
        else:
            changed = True
            bosboot_msg = "Bosboot executed"

    elif len(pvs_to_run_bosboot) == 1:
        bosboot_cmd = module.get_bin_path('bosboot', True)
        rc, stdout, stderr = module.run_command("%s -ad %s" % (bosboot_cmd, 'bosboot', '/dev/' + (pvs_to_run_bosboot[0])))
        if rc != 0:
            changed = False
            module.fail_json(msg="Unable to run bosboot") 
        else:
            changed = True
            bosboot_msg = "Bosboot executed"
    else:
        changed = False
        bosboot_msg = "unknown failure"
        module.fail_json(msg="Unable to run bosboot")

    msg = bosboot_msg
    return changed, msg, length
    
    
def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            bootlist=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    name = module.params['name']
    bootlist = module.params['bootlist']
    changed, msg = bosboot(module, bootlist)

if __name__ == '__main__':
    main()
