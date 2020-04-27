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

def _list_devices(module):

    a = open("lsdev.txt", "r")
    b = a.read()
    hdisk = []
    output = []
    for line in b.splitlines():
        if 'hdisk' in line:
            fields = line.strip().split()
            out = line
            hdisk.append(fields[0])
            output.append(line)
    result = dict(
        output=output
    )
    
    module.exit_json(**result)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )

    _list_devices(module)

if __name__ == '__main__':
    main()
