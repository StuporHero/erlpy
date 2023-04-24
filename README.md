# erl-async

Python's asyncio is difficult to work with because it is built on concepts that are not intuitive.
Erlang's concurrency model is built on much more intuitive concepts. This library is an attempt to
import Erlang's concurrency model into Python to enable Python developers to write concurrent code
in a much friendlier conceptual model while still having access to all things Python.

## Core Concepts

Erlang is built almost entirely on only three primitive concepts. These are the Process, the
Message, and the Mailbox. A Process in Erlang is essentially a Green Thread that behaves very
similarly in practice to an Object in OOP in that it encapsulates state behind a well-defined
interface. Processes interact with each other by passing asynchronous Messages. Messages are
queued in a Mailbox rather than dispatched like methods.
