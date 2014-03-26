# dorap - The Docker-Rackspace Plugin

### About

Dorap is a Python implementation of a [Docker API Extension](doc/docker_api_extensions.md)
utilizing [Pyrox](http://github.com/zinic/pyrox) as the programmable HTTP
intermediate. The [Dockerfile](Dockerfile) contained within this repository
enumerates all of the steps required to create a Docker container with the
extension code as a runnable target - thereby creating a Docker plugin.

Dorap is copyright [Rackspace, US Inc.](http://www.rackspace.com/) and is
released to you under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).
See [LICENSE](LICENSE) for more information


### Documentation

Below are documents that have been linked to throughout this README.

* [Docker API Extension Proposal](doc/docker_api_extensions.md)
* [Docker API Extension Spec](doc/docker_extension_enumeration.md)
* [Docker Plugin CLI Spec](doc/docker_plugin_cli_contract.md)


### Usage

Dorap follows the [Docker Plugin CLI Expectations](doc/docker_plugin_cli_contract.md)
and offers a few additional command line parameters that may be investigated
by calling dorap using **-h** or **--help**.


#### Running

With the Docker HTTP API daemon listening on **tcp://0.0.0.0:9000**, the following commands
may be then executed.

```bash
# Pull the latest image down
docker -H tcp://localhost:9000 pull zinic/rax_plugin

# Start the plugin using the address for ethernet interface: docker0
DOCKER_IFACE_IP=$(ip addr | awk '/inet/ && /docker0/{sub(/\/.*$/,"",$2); print $2}')
docker -H tcp://localhost:9000 run zinic/rax_plugin -u http://$DOCKER_IFACE_IP:9000 start
```

Locate the new container's IP address.

```bash
# Get the ID of the newly created plugin container
CONTAINER_ID=$(docker -H tcp://localhost:9000 ps | grep zinic/rax_plugin | awk '{print $1}')

# Grab the IPv4 address for it
DOCKER_IP=$(docker -H tcp://localhost:9000 inspect $CONTAINER_ID | grep IPAddress | cut -d '"' -f 4)
```

Now run Docker against the new plugin and cross your fingers!

```bash
docker -H tcp://$DOCKER_IP:8080 ps
```


### Development

Pull requests are always welcome! Development of this plugin is sponsored by Rackspace. Feel free to [contact us](mailto:containers@rackspace.com)!

<img src="http://c15162226.r26.cf2.rackcdn.com/Rackspace_Cloud_Company_Logo_clr_300x109.jpg" alt="rackspace-logo" />
