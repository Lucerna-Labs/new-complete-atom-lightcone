"""Python causation: name binding, mutability, aliasing, GIL, generators, closures, cleanup."""

WORLD = "python-causation-v0"
PREFIX = "pyc"
DOMAIN = "language-ecosystems"
SUBJECT = "language-ecosystems.python"
SOURCES = ["python-language-314"]
SCOPE = "Everyday Python semantics: names versus objects, mutability and aliasing, hashing, the GIL, asyncio, generators, closures, exceptions and cleanup"
ROOT_LABEL = "Python causation world"
ROOT_STATEMENT = "Root of the Python causation world: how name binding, mutability and reference rules cause Python programs to behave as they do."

CONCEPTS = [
    ("name-binding", "Name binding to an object", "A Python name is a label attached to an object, never a box holding one.", []),
    ("object-identity", "Object identity", "Each object's own id, distinct from what it equals.", []),
    ("mutable-object", "Mutable object", "An object whose value can change in place, like a list or dict.", []),
    ("immutable-object", "Immutable object", "An object whose value can never change, like a str or tuple.", []),
    ("aliasing", "Aliasing two names", "Two names attached to the very same object.", []),
    ("shallow-copy", "Shallow copy", "A copy of the outer container that still shares nested objects.", []),
    ("deep-copy", "Deep copy", "A copy duplicating every nesting level.", []),
    ("is-vs-eq", "Identity versus equality", "The is operator compares object identity while == compares value.", []),
    ("hashability", "Hashability of a type", "A type whose instances keep one stable hash, required for set and dict keys.", []),
    ("dict-key", "Dictionary key lookup", "Finding a value by hashing the key then comparing candidates.", []),
    ("gil", "Global interpreter lock", "One lock letting only one thread run Python bytecode at a time.", ["GIL"]),
    ("thread-parallelism", "Thread parallelism limits", "CPU-bound threads taking turns instead of running truly together.", []),
    ("event-loop", "Asyncio event loop", "One loop that runs cooperative tasks on a single thread.", []),
    ("await-yield", "Await yielding control", "An await point where a task hands control back to the loop.", []),
    ("generator-lazy", "Generator lazy evaluation", "Producing items only when asked, one at a time.", []),
    ("yield-suspension", "Yield suspension point", "Where a generator pauses, keeping its state for the next call.", []),
    ("iterator-protocol", "Iterator protocol", "The dunder pair that makes any object work with for loops.", []),
    ("comprehension-scope", "Comprehension scope", "List comprehensions binding their loop variable in a private scope.", []),
    ("late-binding-closure", "Closure late binding", "Closures capturing variables by name, resolved at call time.", []),
    ("default-mutable-arg", "Default mutable argument", "A default value created once at function definition and reused across calls.", []),
    ("exception-flow", "Exception control flow", "An error unwinding the stack until a handler catches it.", []),
    ("finally-guarantee", "Finally guarantee", "The finally block running no matter how the try exits.", []),
    ("context-manager", "Context manager with-block", "A with block guaranteeing enter and exit around a resource.", []),
    ("refcount-gc", "Reference counting cleanup", "Objects freed the moment their reference count hits zero.", []),
    ("cycle-collector", "Cycle collector", "The periodic scan that frees objects referencing each other in loops.", []),
    ("duck-typing", "Duck typing", "Behaviour decided by the methods an object has, not its declared type.", []),
    ("dunder-methods", "Dunder methods", "The double-underscore hooks Python calls for built-in operations.", []),
    ("property-descriptor", "Property descriptor", "An attribute whose get and set run code behind a plain look.", []),
    ("class-attribute", "Class attribute sharing", "One value stored on the class and read by every instance.", []),
    ("instance-attribute", "Instance attribute shadowing", "An instance's own value hiding the class attribute.", []),
    ("mro", "Method resolution order", "The fixed search order through bases when looking up attributes.", []),
    ("import-cache", "Module import cache", "Imported modules stored once and shared across every importer.", []),
    ("type-hints", "Type hints unenforced", "Annotations stored for tools but not checked at run time.", []),
]

