#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'patching team'
}
import json
from ansible.module_utils.basic import AnsibleModule, load_platform_subclass

def main():
    result = dict(
        changed=False,
        stdout='',
        stderr='',
        rc='',
    )

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),

        ),
        supports_check_mode=True,
    )
    if module.check_mode:
        module.exit_json(**result)

    df_cmd = module.get_bin_path('df', True)
    if module.params['name'] == 'list':
        rc, out, err = module.run_command("%s -k" % (df_cmd))
        if rc == 0:
            out = out.rstrip(b"\r\n")
            err = err.rstrip(b"\r\n")

            result = dict(
                stdout=out,
                stderr=err,
                rc=rc,
                changed=True,
            )

            module.exit_json(**result)

        if rc != 0:
            module.fail_json(msg="Failing to run %s command." % df_cmd)

    else:
            module.exit_json(msg = "Invalid input. Error!")

    if module.params['name'] is None:
        module.exit_json(msg = "Input is blank. Error!")

if __name__ == '__main__':
    main()
