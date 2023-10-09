from ansible.plugins.action import ActionBase
from isidore.libIsidore import *
from datetime import datetime


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        # Access arguments
        name = self._task.args.get('name')
        description = self._task.args.get('description', None)
        state = self._task.args.get('state', 'present')
        commission = self._task.args.get('commission', False)
        decommission = self._task.args.get('decommission', False)

        result = dict(
            changed=False,
            message=''
        )

        try:
            isidore = Isidore.fromConfigFile()
            host = isidore.getHost(name)

            if state == 'present':
                if not host:
                    isidore.createHost(name)
                    host = isidore.getHost(name)
                    result['changed'] = True
                    result['message'] = 'Host was created successfully.'
                else:
                    result['message'] = 'Host already exists.'

                if commission:
                    if not host.getCommissionDate():
                        host.setCommissionDate(datetime.now())
                        result['changed'] = True
                        result['message'] += f' Host was commissioned on {datetime.now().strftime("%Y-%m-%d")}.'
                    else:
                        existing_commission_date = host.getCommissionDate().strftime('%Y-%m-%d')
                        result['message'] += f' Host was already commissioned on {existing_commission_date}.'

                if description:
                    if host is None:
                        result['changed'] = False
                        result['message'] = "Host not found in Isidore."
                    else:
                        current_description = host.getDescription()
                        if current_description != description:
                            host.setDescription(description)
                            result['changed'] = True
                            result['message'] = 'Description was updated'

            elif state == 'decommissioned':
                if host:
                    # Check if host is already decommissioned
                    if not host.isDecommissioned():  # Replace with actual check
                        # Decommission the host
                        host.decommission()  # Replace with actual method to decommission
                        result['changed'] = True
                        result['message'] = f'Host {name} was successfully decommissioned.'
                    else:
                        result['message'] = f'Host {name} is already decommissioned.'
                else:
                    result['message'] = f'Host {name} does not exist.'

            elif state == 'absent':
                if host:
                    try:
                        tags = host.getTags()
                        if tags:
                            for tag in tags:
                                result['message'] += f"Tag {tag.getName()} has to be removed. "
                        host.delete()
                        result['changed'] = True
                        result['message'] += f"Host {name} has been deleted."
                    except Exception as e:
                        result['changed'] = False
                        result['message'] = f"Failed to delete host {name}. Error: {str(e)}"
                else:
                    result['changed'] = False
                    result['message'] = f"Host {name} does not exist."

        except Exception as e:
            result['failed'] = True
            result['message'] = f"An error occurred: {str(e)}"

        return result