RELATIONS = [
    ("binding-enables-identity", "name-binding", "object-identity", "enables", "A name binding to an object enables object identity checks through the is operator.", "two names are compared", ""),
    ("aliasing-causes-shared-state", "aliasing", "mutable-object", "causes", "Aliasing two names causes mutable object changes to show through both names.", "one object gains two names", ""),
    ("immutability-prevents-alias-bugs", "immutable-object", "aliasing", "prevents", "An immutable object prevents aliasing two names from creating shared-state surprises.", "the value can never change in place", ""),
    ("shallow-copy-limits", "shallow-copy", "aliasing", "inhibits", "A shallow copy inhibits outer-level aliasing two names but keeps nested shared parts.", "only the top level is copied", ""),
    ("deep-copy-prevents-sharing", "deep-copy", "aliasing", "prevents", "A deep copy prevents aliasing two names at every nesting level.", "the whole structure is duplicated", ""),
    ("identity-predicts-equality", "object-identity", "is-vs-eq", "predicts", "A shared object identity predicts the equality side of identity versus equality also passing.", "the default equality compares identity", ""),
    ("hashability-prereq-keys", "hashability", "dict-key", "prerequisite", "Hashability of a type is a prerequisite for dictionary key lookup to work.", "a type wants to be a key", ""),
    ("mutability-prevents-hashing", "mutable-object", "hashability", "prevents", "A mutable object prevents hashability of a type by allowing change after hashing.", "the object can mutate", ""),
    ("dictkey-tests-equality", "dict-key", "is-vs-eq", "enables", "Dictionary key lookup enables the identity versus equality distinction to matter for custom keys.", "keys are compared after hashing", ""),
    ("gil-limits-threads", "gil", "thread-parallelism", "inhibits", "The global interpreter lock inhibits thread parallelism limits from lifting for CPU-bound bytecode.", "several threads want to run Python code at once", ""),
    ("await-yields-to-loop", "await-yield", "event-loop", "enables", "An await yielding control enables the asyncio event loop to run other tasks meanwhile.", "a coroutine awaits I/O", ""),
    ("loop-bypasses-gil", "event-loop", "gil", "enables", "The asyncio event loop enables I-O concurrency that sidesteps the global interpreter lock bottleneck.", "tasks cooperate at await points", ""),
    ("yield-enables-lazy", "yield-suspension", "generator-lazy", "enables", "A yield suspension point enables generator lazy evaluation one item at a time.", "a generator function runs", ""),
    ("generator-drives-iterator", "generator-lazy", "iterator-protocol", "enables", "Generator lazy evaluation enables the iterator protocol over huge or endless streams.", "items are pulled on demand", ""),
    ("comprehension-isolates", "comprehension-scope", "late-binding-closure", "prevents", "The comprehension scope prevents closure late binding leaks from its loop variable.", "a comprehension assigns its own loop target", ""),
    ("closure-late-binding", "late-binding-closure", "name-binding", "causes", "Closure late binding causes the name binding to an object to be looked up at call time, not creation time.", "loops create closures capturing a variable", ""),
    ("default-mutable-shared", "default-mutable-arg", "aliasing", "causes", "A default mutable argument causes hidden aliasing two names across calls.", "the function is called repeatedly without the argument", ""),
    ("exception-enables-finally", "exception-flow", "finally-guarantee", "enables", "Exception control flow enables the finally guarantee to run cleanup on the way out.", "an exception propagates", ""),
    ("with-enables-cleanup", "context-manager", "finally-guarantee", "enables", "A context manager with-block enables the finally guarantee style cleanup for resources.", "the with block exits normally or by exception", ""),
    ("refcount-ties-to-names", "refcount-gc", "name-binding", "causes", "Reference counting cleanup causes prompt disposal when the last name binding to an object goes away.", "an object's reference count reaches zero", ""),
    ("cycle-collector-frees-loops", "cycle-collector", "refcount-gc", "enables", "The cycle collector enables reference counting cleanup to reclaim mutually referencing objects.", "objects reference each other in a loop", ""),
    ("duck-typing-uses-dunders", "duck-typing", "dunder-methods", "enables", "Duck typing enables dunder methods to drive what operations an object supports.", "an operation is attempted at run time", ""),
    ("dunder-enables-iteration", "dunder-methods", "iterator-protocol", "enables", "Defining dunder methods enables the iterator protocol for a custom class.", "iter and next are implemented", ""),
    ("property-intercepts-access", "property-descriptor", "instance-attribute", "enables", "A property descriptor enables the instance attribute shadowing pattern to hide a computed value.", "an attribute access is intercepted", ""),
    ("class-attr-read-through", "class-attribute", "instance-attribute", "causes", "Class attribute sharing causes instance attribute shadowing to matter for per-object values.", "instances read an attribute the class also holds", ""),
    ("instance-shadowing-protects", "instance-attribute", "class-attribute", "inhibits", "Instance attribute shadowing inhibits accidental writes that would defeat class attribute sharing.", "an instance assigns its own value", ""),
    ("mro-predicts-lookup", "mro", "class-attribute", "predicts", "The method resolution order predicts which value class attribute sharing serves in a diamond layout.", "multiple bases share a parent", ""),
    ("import-cache-shares-modules", "import-cache", "aliasing", "causes", "The module import cache causes module-level aliasing two names of one module across the program.", "a module is imported in several places", ""),
    ("hints-leave-duck-typing", "type-hints", "duck-typing", "enables", "Leaving type hints unenforced at run time enables duck typing to remain the rule.", "annotations are present but not checked", ""),
    ("immutability-enables-hashing", "immutable-object", "hashability", "enables", "An immutable object enables hashability of a type by keeping its hash stable.", "the value never changes", ""),
    ("mutable-needs-shallow-copy", "mutable-object", "shallow-copy", "causes", "Handing out a mutable object causes a shallow copy to be needed to protect the original.", "a function stores its argument", ""),
    ("await-uses-generators", "await-yield", "generator-lazy", "enables", "An await yielding control enables generator lazy evaluation machinery to drive coroutines.", "coroutines are implemented over generators", ""),
    ("mro-predicts-dunders", "mro", "dunder-methods", "predicts", "The method resolution order predicts which dunder methods a mix-in provides first.", "mix-ins define the same name", ""),
    ("import-cache-shares-class-state", "import-cache", "class-attribute", "causes", "The module import cache causes module-level class attribute sharing program-wide.", "the module is imported again elsewhere", ""),
    ("deep-copy-beats-shallow", "deep-copy", "shallow-copy", "prevents", "A deep copy prevents the shallow copy trap of shared nested parts.", "nested containers must be independent", ""),
    ("with-enables-deterministic-cleanup", "context-manager", "refcount-gc", "enables", "A context manager with-block enables deterministic cleanup without waiting for reference counting cleanup.", "the with block scope ends", ""),
    ("duck-typing-prereq-iterator", "duck-typing", "iterator-protocol", "prerequisite", "Duck typing is a prerequisite for the iterator protocol to accept any iterable.", "an object is passed to a for loop", ""),
    ("eq-prereq-hash", "dunder-methods", "hashability", "prerequisite", "Defining equality dunder methods is a prerequisite for hashability of a type to stay consistent.", "a class defines eq without hash", ""),
    ("exception-ends-iteration", "exception-flow", "iterator-protocol", "inhibits", "A raised exception control flow inhibits the iterator protocol mid-stream and ends iteration with an error.", "an exception escapes the generator", ""),
    ("loop-avoids-gil-contention", "event-loop", "gil", "inhibits", "The asyncio event loop inhibits global interpreter lock contention by staying on one thread.", "all work stays on one loop thread", ""),
    ("aliasing-makes-shallow-look-fine", "aliasing", "shallow-copy", "causes", "Aliasing two names causes a shallow copy to look sufficient while nests stay shared.", "a copied list holds sublists", ""),
]

