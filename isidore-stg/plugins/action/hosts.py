#!/usr/bin/python

from isidore.libIsidore import *


def run_module(module):
    isidore = Isidore.fromConfigFile()
    host = isidore.getHost(module.params['name'])
    result = dict(changed=False)

    if module.params['state'] == 'present':
        if not host:
            if not module.check_mode:
                isidore.createHost(module.params['name'])
            host = isidore.getHost(module.params['name'])
            result['changed'] = True
            result['message'] = 'Host was created successfully.'
        else:
            result['message'] = 'Host already exists.'

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
            if not module.check_mode:
                host.delete()
            result['changed'] = True
            result['message'] = 'Host was deleted.'
        else:
            result['changed'] = False
            result['message'] = 'Host does not exist.'

    return result
