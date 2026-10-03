"""Python causation: binding, aliasing, hashing, concurrency, closures and cleanup."""

WORLD = "python-causation-v0"
PREFIX = "pyc"
DOMAIN = "language-ecosystems"
SUBJECT = "language-ecosystems.python"
SOURCES = ["python-language-314", "python-pep-779", "python-free-threading-314", "python-asyncio-314", "python-copy-314"]
SCOPE = "Python 3 semantics with CPython 3.13/3.14 implementation and build boundaries: binding, copying, hashing, asyncio, closures, descriptors and resource cleanup; no universal thread-safety or finalization guarantee"
ROOT_LABEL = "Python causation world"
ROOT_STATEMENT = "Root of the Python causation world: how binding, object protocols and lifetime mechanisms affect observable Python behavior."

CONCEPTS = [
    ("name-binding", "Name binding to an object", "An association between a name in a namespace and an object; assigning a name need not copy that object.", []),
    ("object-identity", "Object identity", "The identity of an object, tested by is and distinct from its equality relation.", []),
    ("mutable-object", "Mutable object", "An object whose own state can change after creation, such as a list or dictionary.", []),
    ("immutable-object", "Immutable object", "An object whose own structure cannot change; an immutable tuple may still refer to mutable objects.", []),
    ("aliasing", "Aliasing two names", "Two names or access paths referring to the same object.", []),
    ("shallow-copy", "Shallow copy", "A new outer container that retains references to the original container's elements.", []),
    ("deep-copy", "Deep copy", "Recursive copying subject to memoization and type-specific copy behavior; not a promise that every reachable object is duplicated.", []),
    ("is-vs-eq", "Identity versus equality", "The distinction between is testing identity and == invoking equality behavior.", []),
    ("hashability", "Hashability of a type", "Support for instance hashes stable over the object's lifetime and equal hashes for objects comparing equal; built-in container hashability can depend on contents.", []),
    ("dict-key", "Dictionary key lookup", "Lookup by hash followed by identity or equality checks on candidate keys.", []),
    ("gil", "Global interpreter lock", "The lock serializing Python execution within an interpreter in the default CPython build; optional free-threaded 3.13t/3.14t builds can run with it disabled.", ["GIL"]),
    ("thread-parallelism", "Thread parallelism limits", "The inability of CPU-bound Python threads in one GIL-enabled interpreter to execute Python bytecode simultaneously.", []),
    ("event-loop", "Asyncio event loop", "A scheduler executing cooperative tasks and callbacks on its event-loop thread.", []),
    ("await-yield", "Await yielding control", "Suspension of a coroutine at an await that cannot complete immediately; not every await suspends.", []),
    ("generator-lazy", "Generator lazy evaluation", "Execution of a generator body as its iterator is advanced instead of producing all results at creation.", []),
    ("yield-suspension", "Yield suspension point", "A yield expression suspending generator execution while retaining its local state.", []),
    ("iterator-protocol", "Iterator protocol", "The __iter__ and __next__ operations through which an iterator supplies values and signals exhaustion.", []),
    ("comprehension-scope", "Comprehension scope", "Python 3 comprehension iteration targets are local to the comprehension's semantic scope.", []),
    ("late-binding-closure", "Closure late binding", "A closure accesses its captured variable's current binding when executed rather than freezing the value at creation.", []),
    ("default-mutable-arg", "Default mutable argument", "A mutable default object evaluated at function definition and reused by calls omitting that argument.", []),
    ("exception-flow", "Exception control flow", "Propagation of an exception through active calls and handlers.", []),
    ("finally-guarantee", "Finally guarantee", "Execution of an entered try statement's finally suite on Python-level normal or exceptional exit, excluding termination that bypasses Python cleanup.", []),
    ("context-manager", "Context manager with-block", "The with protocol invoking __exit__ on block exit after __enter__ has returned successfully.", []),
    ("refcount-gc", "Reference counting cleanup", "CPython deallocation driven by reference counts; immortal objects, resurrection and free-threaded mechanisms limit promptness claims.", []),
    ("cycle-collector", "Cycle collector", "CPython's collector for unreachable tracked reference cycles, distinct from ordinary reference counting.", []),
    ("duck-typing", "Duck typing", "Use of an object's supported behavior without requiring a particular nominal type.", []),
    ("dunder-methods", "Dunder methods", "Special methods on a type that customize supported Python operations.", []),
    ("property-descriptor", "Property descriptor", "A data descriptor whose accessor methods participate in attribute access even when no setter is supplied.", []),
    ("class-attribute", "Class attribute sharing", "Instances can read a common class attribute when instance lookup does not override it.", []),
    ("instance-attribute", "Instance attribute shadowing", "An instance dictionary entry overriding an ordinary class attribute or non-data descriptor during normal lookup.", []),
    ("mro", "Method resolution order", "The class linearization used to search class and base-class attributes.", ["MRO"]),
    ("import-cache", "Module import cache", "The sys.modules mapping through which imports normally reuse an existing module for a fully qualified name.", []),
    ("type-hints", "Type hints unenforced", "Python annotations do not themselves impose runtime type checks, though external tools or libraries may use them.", []),
    ("shared-mutation", "Shared mutation visibility", "An in-place change observed through another reference to the same mutable object.", []),
    ("loop-variable-leak", "Loop variable leakage", "A loop iteration target becoming bound or overwritten in the enclosing scope.", []),
    ("skipped-cleanup", "Skipped cleanup", "Required resource-release code being bypassed on a control-flow exit.", []),
    ("last-reference-dropped", "Last reference dropped", "Removal of the final strong reference to an object, including references held by containers or frames.", []),
    ("io-concurrency", "Single-thread I/O concurrency", "Overlapping pending I/O operations while callbacks and Python task code execute on one thread.", []),
    ("equality-result", "True equality result", "A successful equality comparison yielding True for the operands.", []),
]

