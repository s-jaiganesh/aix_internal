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
    
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule

def bosboot(module):

    # Define pvs_to_run_bosboot (list of physical volumes to run bosboot).
    lslv_cmd = module.get_bin_path('lslv', True)
    rc, hd5_pvs, err = module.run_command("%s -l '%s'" % (lslv_cmd, 'hd5'))
    if rc != 0:
        module.fail_json(msg="Failing to execute '%s' command." % lslv_cmd)

    pvs_to_run_bosboot = []
    for line in hd5_pvs.splitlines()[2:]:
        pvs_to_run_bosboot.append(line.split()[0])   
    
    if len(pvs_to_run_bosboot) <= 0:
        changed = False
        bosboot_msg = "No Boot image present on any PV"
        return changed, msg
    elif len(pvs_to_run_bosboot) == 2:
        bosboot_cmd = module.get_bin_path('bosboot', True)
        rc, stdout, stderr = module.run_command("%s -ad %s" % (bosboot_cmd, '/dev/'.join(pvs_to_run_bosboot)))
        if rc != 0:
            changed = False
            module.fail_json(msg="Unable to run bosboot '%s' '%s' '%s'" % rc=rc, stdout=stdout, stderr=stderr)
        else:
            changed = True
            bosboot_msg = "Bosboot executed on '%s'"
    elif len(pvs_to_run_bosboot) == 1:
        bosboot_cmd = module.get_bin_path('bosboot', True)
        rc, stdout, stderr = module.run_command("%s -ad %s" % (bosboot_cmd, '/dev/'.join(pvs_to_run_bosboot)))
        if rc != 0:
            changed = False
            module.fail_json(msg="Unable to run bosboot '%s' '%s' '%s'" % rc=rc, stdout=stdout, stderr=stderr)
        else:
            changed = True
            bosboot_msg = "Bosboot executed on '%s'"
    else:
    msg = bosboot_msg
    return changed, msg
    
    
def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )

    name = module.params['name']    
    changed, msg = bosboot(module)

if __name__ == '__main__':
    main()
