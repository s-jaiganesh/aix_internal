#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
import re
import subprocess
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
    
- name: Install xorgs ifix IJ11544s0a.181127.epkg.Z
  emgr:
    package: /mnt/IJ11544s0a.181127.epkg.Z
    state: present
- name: Remove ifix with label IJ11544s0a
  emgr:
    label: IJ11544s0a
    state: absent    
'''

RETURN = r''' # '''

from ansible.module_utils.basic import AnsibleModule

def _get_ifix_label(package):
    # gets ifix label from the ifix package file (.Z)
    command = ["emgr"]
    command.extend(["-d",  "-e", package])
    result = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    output = result.communicate()[0]
    labels = re.findall("LABEL:\s+(\w+)",output)
    returncode = result.returncode
    if returncode is 0 and len(labels) > 0:
        return labels[0]
    else:
        return None

def _ifix_installed(label):
    # checks if an ifix with given label is installed on the system
    command = ["emgr"]
    command.extend(["-c", "-L", label])
    result = subprocess.Popen(command)
    output = result.communicate()[0]
    returncode = result.returncode
    if returncode is 0:
        return True
    else:
        return False

def _install_ifix_pkg(package):
    # installs ifix given package file
    command = ["emgr"]
    command.extend(["-e", package])
    result = subprocess.Popen(command)
    output = result.communicate()[0]
    returncode = result.returncode
    if returncode is 0:
        return True
    else:
        return False

def _remove_ifix_pkg(label):
    command = ["emgr"]
    command.extend(["-r", "-L", label])
    result = subprocess.Popen(command)
    output = result.communicate()[0]
    returncode = result.returncode
    if returncode is 0:
        return True
    else:
        return False

def _remove_all_efix_pkg_preview(module, preview):      

    result = dict()
    res = ''
    _to_remove, _failed, _success, _err, _out = ([] for i in range(5))
    emgr_cmd = module.get_bin_path('emgr', True)
    rc, lables, err = module.run_command("%s -l" % (emgr_cmd))
    out = lables.rstrip(b"\r\n")
    for i in lables.splitlines():
        if i == "There is no efix data on this system.":
            res = False            
        else:
            res = True

    if res is True:
        if preview is True:            
            emgr_remove_cmd = ("%s -p -r -L" % (emgr_cmd))
        elif preview is False:            
            emgr_remove_cmd = ("%s -r -L" % (emgr_cmd))
        else:
            module.fail_json(msg="Preview option not avaiable. valid must be True or False")
            
        lines = lables.split('\n',3)[-1]
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
                module.exit_json(msg="Empty array")
    else:
        result = { 'stdout' : _out, 'stdout_lines' : _out, 'rc' : 0, 'stderr': '', 'changed' : False, 'msg' : 'There is no efix data on this system' }
        module.exit_json(**result)
  
def main():
    module = AnsibleModule(
        argument_spec=dict(
            label=dict(type='str', required=False),
            package=dict(type='str', required=False),
            state=dict(type='str',default=False, choices=['present', 'absent']),
            preview=dict(type='bool',default=False),

        ),
        supports_check_mode=True,
    )    
    label = module.params['label']
    package = module.params['package']
    state = module.params['state']
    preview = module.params['preview']
    
    if state == 'present':
        if package is None:
            module.fail_json(msg="package path/filename is required to install ifix")
		
        label = _get_ifix_label(package)

        if label is None:
            module.fail_json(msg = ("Invalid package file or unable to get ifix label from %s" % package))
	
        if _ifix_installed(label):
            changed = False
            msg = ("Ifix already installed: %s" % label)
        else:
            if _install_ifix_pkg(package):
                changed = True
                module.exit_json(msg = ("IFIX package %s has been installed" % package))            
            else:
                module.fail_json(msg = ("Failed to install ifix from %s" % package))

    elif state == 'absent':		

        if label is None:
            module.fail_json(msg = "Ifix label is required to uninstall ifix")
		
        if label == "all":
            _remove_all_efix_pkg_preview(module, preview)        
        elif _ifix_installed(label):
            if not module.check_mode and _remove_ifix_pkg(label):
                changed = True
                module.exit_json(msg = ("IFIX package with label {0} has been removed".format(label)))
            elif module.check_mode:
                changed = True
                module.exit_json(msg = ("IFIX package with label {0} would be removed".format(label)))
            else:
                module.fail_json(msg = ("Failed to uninstall ifix %s" % label))
        else:
            changed = False
            module.exit_json(msg = ("Ifix is not present: %s" % label))
    else:
        changed = False
        msg = "Unexpected state."
        module.fail_json(msg=msg)
        
if __name__ == '__main__':
    main()
