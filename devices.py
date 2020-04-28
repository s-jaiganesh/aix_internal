#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'none'
}

from ansible.module_utils.basic import AnsibleModule

def _list_devices(module, device):

    lsdev_cmd = module.get_bin_path('lsdev', True)
    rc, out, err = module.run_command("%s '-C'" % (lsdev_cmd)
    
    if rc != 0:
        changed = False
        module.fail_json(msg="Failing to execute '%s' command." % lsdev_cmd)
    else:
        hdisks = []
        output = []
        for line in out.splitlines():
            if 'device' in line:
                fields = line.strip().split()
                out = line
                hdisks.append(fields[0])
                output.append(line)
        result = dict(
            output=output,
            rc=rc,
            changed=True,
        )
        module.exit_json(**result)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )
    if module.param['name'] == 'disk':
        _list_devices(module, 'hdisk')
    elif module.param['name'] == 'fcs':
        _list_devices(module, 'fcs')
    elif module.param['name'] == 'ent':
        _list_devices(module, 'ent')
    elif module.param['name'] == 'port':
        _list_devices(module, 'EtherChannel')
    else
        module.fail_json(msg="Invalid input")
        
if __name__ == '__main__':
    main()
