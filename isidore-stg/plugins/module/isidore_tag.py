#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: addtag
short_description: Manage tags in the Isidore system
version_added: "1.0"
description:
  - This module allows users to add or remove tags in the Isidore system.
options:
  name:
    description:
      - The name of the tag.
    required: true
    type: str
  state:
    description:
      - Determines whether to add (present) or delete (absent) a tag.
    default: present
    choices:
      - present
      - absent
    type: str
author:
  - Minor Keith
'''

from ansible.module_utils.basic import AnsibleModule
from isidore.libIsidore import *


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present')
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    print("Debug: Initializing Isidore from config file.")
    isidore = Isidore.fromConfigFile()
    print(f"Debug: Fetching tag with name: {module.params['name']}")
    tag = isidore.getTag(module.params['name'])

    if module.params['state'] == 'present':
        print("Debug: Desired state is 'present'")
        if not tag:
            print("Debug: Tag not found. Creating tag.")
            if not module.check_mode:
                isidore.createTag(module.params['name'])
            result['changed'] = True
            result['message'] = 'Tag was successfully added.'
        else:
            result['message'] = 'Tag already exists.'

    elif module.params['state'] == 'absent':
        if tag:
            if not module.check_mode:
                tag.delete()
            result['changed'] = True
            result['message'] = 'Tag was successfully removed.'
        else:
            result['message'] = 'Tag does not exist.'

    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