MYTHS = [
    ("variables-contain", "Python variables contain values",
     "A name binding to an object is a label on an object, not a box with a value inside.", "name-binding"),
    ("is-equals-eq", "is and == are interchangeable",
     "The is operator tests object identity while == tests value equality.", "is-vs-eq"),
    ("gil-kills-io-parallel", "The GIL blocks all parallel work",
     "I/O releases the global interpreter lock, so I/O threads overlap fine.", "gil"),
    ("lists-copy-themselves", "Assigning a list copies it",
     "Assignment creates aliasing two names on one list; mutation shows through both.", "aliasing"),
    ("hints-enforced", "Type hints enforce types at run time",
     "Type hints unenforced are for tools; the interpreter ignores them.", "type-hints"),
]

BOUNDARIES = [
    ("free-threading-edge", "Free-threaded builds relax the GIL",
     "Newer experimental builds loosen the global interpreter lock; the default still holds it.", "gil"),
    ("refcount-promptness", "Reference counting is not a spec promise",
     "Prompt disposal via reference counting cleanup is an implementation behaviour, not guaranteed timing.", "refcount-gc"),
    ("closure-defaults", "Defaults bind once, closures bind late",
     "A default mutable argument is made once at definition while closure late binding defers to call time.", "default-mutable-arg"),
]

EXAMPLES = [
    ("two-names-one-list", "Two names, one list",
     "Appending through one name shows up through the other because both are aliasing two names on one list.",
     ["aliasing", "mutable-object", "name-binding"]),
    ("closure-loop-surprise", "Closures in a loop",
     "Handlers built in a loop all see the last value until closure late binding is fixed with a default.",
     ["late-binding-closure", "comprehension-scope", "default-mutable-arg"]),
    ("file-with-block", "Reading a file safely",
     "A context manager with-block closes the file on every path, resting on the finally guarantee.",
     ["context-manager", "finally-guarantee", "exception-flow"]),
    ("async-fetch", "Fetching many pages at once",
     "One asyncio event loop overlaps downloads because each await yielding control lets another task run.",
     ["event-loop", "await-yield", "gil"]),
]

CONTROLS = [
    ("assignment-copies", "Assignment copies objects",
     "Assignment must not be treated as copying a mutable object."),
    ("tuple-holds-anything-mutable-trap", "Tuples make their contents immutable",
     "A tuple must not be treated as freezing the objects it holds."),
    ("gc-orders-destruction", "The collector runs destructors in order",
     "Reference counting cleanup must not be treated as ordering teardown."),
    ("dict-preserves-insert-order-forever", "Dicts never keep order",
     "Dictionaries must not be treated as orderless; they keep insertion order."),
]