RELATIONS = [
    ("binding-enables-identity", "name-binding", "object-identity", "enables", "Name binding to an object enables Object identity to be tested through two name references.", "Python 3; two bound names are operands of is", ""),
    ("aliasing-causes-shared-state", "aliasing", "shared-mutation", "causes", "Aliasing two names causes Shared mutation visibility when either name is used to mutate their common object.", "Python 3; both names refer to the same list and an in-place append is observed through the other name", ""),
    ("immutability-prevents-alias-bugs", "immutable-object", "shared-mutation", "prevents", "An Immutable object prevents Shared mutation visibility of changes to that object's own immutable value.", "Python 3; the shared value is a built-in str, bytes or number and only that value is considered", "Immutability of a container does not freeze mutable objects stored inside it."),
    ("shallow-copy-limits", "shallow-copy", "aliasing", "inhibits", "Shallow copy inhibits Aliasing two names at the outer-container level while preserving references to nested objects.", "Python 3; list.copy creates the new outer list and the source name still refers to the original", ""),
    ("deep-copy-prevents-sharing", "deep-copy", "shared-mutation", "prevents", "Deep copy prevents Shared mutation visibility between the original and copied mutable container nodes.", "Python 3; copy.deepcopy processes a graph of built-in lists and dictionaries with primitive immutable leaves and no custom copy hooks", "Aliases within the original graph can remain aliases within the copied graph because deepcopy memoizes objects."),
    ("identity-predicts-equality", "object-identity", "equality-result", "predicts", "Shared Object identity predicts a True equality result for an object using object.__eq__.", "Python 3; the type inherits the default identity-based equality and does not replace its comparison behavior", "This inference is not universal: float NaN is unequal to itself, and custom __eq__ can be non-reflexive."),
    ("hashability-prereq-keys", "hashability", "dict-key", "prerequisite", "Hashability of a type is a prerequisite for Dictionary key lookup with an instance of that type.", "Python 3; a built-in dict hashes the supplied key and requires that particular instance to be hashable", ""),
    ("mutability-prevents-hashing", "mutable-object", "hashability", "prevents", "A Mutable object prevents Hashability of a type for the built-in mutable container types that disable hashing.", "Python 3; the object is a built-in list, dict, set or bytearray rather than a custom identity-hashed object", ""),
    ("dictkey-tests-equality", "dict-key", "is-vs-eq", "enables", "Dictionary key lookup enables Identity versus equality to select an existing entry for a matching key.", "Python 3; valid hashable keys have matching hashes and dict checks candidate identity or equality", ""),
    ("gil-limits-threads", "gil", "thread-parallelism", "causes", "The Global interpreter lock causes Thread parallelism limits for simultaneous CPU-bound Python execution.", "CPython 3.13/3.14 default GIL build; CPU-bound threads execute Python bytecode in the same interpreter", "Native extension work that releases the GIL and free-threaded execution with the GIL disabled are outside this restriction."),
    ("await-yields-to-loop", "await-yield", "event-loop", "enables", "Await yielding control enables the Asyncio event loop to run other ready callbacks or tasks.", "Python 3 asyncio; the awaited operation actually suspends the current task and another callback or task is ready", ""),
    ("loop-bypasses-gil", "event-loop", "io-concurrency", "enables", "The Asyncio event loop enables Single-thread I/O concurrency by resuming tasks as nonblocking I/O becomes ready.", "Python 3 asyncio; tasks use nonblocking I/O and yield cooperatively on one loop thread without blocking that thread", "This overlap provides no simultaneous Python execution on that single thread."),
    ("yield-enables-lazy", "yield-suspension", "generator-lazy", "enables", "A Yield suspension point enables Generator lazy evaluation by preserving execution state between requested values.", "Python 3; a synchronous generator is advanced incrementally with next rather than exhausted eagerly", ""),
    ("generator-drives-iterator", "generator-lazy", "iterator-protocol", "enables", "Generator lazy evaluation enables the Iterator protocol to consume generated values incrementally.", "Python 3; calling a synchronous generator function supplies an iterator advanced by a for loop", ""),
    ("comprehension-isolates", "comprehension-scope", "loop-variable-leak", "prevents", "Comprehension scope prevents Loop variable leakage from comprehension iteration targets into the enclosing scope.", "Python 3; a list, set or dict comprehension binds its for-clause target rather than an assignment-expression target", "The closures produced by one comprehension can still share its iteration variable and exhibit late binding."),
    ("closure-late-binding", "late-binding-closure", "name-binding", "predicts", "Closure late binding predicts the Name binding to an object observed when the closure later executes.", "Python 3; a closure reads a captured variable after its enclosing loop has rebound that variable and no default argument freezes a value", ""),
    ("default-mutable-shared", "default-mutable-arg", "shared-mutation", "causes", "A Default mutable argument causes Shared mutation visibility across calls that reuse and mutate it.", "Python 3; successive calls omit a list default parameter and append to the default object instead of rebinding it", ""),
    ("exception-enables-finally", "finally-guarantee", "skipped-cleanup", "prevents", "The Finally guarantee prevents Skipped cleanup when a try suite exits through an exception or normal control transfer.", "Python 3; an entered finally suite contains the cleanup, execution reaches it, and that cleanup completes", "os._exit, fatal process termination and a failure before the cleanup operation can bypass or interrupt cleanup."),
    ("with-enables-cleanup", "context-manager", "skipped-cleanup", "prevents", "A Context manager with-block prevents Skipped cleanup by calling a resource-releasing __exit__ after the body exits.", "Python 3; __enter__ succeeded and the manager's __exit__ releases the acquired resource successfully on normal or exceptional exit", "Abrupt process termination can bypass __exit__; arbitrary context managers need not release resources."),
    ("refcount-ties-to-names", "last-reference-dropped", "refcount-gc", "causes", "Last reference dropped causes Reference counting cleanup for an ordinary mortal CPython object.", "CPython 3.13/3.14 GIL-enabled build; the object's final strong reference disappears, its count reaches zero and no finalizer resurrects it", "Immortal objects and free-threaded deferred or biased reference-counting paths do not provide this promptness guarantee."),
    ("cycle-collector-frees-loops", "cycle-collector", "refcount-gc", "enables", "The Cycle collector enables Reference counting cleanup by clearing unreachable cyclic container references.", "CPython 3.13/3.14 GIL-enabled build; enabled cyclic GC collects tracked unreachable containers with supported clearing and no resurrection", ""),
    ("duck-typing-uses-dunders", "dunder-methods", "duck-typing", "enables", "Implementing Dunder methods enables Duck typing for operations that use the implemented special-method protocol.", "Python 3; a custom type supplies the required special methods for the operation being invoked without a nominal-type check", ""),
    ("dunder-enables-iteration", "dunder-methods", "iterator-protocol", "enables", "Implementing Dunder methods enables the Iterator protocol when __iter__ returns self and __next__ supplies values or raises StopIteration.", "Python 3; both iterator methods are implemented on the custom iterator's type with the specified contracts", ""),
    ("property-intercepts-access", "property-descriptor", "instance-attribute", "prevents", "A Property descriptor prevents Instance attribute shadowing because its data-descriptor lookup takes precedence over the instance dictionary.", "Python 3; normal object.__getattribute__ finds a property of the same name in the class MRO", "A custom __getattribute__ implementation can bypass normal descriptor precedence."),
    ("instance-shadowing-protects", "instance-attribute", "class-attribute", "inhibits", "Instance attribute shadowing inhibits Class attribute sharing for subsequent reads of the shadowed attribute on that instance.", "Python 3; ordinary instance assignment stores an instance-dictionary value and the class attribute is not a data descriptor", ""),
    ("mro-predicts-lookup", "mro", "class-attribute", "predicts", "Method resolution order predicts which Class attribute sharing supplies a value from the class hierarchy.", "Python 3; normal attribute lookup searches multiple bases, with no instance shadowing, custom lookup or data-descriptor transformation", ""),
    ("import-cache-shares-modules", "import-cache", "aliasing", "causes", "The Module import cache causes Aliasing two names when importers bind the same cached module.", "Python 3; both imports use the same fully qualified name with its sys.modules entry intact", ""),
    ("immutability-enables-hashing", "immutable-object", "hashability", "enables", "An Immutable object enables Hashability of a type when its supported hash operation depends only on hashable stable contents.", "Python 3; the object is a built-in tuple whose elements are all hashable or a built-in frozenset", "A tuple containing a list is unhashable; immutability alone does not make arbitrary custom classes hashable."),
    ("mro-predicts-dunders", "mro", "dunder-methods", "predicts", "Method resolution order predicts which Dunder methods are found for inherited special-method operations.", "Python 3; implicit special-method lookup searches the operand type and its bases for the same method name", ""),
    ("import-cache-shares-class-state", "import-cache", "class-attribute", "causes", "The Module import cache causes Class attribute sharing across importers that retrieve the same cached class object.", "Python 3; a module defines a class once and repeated imports access that class without reload or rebinding", ""),
    ("eq-prereq-hash", "dunder-methods", "hashability", "prevents", "Defining equality Dunder methods without __hash__ prevents Hashability of a type because class creation sets __hash__ to None.", "Python 3; a new class defines __eq__ but supplies no __hash__ entry, even when a base class had a hash implementation", ""),
    ("exception-ends-iteration", "exception-flow", "iterator-protocol", "inhibits", "Exception control flow inhibits the Iterator protocol's normal value delivery when a generator raises an escaping error.", "Python 3.7+; a synchronous generator raises an unhandled exception instead of yielding its next value and the caller does not suppress it", "Ordinary iterator StopIteration is normal exhaustion; explicit StopIteration escaping generator code becomes RuntimeError."),
]

