remosh [![Build Status](https://travis-ci.org/thusoy/remosh.svg?branch=master)](https://travis-ci.org/thusoy/remosh)
=======

Remote execution engine with less than 100 lines of code.

For CI integration with f. ex GitHub Webhooks, run a given command on some server on every push.

Just make a file in the following format:

    <id>: <command>

And do a POST with the given id to run the command, eg with the file:

    secretpassword: sudo /bin/update-server

The following request will trigger the `update-server` script:

    POST localhost?id=secretpassword

Granted that the user running remosh has the privileges to do so, naturally.


Installation
------------

From PyPI:

    $ pip install remosh

Start the service:

    $ remosh <file-to-read-commands-from>

You might want to put that into an Upstart job or similar.


Tips
----

You might want remosh to run commands as sudo, but giving the user running the service free access to any sudo command is not a good idea. There's no known security issues with remosh, but play it on the safe side. Create an unprivileged user remosh, create an upstart job ala this:

    # Put this in /etc/init/remosh.conf
    description "Remosh job config"

    start on startup
    stop on runlevel [016]

    setgid remosh
    setuid remosh

    respawn

    exec remosh /etc/remosh_commands -l /var/log/remosh.log

And then create a sudoers file for remosh, ala this:

    # Put this in /etc/sudoers.d/remosh
    Cmnd_Alias      COMMANDS = /bin/update-server, /usr/bin/apt-get update, <..>

    # User alias specification
    remosh ALL = NOPASSWD: COMMANDS

Now the remosh user can execute the listed commands with password-less sudo.
