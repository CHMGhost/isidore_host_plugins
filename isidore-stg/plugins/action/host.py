from ansible.plugins.action import ActionBase
from isidore.libIsidore import Isidore

class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        # Use the existing module
        result = self._execute_module(module_name='host', module_args=self._task.args,
                                      task_vars=task_vars)

        return result
