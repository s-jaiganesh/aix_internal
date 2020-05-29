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
module: emgr
short_description: Remove EFIX
description:
- This module removes EFIX with preview option
version_added: '1.0'
'''

EXAMPLES = r'''
- name: emgr remove preview
  emgr:
    label: all
    state: absent    
    preview: True
    
- name: emgr remove
  emgr:
    label: all
    state: absent    
    preview: False  
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule

def _remove_all_efix_pkg_preview(module, preview):      

    result = dict()
    res = ''
    _to_remove, _failed, _success, _err, _out = ([] for i in range(5))
    emgr_cmd = module.get_bin_path('emgr', True)
    rc, lables, err = module.run_command("%s -l" % (emgr_cmd))
    out = lables.rstrip(b"\r\n")
    for i in lables.splitlines():
        if i == "There is no efix data on this system":
            res = False
            result = { 'stdout' : _out, 'stdout_lines' : _out, 'rc' : 0, 'stderr': '', 'changed' : False, 'msg' : 'There is no efix data on this system' }            
            module.exit_json(**result)
        else:
            res = True

    if res is True:
        if preview is True:            
            emgr_remove_cmd = ("%s -p -r" % (emgr_cmd))
        elif preview is False:            
            emgr_remove_cmd = ("%s -r" % (emgr_cmd))
        else:
            module.fail_json(msg="Preview option not avaiable. valid must be True or False")
            
        lines = lables.split('\n',2)[-1]
        reach=0

        for line in lines.splitlines():
            if reach is 0:
                fields = line.strip().split()
                if len(fields) > 2:
                    _to_remove.append(fields[2])
                elif len(fields) < 2:
                    reach = 1
                else:
                    module.fail_json(msg="unexpected return from %s command" % emgr_cmd)
             
        _to_remove_count = len(_to_remove)
        if len(_to_remove) > 0:        
            for lable in _to_remove:
                rc, out, err = module.run_command("%s %s" % (emgr_remove_cmd, lable))
                if rc is 0:
                     out = out.rstrip(b"\r\n")
                     _success.append(lable)
                     _out.append(out)
                if rc != 0:
                    err = err.rstrip(b"\r\n")
                    _failed.append(lable)
                    _err.append(err)                                             

            if len(_failed) != 0:
                if _to_remove_count == len(_failed):
                    result = { 'lables_to_remove' : _to_remove, 'lables_failed' : _failed, 'lables_success' : _success, 'stdout' : _out, 'stdout_lines' : _out, 'stderr' : _err, 'stderr_lines' : _out, 'changed' : False, 'msg' : 'PREVIEW none of the EFIX are affected' }
                    result.update(result)
                    module.fail_json(**result)
                else:
                    result = { 'lables_to_remove' : _to_remove, 'lables_failed' : _failed, 'lables_success' : _success, 'stdout' : _out, 'stdout_lines' : _out, 'stderr' : _err, 'stderr_lines' : _out, 'changed' : True, 'msg' : 'PREVIEW failed to affect one or more EFIX' }
                    result.update(result)
                    module.fail_json(**result)
            elif len(_failed) is 0:
                result = { 'lables_to_remove' : _to_remove, 'lables_failed' : _failed, 'lables_success' : _success, 'stdout' : _out, 'stdout_lines' : _out, 'stderr' : _err, 'stderr_lines' : _out, 'changed' : True, 'msg' : 'PREVIEW success for all EFIX' }
                result.update(result)
                module.exit_json(**result)            
            else:
                module.exit_json(msg="Empty arrary")
    else:
            module.fail_json(msg="Unhandled error")
  
def main():
    module = AnsibleModule(
        argument_spec=dict(
            label=dict(type='str', required=True),
            state=dict(type='str',default=False),
            preview=dict(type='bool',default=False),

        ),
        supports_check_mode=True,
    )
    preview = module.params['preview'] 
    if module.params['label'] == 'all':        
        if module.params['state'] == 'absent':            
            _remove_all_efix_pkg_preview(module, preview)                            
        else:
            module.fail_json(msg="state option can be present or absent only")
    else:
        module.fail_json(msg="not a valid option")
        
if __name__ == '__main__':
    main()
