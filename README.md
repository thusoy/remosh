remoted [![Build Status](https://travis-ci.org/thusoy/remoted.svg)](https://travis-ci.org/thusoy/remoted)
=======

Remote execution engine with less than 100 lines of code.

For CI integration with f. ex GitHub Webhooks, run a given command on some server on every push.

Just make a file in the following format:

    <id>: <command>

And do a POST with the given id to run the command, eg with the file:

    secretpassword: sudo /bin/update-server

The following request will trigger the `update-server` script:

    POST localhost?id=secretpassword

Granted that the user running remoted has the privileges to do so, naturally.


Installation
------------

From PyPI:

    $ pip install remoted

Start the service:

    $ remoted <file-to-read-commands-from>

You might want to put that into an Upstart job or similar.


Tips
----

You might want remoted to run commands as sudo, but giving the user running the service free access to any sudo command is not a good idea. There's no known security issues with remoted, but play it on the safe side. Create an unprivileged user remoted, create an upstart job ala this:

    # Put this in /etc/init/remoted.conf
    description "Remoted job config"

    start on startup
    stop on runlevel [016]

    setgid remoted
    setuid remoted

    respawn

    exec remoted /etc/remoted_commands -l /var/log/remoted.log

And then create a sudoers file for remoted, ala this:

    # Put this in /etc/sudoers.d/remoted
    Cmnd_Alias      COMMANDS = /bin/update-server, /usr/bin/apt-get update, <..>

    # User alias specification
    remoted ALL = NOPASSWD: COMMANDS

Now the remoted user can execute the listed commands with password-less sudo.
