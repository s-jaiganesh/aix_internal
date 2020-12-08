#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

EXAMPLES = r'''
- name: FS increase command in MB
  ibm_chfs:
    size: 512
    fs_name: /var
    action: increase

- name: FS decrease command in MB
  ibm_chfs:
    size: 512
    fs_name: /var
    action: decrease       
'''

def _chfs(module, fs_size, fs_name, action):
    chfs_cmd = module.get_bin_path('chfs', True)
    if 'increase' in action:
        rc, chfs_out, err = module.run_command("%s -a size=+%sM %s" % (chfs_cmd, fs_size, fs_name))
    elif 'decrease' in action:
        rc, chfs_out, err = module.run_command("%s -a size=-%sM %s" % (chfs_cmd, fs_size, fs_name))
    else
        module.fail_json(msg='Unknown option. Please choose increase/decrease')

    if rc == 0:
        result = { 'stdout' : chfs_out, 'rc' : rc, 'stderr': err, 'changed' : True, 'msg' : 'the chfs command completed successfully' }
 
        module.exit_json(**result)
    else:
        result = { 'stdout' : chfs_out, 'rc' : rc, 'stderr': '', 'changed' : False, 'msg' : 'the chfs command not completed successfully' }

        module.fail_json(**result)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            size=dict(type='int', required=True),
            fs_name=dict(type='str', required=True),
            action=dict(type='str', required=True),

        ),
        supports_check_mode=True,
    )
    fs_size = module.params['size']
    fs_name = module.params['fs_name']
    action = module.params['action']

    _chfs(module, fs_size, fs_name, action)

if __name__ == '__main__':
    main()
