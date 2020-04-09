
## Why gRPC over REST?

This project uses gRPC for communication between sensors and the server primarily for performance reasons. In the grand infinity of time, and considering the small payload size, the performance overhead is likely negligible. That being said, there is a legitimate need to consider performance given that each sensor's network connection is stochastic and likely entirely unreliable. Given that the burden of implementing a REST interface and gRPC interface are about the same in this context, gRPC makes more sense.

## Why SQLite?

[There are plenty of good reasons to choose SQLite.](https://www.sqlite.org/whentouse.html) For context, this project's design objectives imply that:
* Data from bus sensors will be more frequently sent to the server than requested by a client.
* Low - if any - scalability requirements. (At peak, the server might receive data from ten buses a minute. Benchmark data suggests that SQLite can support significantly larger loads.)

SQLite is a lightweight option that best serves both of those criteria, in addition to being simple to implement and requiring minimal administration.

## Why software as a product over software as a service?

Simplicity for the purposes of designing a minimum viable product as quickly as possible. Pivoting this project to the SaaS model is theoretically trivial, but would require implementation of other features such as user login and authentication that are not listed in the project's design objectives.

## Why Docker?

If this project is being constructed as a product and not a service, and it is being constructed for a university client (e.g., UCSC TAPS) then were it self hosted it might be hosted using [UCSC ITS Virtual Server Hosting](https://its.ucsc.edu/data-center/virtual-server-hosting.html). Using Docker would, in theory, make it easier to deploy this project using that service, and has the added benefit of reducing vendor lock-in.

This project is small enough that it would likely be much cheaper to implement as a set of Lambdas, etc. but there is a realistic chance that self-hosting on such platforms could be prohibitive for a university client.
