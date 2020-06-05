#!/usr/bin/python
import json

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'patching team'
}

DOCUMENTATION = '''
---
module: list_vg
short_description: lsvg module

version_added: "1.0"

description:
    - "Get inforamtion about volume groups"

author:
    - Jai Ganesh
'''

EXAMPLES = '''
- name: Get result of lsvg <vgname>
  aix_list_vg:
    name: datavg    

- name: Get result of lsvg 
  aix_list_vg:
    name: all
    state: all

- name: Get result of lsvg -o
  aix_list_vg:
    name: all
    state: active

- name: Get result of in active VGs
  aix_list_vg:
    name: all
    state: inactive

'''
from ansible.module_utils.basic import AnsibleModule, load_platform_subclass
cmd = 'lsvg'

def _get_vg_status(module, vgname):
    lsvg_cmd = module.get_bin_path('lsvg', True)    
    rc, out, err = module.run_command("%s %s" % lsvg_cmd, vgname)
    if rc is 0:
        return True
    else:
        module.fail_json(msg = "%s is not a valid volume group name" % vgname)

def _get_vg_info(module, vgname):
    lsvg_cmd = module.get_bin_path('lsvg', True)    
    rc, out, err = module.run_command("%s %s" % (lsvg_cmd, vgname))
    result = { 'stdout':out, 'stderr':err, 'rc':rc, 'changed':True }
    module.exit_json(**result)

def _list_vg(module):
    lsvg_cmd = module.get_bin_path('lsvg', True)    
    rc, out, err = module.run_command(lsvg_cmd)
    result = { 'stdout':out, 'stderr':err, 'rc':rc, 'changed':True }
    module.exit_json(**result)
    
def _list_active_vg(module):
    lsvg_cmd = module.get_bin_path('lsvg', True)    
    rc, out, err = module.run_command("%s -o" % (lsvg_cmd))    
    result = { 'stdout':out, 'stderr':err, 'rc':rc, 'changed':True }
    module.exit_json(**result)

def _list_inactive_vg(module):
    _lsvg, _active_vg, _inactive_vg = ([] for i in range(3))
    lsvg_cmd = module.get_bin_path('lsvg', True)
    rc, allvg, err = module.run_command("%s" % (lsvg_cmd))
    rc, activevg, err = module.run_command("%s -o" % (lsvg_cmd))
    for line in allvg.splitlines():
        _lsvg.append(line)
    for line in activevg.splitlines():
        _active_vg.append(line)
    _inactive_vg = list(set(_lsvg) - set(_active_vg))
    result = { 'stdout':_inactive_vg, 'stderr':err, 'rc':rc, 'changed':True }
    module.exit_json(**result)
    
def main():
    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=dict(
            vgname=dict(type='str', required=False),
            state=dict(type='str'),
        ),
        supports_check_mode=True,
    )
    if module.check_mode:
        module.exit_json(**result)

    vgname = module.params['vgname']    
    
    if vgname == 'all' and state == 'all':
        _list_vg(module)
    elif vgname == 'all' and state == 'active':
        _list_active_vg(module)
    elif vgname == 'all' and state == 'inactive':
        _list_inactive_vg(module)
    elif _get_vg_status(module, vgname):
        _get_vg_info(module, vgname)
    else:
        module.fail_json(msg = "Not valid input. Refer Documentation & Examples.")

if __name__ == '__main__':
    main()
