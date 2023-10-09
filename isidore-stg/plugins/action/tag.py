from ansible.plugins.action import ActionBase
from isidore.libIsidore import *

class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        # Access arguments
        name = self._task.args.get('name')
        state = self._task.args.get('state', 'present')

        result = dict(
            changed=False,
            message=''
        )

        try:

            isidore = Isidore.fromConfigFile()
            tag = isidore.getTag(name)

            if state == 'present':
                if not tag:
                    isidore.createTag(name)
                    result['changed'] = True
                    result['message'] = 'Tag was successfully added.'
                else:
                    result['message'] = 'Tag already exists.'

            elif state == 'absent':
                if tag:
                    tag.delete()
                    result['changed'] = True
                    result['message'] = 'Tag was successfully removed.'
                else:
                    result['message'] = 'Tag does not exist.'
        except Exception as e:
            result['failed'] = True
            result['message'] = f"An error occurred: {str(e)}"

        return result
