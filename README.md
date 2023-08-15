### Isidore Host and Tag Ansible Module

This Ansible modules in this repo (isidore_host and isidore_tag) , allows users to manage hosts and tages in the Isidore system.
#### Features

    Add a new host to Isidore.
    Set attributes for the host, such as description.
    Support for Ansible's check mode.

#### Requirements

    Ansible
    isidore.libIsidore Python library

#### Installation

    Save the module code to a file named isidore_host.py in your custom Ansible modules directory.
    Update the ANSIBLE_LIBRARY environment variable or ansible.cfg to include the path to your custom modules directory.

#### Usage

Here's a basic example of how to use the isidore_host module in an Ansible playbook:

```---
- hosts: localhost
  tasks:
    - name: Add host to Isidore
      isidore_host:
        name: "example.com"
        description: "This is a new host"
        state: present
        
    - name: Add a tag named "TestTag"
      isidore_tag:
        name: "TestTag"
        state: present
      register: tag_result
    
    - name: Commission the host
      isidore_host:
        name: "example.com"
        commission: true
      register: commission_result
      
    - name: Decommission the host
      isidore_host:
        name: "example.com"
        decommission: true
      register: decommission_result
      
    - name: Delete the tag named "TestTag"
      isidore_tag:
        name: "TestTag"
        state: absent
      register: delete_tag_result  
    
    - name: Remove host from Isidore
      isidore_host:
        name: "example.com"
        description: "This is a new host"
        state: absent
     
````



#### Parameters for Host Module

    name: The name of the host. (Required)
    description: A description for the host. (Optional)
    state: Determines whether to add (present) or delete (absent) a host. Default is present.
    decommission: Adds the host to the decommission list (Optional). Default is False.
    commission: Adds the host to the commission list (Optional) Default is False.

#### Parameters for Tag Module

    name: The name of the tag. (Required)
    state: Determines whether to add (present) or delete (absent) a tag. Default is present.
    