MYTHS = [
    ("variables-contain", "Python assignment copies values", "Binding a second name to a list reuses that list; mutation through either reference is visible through the other.", "name-binding"),
    ("is-equals-eq", "is and == are interchangeable", "is tests identity; == invokes equality behavior, which can be customized and can be non-reflexive for NaN.", "is-vs-eq"),
    ("gil-kills-io-parallel", "The GIL blocks all parallel work", "In the default CPython build, blocking I/O commonly releases the GIL and native extensions may release it for CPU work.", "gil"),
    ("lists-copy-themselves", "Assigning a list copies it", "Plain assignment does not duplicate a list or its nested elements.", "aliasing"),
    ("hints-enforced", "Type hints enforce types at run time", "Annotations alone do not check argument or return types; runtime validation requires additional code or a library.", "type-hints"),
    ("comprehensions-freeze-closures", "Comprehensions freeze each lambda's loop value", "In Python 3, [lambda: i for i in range(3)] produces closures that all return 2 after the comprehension completes.", "late-binding-closure"),
]

BOUNDARIES = [
    ("free-threading-edge", "Free-threaded builds can disable the GIL", "Default CPython 3.13/3.14 builds use the GIL; optional 3.13t/3.14t builds support disabling it, with supported status from 3.14 under PEP 779; configuration or an unsupported extension can re-enable it.", "gil"),
    ("refcount-promptness", "Reference counting is not a spec promise", "Python specifies no prompt collection guarantee; CPython reference counting does not make cyclic, immortal, resurrected or deferred-count objects disappear when a name is deleted.", "refcount-gc"),
    ("closure-defaults", "Defaults bind once, closures bind late", "A default expression is evaluated when the function is defined; a closure reads a captured variable later, and comprehension scope does not change that rule.", "default-mutable-arg"),
    ("hash-equality-contract", "Equal keys need equal hashes", "For hashable a and b, a == b requires hash(a) == hash(b), while equal hashes do not imply equality; custom classes must preserve this contract.", "hashability"),
]

