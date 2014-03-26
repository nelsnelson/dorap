# Enumerating Docker Extensions via the Docker HTTP API
**Revision Version: 1.0**
**©2013-2014 Rackspace, US Inc.**

### Purpose

More complex installations of Docker plugins may require the Docker client
to expose features of certain plugins, thereby extending the list of
available Docker commands seamlessly. This document outlines a system for
accomplishing this communication in a lightweight and non-disruptive
manner to the currently existing Docker API.


### API Extensions

Docker extension intermediates may choose to completely reply to a request
of their own accord. This allows for transparent extension of the Docker
HTTP API callset without having to modify the origin server. This then,
allows a Docker extension to host additional functionality that goes beyond
the scope of the original API.


### Enumerating Plugins

In order to enumerate the plugins installed in a given Docker stack, a
**HEAD** request is sent to **/version**. This request should travel down
the stack. Upon its return, every intermediate is required to enhance a
HTTP header in the response named **Docker-Plugins** by adding a HTTP URI that
resolves someplace within the stack. This URI is called the **plugin
descriptor** and can be queried for additional information about the
plugin such as presentation, arguments, and short documentation.

Example Request
```
HEAD /version HTTP/1.1
Host: localhost
User-Agent: docker-cli_0.9.1
Accept: application/json

```

Example Response
```
HTTP/1.1 200 OK
Content-Length: 0
Docker-Plugins: http://localhost:9000/_auth, http://localhost:9000/_rax
Docker-Version: 0.0.9

```


### Plugin Description JSON

```json
{
    "name": "docker_auth_plugin",
    "cmd": "auth",
    "path": "/_auth",

    "routes": {
        "/setup": {
            "subcmd": "setup",
            "arguments": [
                {
                    "flags": [
                        "-u",
                        "--user"
                    ],

                    "nargs": 1,
                    "store_as": "user"
                },
                {
                    "flags": [
                        "-p",
                        "--password"
                    ],

                    "nargs": 1,
                    "store_as": "password"
                }
            ]
        }
    }
}
```
