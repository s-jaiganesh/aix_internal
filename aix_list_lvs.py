#!/usr/bin/python
import json

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'patching team'
}

DOCUMENTATION = '''
---
module: aix_list_lv
short_description: 
version_added: "1.0"
description:
    - "Get inforamtion about logical volumes"
author:
    - Jai Ganesh
'''

EXAMPLES = '''
- name: Get all closed LVs
  aix_list_lv:
    name: all
    state: closed
- name: Get all stale LVs
  aix_list_lv:
    name: all
    state: stale
- name: Get information about particular LV (lslv <lvname>)
  aix_list_lv:
    name: oralv    
- name: Get all LVs from particular VG (lsvg -l <vgname>)
  aix_list_lv:
    vgname: oravg
'''
from ansible.module_utils.basic import AnsibleModule, load_platform_subclass

def _get_lv_status(module, lvname):
    lslv_cmd = module.get_bin_path('lslv', True)
    rc, out, err = module.run_command("%s %s" % lslv_cmd, lvname)
    if rc is 0:
        return True
    else:
        module.fail_json(msg = "%s is not a valid logical volume" % lvname)

def _get_lv_info(module, lvname):
    lslv_cmd = module.get_bin_path('lslv', True)
    rc, out, err = module.run_command("%s %s" % (lslv_cmd, lvname))
    result = { 'stdout':out, 'stderr':err, 'rc':rc, 'changed':True }
    module.exit_json(**result)

def _list_all_lvs(module):
    lsvg_cmd = module.get_bin_path('lsvg', True)
    lslv_cmd = module.get_bin_path('lslv', True)
    rc, vgs, err = module.run_command("%s -o" % (lsvg_cmd))
    
    for line in vgs.splitlines():
        rc, lvs, err = module.run_command("%s -l %s" % (lsvg_cmd, line))
        lines = lvs.split('\n',2)[-1]
        lv_data.append(lines)
    result = { 'stdout':lv_data, 'stderr':err, 'rc':rc, 'changed':True }
    module.exit_json(**result)
    
def _list_stale_lvs(module):
    lsvg_cmd = module.get_bin_path('lsvg', True)
    lslv_cmd = module.get_bin_path('lslv', True)
    rc, vgs, err = module.run_command("%s -o" % (lsvg_cmd))
    
    for line in vgs.splitlines():
        rc, lvs, err = module.run_command("%s -l %s" % (lsvg_cmd, line))
        lines = lvs.split('\n',2)[-1]
        for line in lines.splitlines():
            fields = line.strip().split()
            if fields[5] == "closed/stale" and fields[5] == "open/stale":
                _stale_lvs.append(fields)
    if len(_stale_lvs) is 0:        
        result = { 'stdout':_stale_lvs, 'stderr':err, 'rc':rc, 'changed':False }
        module.exit_json(**result)
    else:
        result = { 'stdout':_stale_lvs, 'stderr':err, 'rc':rc, 'changed':True }
        module.exit_json(**result)

def _list_closed_lvs(module):
    lsvg_cmd = module.get_bin_path('lsvg', True)
    lslv_cmd = module.get_bin_path('lslv', True)
    rc, vgs, err = module.run_command("%s -o" % (lsvg_cmd))
    
    for line in vgs.splitlines():
        rc, lvs, err = module.run_command("%s -l %s" % (lsvg_cmd, line))
        lines = lvs.split('\n',2)[-1]
        for line in lines.splitlines():
            fields = line.strip().split()
            if fields[5] == "closed/stale" and fields[5] == "closed/syncd":
                _closed_lvs.append(fields)
    if len(_closed_lvs) is 0:        
        result = { 'stdout':_closed_lvs, 'stderr':err, 'rc':rc, 'changed':False }
        module.exit_json(**result)
    else:
        result = { 'stdout':_closed_lvs, 'stderr':err, 'rc':rc, 'changed':True }
        module.exit_json(**result)

def _get_lvs_from_vg(module, vgname):
    lsvg_cmd = module.get_bin_path('lsvg', True)    
    rc, vgs, err = module.run_command("%s -l $s" % (lsvg_cmd, vgname))
     
def main():
    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=False),
            state=dict(type='str'),
            vgname=dict(type='str'),
        ),
        supports_check_mode=True,
    )
    if module.check_mode:
        module.exit_json(**result)

    lvname = module.params['name']
    state = module.params['state']
    vgname = module.params['vgname']
    
    if lvname == 'all' and state == 'all':
        _list_all_lvs(module)
    elif lvname == 'all' and state == 'stale':
        _list_stale_lvs(module)
    elif lvname == 'all' and state == 'closed':
        _list_closed_lvs(module)
    elif _get_lv_status(module, lvname):
        _get_lv_info(module, lvname)
    else:
        module.fail_json(msg = "Not valid input. Refer Documentation & Examples.")
    if lvname is None and vgname:
        _get_lvs_from_vg(module, vgname)
        

if __name__ == '__main__':
    main()
