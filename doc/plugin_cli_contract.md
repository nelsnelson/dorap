# Docker Plugin CLI Expectations
**Revision Version: 1.0**
**©2013-2014 Rackspace, US Inc.**

### Purpose

Docker plugins may accept command line arguments to simplify their
interactions.


### Call Expectations

Plugins should expect to be called by Docker as the entrypoint to a
container. Docker will pass all user aguments to the entrypoint for
consumption. Plugins may specify their own arguments so long as the user
is aware of them.


### Expected Arguments

Docker will require that all plugins answer to a set
of basic command line arguments, They are as follows

#### Help
Flags: **-h, --help**
Argument: `None`

The help function should return enough documentation about the plugin such
that a user with understanding of the plugin's purpose can configure and
run it.


#### Version
Flags: **-v, --version**
Argument: `None`

The version function should return the plugin's version information.


#### Docker URI
Flags: **-u, --docker-uri**
Argument: `[http|https]://<docker_host>:<port>`

The HTTP/HTTPS URI for the Docker host the plugin is being installed for.
This URI must represent a valid Docker HTTP endpoint.
