#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: greeting_module

short_description: This is my first ansible module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my first ansible module.

options:
    name:
        description: Name
        required: false
        type: str

# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Ram Gopinathan (@rprakashg)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  rprakashg.hello_ansible.greeting_module:
    name: Ram

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
greeting:
    description: Greeting.
    type: str
    returned: always
    sample: 'Hello Ram'
'''

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.rprakashg.hello_ansible.plugins.module_utils.commandrunner import CommandRunner # noqa E402
from ansible_collections.rprakashg.hello_ansible.plugins.module_utils.commandresult import CommandResult # noqa E402

def run_module(module, runner):
    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        msg="",
        ansible_version=""
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    if module.params['name'] is None:
        result['msg'] = "Hello"
    else:        
        result['msg'] = "Hello %s" % (module.params['name'])
        result['changed'] = True

    args = [
        "--version",
    ]
    cr: CommandResult = runner.run("", "cluster", args)
    if cr.exit_code == 0:
        result["ansible_version"] = result.output
    else:
        result["msg"] = cr.error
        module.fail_json(result)


    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=False)
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    binary = "ansible"
    runner: CommandRunner = CommandRunner(binary)

    run_module(module, runner)

if __name__ == '__main__':
    main()
