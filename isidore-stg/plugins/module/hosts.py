#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
from datetime import datetime

__metaclass__ = type

DOCUMENTATION = r'''
---
module: isidore_host
short_description: Manage hosts in the Isidore system
version_added: "1.0"  # Replace X.Y with the version of Ansible you're adding this to
description:
  - This module allows users to add, modify, or remove hosts in the Isidore system.
options:
  name:
    description:
      - The name of the host.
    required: true
    type: str
  description:
    description:
      - A description for the host.
    required: false
    type: str
  state:
    description:
      - Determines whether to add (present) or delete (absent) a host.
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
        description=dict(type='str', required=False, default=None),
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        commission=dict(type='bool', default=False)
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    isidore = Isidore.fromConfigFile()
    host = isidore.getHost(module.params['name'])

    if module.params['state'] == 'present':
        if not host:
            if not module.check_mode:
                isidore.createHost(module.params['name'])
            host = isidore.getHost(module.params['name'])
            result['changed'] = True
            result['message'] = 'Host was created successfully.'
        else:
            result['message'] = 'Host already exists.'

        if module.params['commission']:
            if not host.getCommissionDate():  # Check if the host is not already commissioned
                if not module.check_mode:
                    host.setCommissionDate(datetime.now())
                result['changed'] = True
                result['message'] += f' Host was commissioned on {datetime.now().strftime("%Y-%m-%d")}.'
            else:
                existing_commission_date = host.getCommissionDate().strftime('%Y-%m-%d')
                result['message'] += f' Host was already commissioned on {existing_commission_date}.'

        if module.params['description']:
            if host is None:
                module.fail_json(msg="Host not found in Isidore.")
            else:
                current_description = host.getDescription()
                if current_description != module.params['description']:
                    if not module.check_mode:
                        host.setDescription(module.params['description'])
                    result['changed'] = True
                    result['message'] = 'Description was updated'

    elif module.params['state'] == 'absent':
        host = isidore.getHost(module.params['name'])
        if host:
            # Remove all associated tags before deleting the host
            for tag in host.getTags():
                tag.delete()

            if not module.check_mode:
                host.delete()
            result['changed'] = True
            result['message'] = 'Host was deleted.'
        else:
            result['changed'] = False
            result['message'] = 'Host does not exist.'
        # if host:
        #     if not module.check_mode:
        #         host.delete()
        #     result['changed'] = True
        #     result['message'] = 'Host was deleted.'
        # else:
        #     result['changed'] = False
        #     result['message'] = 'Host does not exist.'


    module.exit_json(**result)


if __name__ == '__main__':
    run_module()