EXAMPLES = [
    ("two-names-one-list", "Two names, one list", "After a = []; b = a; b.append(1), a is [1] because both names refer to the same list.", ["aliasing", "mutable-object", "shared-mutation"]),
    ("closure-loop-surprise", "Closures in a comprehension", "In Python 3, [f() for f in [lambda: i for i in range(3)]] is [2, 2, 2]; using lambda i=i: i instead yields [0, 1, 2], while the comprehension target does not leak outside.", ["late-binding-closure", "comprehension-scope", "loop-variable-leak"]),
    ("file-with-block", "Reading a file safely", "After successful open in a with statement, a ValueError inside the body invokes the file's __exit__, closing it before the exception propagates.", ["context-manager", "skipped-cleanup", "exception-flow"]),
    ("async-fetch", "Fetching many pages at once", "Separate asyncio tasks awaiting pending nonblocking reads let one loop thread overlap downloads; a CPU-bound loop without suspension delays the other tasks.", ["event-loop", "await-yield", "io-concurrency"]),
]

CONTROLS = [
    ("assignment-copies", "Assignment copies objects", "Assignment must not be treated as copying a mutable object."),
    ("tuple-holds-anything-mutable-trap", "Tuples make their contents immutable", "A tuple must not be treated as freezing the objects it holds."),
    ("gc-orders-destruction", "The collector guarantees cleanup order", "Garbage collection must not be treated as a portable guarantee of resource-release timing or order."),
    ("dicts-never-keep-order", "Dicts never keep order", "Python 3.7+ dictionaries must not be treated as orderless; insertion order is a language guarantee."),
]
