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
module: emgr
short_description: Collect precheck before patching
description:
- This module creates boot image on disks
version_added: '1.0'
options:
  name:
    description:
    - name of action example
    type: str
    default: yes
'''

EXAMPLES = r'''
- name: emgr remove preview
  emgr:
    label: all
    state: absent    
    preview: yes
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule

def _remove_all_efix_pkg_preview(module):      

    result = dict()    
    _to_remove, _failed, _success, _err, _out = ([] for i in range(5))
    emgr_cmd = module.get_bin_path('emgr', True)
    rc, lables, err = module.run_command("%s -l" % (emgr_cmd))
    for i in lables.splitlines():
        if i == "There is no efix data on this system":
            changed = False
            module.exit_json(msg="There is no efix data on this system")
        else:
            res = 'True'

    if res is True:        
        lines = lables.split('\n',2)[-1]
        for line in lines.splitlines():                   
             _to_remove.append(fields[2])
             
        result = { 'lables_to_remove' : _to_remove}
        _to_remove_count = len(_to_remove)
        if len(_to_remove) > 0:        
            for lable in _to_remove:
                rc, out, err = module.run_command("%s -p -r %s" % (emgr_cmd, lable))
                if rc is 0:
                     out = out.rstrip(b"\r\n")
                     _success.append(lable)
                     _out.append(out)
                if rc != 0:
                    err = err.rstrip(b"\r\n")
                    _failed.append(lable)
                    _err.append(err)
                     
            if len(_success) > 0:
                result = { 'changed' : 'True'}
                      
            result = { 'lables_failed' : _failed}
            result = { 'lables_success' : _success}
            result = { 'stdout' : _out}
            result = { 'stderr' : _err}

            if len(_failed) != 0:
                if _to_remove_count == len(_failed):
                    result = { 'changed' : 'False'}
                    result = { 'msg' : 'PREVIEW none of the EFIX are affected'}
                    module.fail_json(**result)
                else:
                    result = { 'msg' : 'PREVIEW failed to affect one or more EFIX'}
                    module.exit_json(**result)
            elif len(_failed) is 0:
                result = { 'msg' : 'PREVIEW success for all EFIX'}
                module.exit_json(**result)            
            else:
                module.exit_json(msg="Empty arrary")
          
  
def main():
    module = AnsibleModule(
        argument_spec=dict(
            label=dict(type='str', required=True),
            state=dict(type='str',default=False),
            preview=dict(type='bool',default=False),

        ),
        supports_check_mode=True,
    )
    if module.params['label'] == 'all':        
        if module.params['state'] == 'absent':
            if module.params['preview'] is True:
                _remove_all_efix_pkg_preview(module)                
            else:
                module.fail_json(msg="Preview: option not available")
        else:
            module.fail_json(msg="state option can be present or absent only")
    else:
        module.fail_json(msg="not a valid option")
        
if __name__ == '__main__':
    main()
