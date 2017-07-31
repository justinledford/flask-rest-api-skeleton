# Deploy

Included is an Ansible playbook to automate initial setup
of nginx, gunicorn and mysql.

## Steps
1. Fill in `vars.yml`
    - `project_name` will be used in various config files,
      should be lowercase, underscored, etc.
    - `project_root` is where the project will be on
      the remote server, `/var/www/foobar` is a good
      choice (if foobar is your project name).
2. Update `hosts` with the IP address of the host
   to deploy to.

3. Run the Ansible playbook
```
$ cd deploy
$ ansible-playbook playbook.yml
```

A Vagrantfile is also included to setup a dev environment.
