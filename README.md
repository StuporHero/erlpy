# erlpy

Make Python Erlang.

Python's asyncio is difficult to work with because it forces the writer to make everything
async. Erlang's concurrency model has the potential to be much less intrusive thanks to its
relatively simple conceptual model. This model is leveraged in Erlang's standard library,
OTP, to give us `gen_server` which allows writers of Erlang to focus on the functionality
of the system they are building while getting a full suite of advanced functionality
(including concurrency, fault tolerance, and even hot code reload!) essentially for free. This
library is an attempt to import Erlang's concurrency model into Python to enable Python
developers to focus on the problems they are solving instead of solving problems that have
been solved for decades.

## Core Concepts

Erlang is built almost entirely on only three primitive concepts. These are the Process, the
Signal, and the Mailbox. A Process in Erlang is essentially a Green Thread that behaves very
similarly in practice to an Object in OOP in that it encapsulates state behind a well-defined
interface. Processes interact with each other by passing asynchronous Signals. Signals are
either handled behind the scenes in the case of a `kill` signal or are queued in a Mailbox
in the case of a Message Signal. Processes can also be linked or monitored which faciliteates
the creation of Process trees for the propogation of non-Message Signals primarily for error
handling.

Erlang also has the concept of a Node which is essentially an active runtime. Nodes are able
to communicate with each other over a published protocol to facilitate distributed computing
scenarios.

## Atom Type

Erlang makes liberal use of a type known as an Atom. This type is essentially a global constant
symbol that is instantiated the first time it is referenced. Under the hood, the symbol maps to
a platform-native integer (typically 32 or 64 bits). This integer is chosen by the runtime and
persists only until the runtime exits. Because of this, Atoms need to be translated when being
used between Nodes. This translation is done according to the
[External Term Format](https://www.erlang.org/doc/apps/erts/erl_ext_dist.html).

## Prototypes

Before implementing a library that can be packaged and published to pip, several prototypes
will be made to learn about the various options available for implementing core concepts.

### asyncio Prototype

Found in the [proto1](/proto1/) module and demonstrated in
[proto1_scratch.py](/proto1_scratch.py), this prototype focused on leveraging Python's asyncio
to produce viable Green Threads for Erlang-style Processes. This included exploring the
implications of asyncio on propogating asynchronous signals which was required to fully
exercise the Green Thread behavior of non-blocking execution. This implementation proved to be
effective for code that was written with cooperative scheduling in mind, however, it is likely
to be unsuitable for legacy code which would have to be retrofitted with cooperative calls to
play nice. A future prototype will need to explore using threading which I've been led to
believe would be eligible for preemption. A full exploration of the idea will be documented
for that prototype.
