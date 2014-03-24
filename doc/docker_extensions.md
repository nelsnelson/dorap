# Docker Extension Specification Proposal
­
**Revision Version: 1.0**
<br />
**©2013-2014 Rackspace, US Inc.**


### Brief

This document lays out initial assumptions and goals accompanied by a basic implementation outline for Docker extensions. The proposal is designed to incite discussion and therefore provides few technical implementation details.


#### Assumptions

* Building pluggable modules in Go is difficult. Alternatives are ideal.
* Must be vendor neutral and flexible enough to support multiple vendors.
* Must support multiple extensions per installation.
* Extensions are best served as containers such that any Docker installation aware of the Docker index may then download, deploy and utilize them.


#### Goals

* Should be language neutral if at all possible to better promote community participation and contribution.
* Should allow for future enhancements to the extension specification. The ability to version the extension specification must be supported.
* Should allow for flexible scalability of the system to account for deployments both small and large.


### The Contract

Docker has a strong HTTP contract for it's API at current. Every call presents a well defined operation, making them strong candidates for providing integration points for integration, orchestration and enhancement. Therefore, 
instead of relying on the Docker code base to provide a lower-level API (such as interface or class oriented code extensions) for extensibility, the Docker HTTP API instead should become the provider for this functionality.

This requires certain enhancements to both the Docker client and the Docker HTTP API, detailed below.


#### Docker Extension Intermediate

Using the Docker HTTP API as the basis for all extension integration is trivial if the extensions are deployed as HTTP intermediates or proxies. These intermediates may exist either on the client as locally deployed containers or 
on the server as deployed containers. This allows for extensions to be network agnostic in an endeavor to maintain flexibility of deployment. In addition, this also allows for fully local stacks of extensions to be deployed in an 
effort to maintain low latency from client request to response.

The intermediates must reply to all calls found within the Docker HTTP API with the default action being to simply forward the request without action. This allows intermediates to be stacked easily without incurring additional work 
from the extension implementer.

Use of an intermediate allows an extension developer to implement many useful enterprise integration patterns [1] without ever having to understand the Docker code base.


#### Extension Discovery and the Extension API

The extension API should be an optional add-on to the standard Docker HTTP API. The extension API should include only an extremely limited set of calls to enable a Docker endpoint to describe the extensions available. The extension 
itself may describe additional HTTP API operations for additional integration efforts, but these should be considered private operations and will not be available through the Docker client.


#### Enumerating Extensions

In order to make use of deployed extensions, first a method of discovery is required. This may be accomplished by a simple GET request on the Docker client's part.

This GET request must be identified within the canonical Docker API as a support operation. The request may then be routed down a potential stack of Docker extensions such that upon return the HTTP response contains a data 
structure describing the extensions, their available operations and links to potential documentation.

The client may then consume this structure to generate a parser for extension related command line arguments. The parser will provide translation from command line argument to relevant HTTP structures such that when the interested 
extension intercepts the call it has all of the information needed to perform the requested work.


### Appendix

1. http://www.enterpriseintegrationpatterns.com/toc.html
