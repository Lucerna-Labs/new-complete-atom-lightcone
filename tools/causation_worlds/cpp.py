"""C++ causation: RAII, ownership, moves, smart pointers, dispatch, undefined behaviour."""

WORLD = "cpp-causation-v0"
PREFIX = "cpp"
DOMAIN = "language-ecosystems"
SUBJECT = "language-ecosystems.cpp"
SOURCES = ["cpp-standard"]
SCOPE = "Everyday C++ semantics: RAII and destructors, heap and stack lifetime, moves and copies, smart pointers, exceptions, templates versus virtuals, iterators"
ROOT_LABEL = "C++ causation world"
ROOT_STATEMENT = "Root of the C++ causation world: how object lifetime, ownership and dispatch rules cause C++ programs to behave as they do."

CONCEPTS = [
    ("raii", "RAII resource lifetime", "A resource's life tied to an object's scope.", []),
    ("stack-object", "Stack object scope", "An object living inside its enclosing block's frame.", []),
    ("heap-new", "Heap allocation with new", "Storage obtained manually and released by delete.", []),
    ("memory-leak", "Memory leak", "Allocated storage never returned.", []),
    ("dangling-pointer", "Dangling pointer", "A pointer to storage that has ended its life.", []),
    ("undefined-behavior", "Undefined behaviour", "The standard placing no limits on what happens next.", []),
    ("destructor-deterministic", "Deterministic destructor", "Cleanup running at a known moment, not at a collector's whim.", []),
    ("move-semantics", "Move semantics", "Transferring a resource instead of copying it.", []),
    ("moved-from-state", "Moved-from state", "The valid-but-unspecified source object after a move.", []),
    ("copy-constructor", "Copy constructor", "Making a duplicate of an object's value.", []),
    ("rule-of-five", "Rule of five", "Managing destructor, copy, move and their assign forms together.", []),
    ("unique-ownership", "unique_ptr ownership", "One exclusive smart owner deleting on scope exit.", []),
    ("shared-refcount", "shared_ptr refcount", "Several owners kept alive by a reference count.", []),
    ("cycle-shared", "shared_ptr cycle", "Owners in a loop keeping each other's counts above zero.", []),
    ("weak-breaks-cycle", "weak_ptr cycle break", "Non-owning references that do not feed the count.", []),
    ("exception-unwinding", "Exception unwinding", "A throw leaving scopes and running destructors on the way.", []),
    ("const-correctness", "Const correctness", "Marking what must not change, enforced by the type system.", []),
    ("reference-binding", "Reference binding", "An alias bound once to an object.", []),
    ("pointer-rebind", "Pointer rebinding", "Pointers able to retarget and be null.", []),
    ("template-instantiation", "Template instantiation", "The compiler stamping code per used type.", []),
    ("generic-static-dispatch", "Generic static dispatch", "Calls resolved to the exact function at compile time.", []),
    ("virtual-function", "Virtual function", "A call resolved by the dynamic type at run time.", []),
    ("vtable-dispatch", "Vtable dispatch", "Looking up the function through the object's table.", []),
    ("object-slicing", "Object slicing", "Copying a derived object into a base, losing the added part.", []),
    ("override-keyword", "Override checking", "The override marker verifying a function really overrides.", []),
    ("iterator-invalidation", "Iterator invalidation", "Container changes making held iterators stale.", []),
    ("vector-contiguous", "Vector contiguous storage", "Elements packed in one growing array.", []),
    ("value-semantics", "Value semantics default", "Assignment and passing copying values by default.", []),
    ("lifetime-extension", "Temporary lifetime extension", "A const reference keeping a temporary alive.", []),
    ("static-init-order", "Static initialisation order fiasco", "Globals initialising in an unpredictable cross-file order.", []),
]

RELATIONS = [
    ("raii-ties-scope", "raii", "stack-object", "enables", "RAII resource lifetime enables a stack object scope to own and free its resource.", "the object goes out of scope", ""),
    ("scope-runs-destructor", "stack-object", "destructor-deterministic", "causes", "Leaving the stack object scope causes the deterministic destructor to run at a known time.", "control exits the block", ""),
    ("deterministic-prevents-leaks", "destructor-deterministic", "memory-leak", "prevents", "A deterministic destructor prevents a memory leak for scope-owned resources.", "every resource has an owner", ""),
    ("new-leaks-without-delete", "heap-new", "memory-leak", "causes", "A heap allocation with new without a matching delete causes a memory leak.", "the pointer is lost or goes out of scope", ""),
    ("unique-prevents-leaks", "unique-ownership", "memory-leak", "prevents", "unique_ptr ownership prevents a memory leak by deleting on scope exit.", "the smart pointer owns the allocation", ""),
    ("shared-prevents-leaks", "shared-refcount", "memory-leak", "prevents", "shared_ptr refcount tracking prevents a memory leak until the last owner leaves.", "counts reach zero eventually", ""),
    ("cycle-inhibits-counting", "cycle-shared", "shared-refcount", "inhibits", "A shared_ptr cycle inhibits shared_ptr refcount from reaching zero.", "nodes hold each other", ""),
    ("weak-prevents-cycle-leak", "weak-breaks-cycle", "cycle-shared", "prevents", "A weak_ptr cycle break prevents the shared_ptr cycle from leaking both nodes.", "back edges use weak references", ""),
    ("dangling-causes-ub", "dangling-pointer", "undefined-behavior", "causes", "Using a dangling pointer causes undefined behaviour at once.", "the pointed-to object was freed", ""),
    ("invalidation-dangles", "iterator-invalidation", "dangling-pointer", "causes", "Iterator invalidation causes a dangling pointer equivalent for kept iterators after a reallocation.", "an element pointer or iterator is held across growth", ""),
    ("growth-invalidates", "vector-contiguous", "iterator-invalidation", "causes", "Growing the vector contiguous storage causes iterator invalidation of every old element pointer.", "the vector reallocates on push", ""),
    ("move-causes-moved-from", "move-semantics", "moved-from-state", "causes", "Applying move semantics causes a moved-from state in the source object.", "the object is std-moved", ""),
    ("moved-from-inhibits-ub", "moved-from-state", "undefined-behavior", "inhibits", "A specified moved-from state inhibits undefined behaviour after a move.", "only operations valid on empty objects are used", ""),
    ("move-inhibits-copy", "move-semantics", "copy-constructor", "inhibits", "Move semantics inhibits needless copy constructor work for temporary values.", "the value is an expiring temporary", ""),
    ("copy-prereq-rule-five", "copy-constructor", "rule-of-five", "prerequisite", "Declaring a copy constructor is a prerequisite for the rule of five to kick in.", "the class manages a resource", ""),
    ("rule-five-prevents-leaks", "rule-of-five", "memory-leak", "prevents", "Following the rule of five prevents a memory leak from half-managed resources.", "all five members are handled", ""),
    ("unwinding-enables-cleanup", "exception-unwinding", "destructor-deterministic", "enables", "Exception unwinding enables the deterministic destructor to clean up on the throw path.", "an exception propagates through scopes", ""),
    ("raii-enables-exception-safety", "raii", "exception-unwinding", "enables", "RAII resource lifetime enables exception unwinding cleanup without manual finally blocks.", "resources are stack-owned", ""),
    ("const-enables-binding", "const-correctness", "reference-binding", "enables", "Const correctness enables reference binding that promises no mutation.", "a function takes const references", ""),
    ("reference-prevents-rebind", "reference-binding", "pointer-rebind", "prevents", "Reference binding prevents pointer rebinding after initialisation.", "the reference is initialised once", ""),
    ("pointer-enables-rebind", "pointer-rebind", "reference-binding", "enables", "Pointer rebinding enables what reference binding cannot: retargeting.", "a handle must change targets", ""),
    ("instantiation-causes-static-dispatch", "template-instantiation", "generic-static-dispatch", "causes", "Template instantiation causes generic static dispatch per concrete type.", "the template is used with a type", ""),
    ("static-dispatch-inhibits-vtable", "generic-static-dispatch", "vtable-dispatch", "inhibits", "Generic static dispatch inhibits vtable dispatch overhead for template calls.", "the type is known at compile time", ""),
    ("virtual-causes-vtable", "virtual-function", "vtable-dispatch", "causes", "Declaring a virtual function causes vtable dispatch at run time.", "the call goes through a base pointer", ""),
    ("override-checks-signatures", "override-keyword", "virtual-function", "enables", "Override checking enables virtual function signature mistakes to fail at compile time.", "the compiler sees the override marker", ""),
    ("slicing-inhibits-virtual", "object-slicing", "virtual-function", "inhibits", "Object slicing inhibits virtual function calls by copying away the derived part.", "a derived value assigns to a base by value", ""),
    ("value-semantics-copies", "value-semantics", "copy-constructor", "enables", "Value semantics default enables predictable copy constructor based duplication.", "no move applies", ""),
    ("extension-prevents-dangling", "lifetime-extension", "dangling-pointer", "prevents", "Temporary lifetime extension prevents a dangling pointer from a const reference binding.", "a const reference binds a temporary", ""),
    ("static-init-causes-ub", "static-init-order", "undefined-behavior", "causes", "A static initialisation order fiasco causes undefined behaviour across translation units.", "globals reference globals in another file", ""),
    ("unique-enables-transfer", "unique-ownership", "move-semantics", "enables", "unique_ptr ownership enables move semantics transfers without copying.", "the pointer is returned or stored", ""),
    ("shared-enables-cycles", "shared-refcount", "cycle-shared", "enables", "shared_ptr refcount tracking enables a shared_ptr cycle when nodes hold each other.", "back pointers are strong", ""),
    ("manual-delete-dangles", "heap-new", "dangling-pointer", "causes", "A mistimed delete of heap allocation with new causes a dangling pointer or worse.", "delete timing is hand-written", ""),
    ("stack-enables-raii", "stack-object", "raii", "enables", "Cheap stack object scope lifetime enables RAII resource lifetime patterns by default.", "the value fits and stays local", ""),
    ("unique-inhibits-shared-overhead", "unique-ownership", "shared-refcount", "inhibits", "Preferring unique_ptr ownership inhibits needless shared_ptr refcount overhead.", "single ownership suffices", ""),
    ("templates-inhibit-type-ub", "template-instantiation", "undefined-behavior", "inhibits", "Template instantiation inhibits type-mismatch undefined behaviour by checking each use at compile time.", "the use compiles", ""),
    ("virtual-reference-prevents-slicing", "virtual-function", "object-slicing", "prevents", "A base reference virtual function call prevents object slicing by keeping the whole object.", "arguments pass by reference", ""),
    ("move-enables-growth", "move-semantics", "vector-contiguous", "enables", "Cheap move semantics enables vector contiguous storage growth without deep copies.", "the vector grows", ""),
    ("weak-enables-observation", "weak-breaks-cycle", "shared-refcount", "enables", "A weak_ptr cycle break enables observing shared_ptr refcount targets without owning them.", "a handle may dangle logically", ""),
    ("const-prevents-ub", "const-correctness", "undefined-behavior", "prevents", "Const correctness prevents undefined behaviour from modifying truly const objects.", "the object was defined const", ""),
    ("unwinding-prevents-leaks", "exception-unwinding", "memory-leak", "prevents", "Stack-based exception unwinding prevents a memory leak of owned locals on throw.", "locals own their resources", ""),
]

MYTHS = [
    ("cpp-has-gc", "C++ has a garbage collector",
     "There is none; RAII resource lifetime and deterministic destructors do the freeing.", "raii"),
    ("all-virtual", "All member functions are virtual",
     "Functions are non-virtual by default; only marked ones use vtable dispatch.", "virtual-function"),
    ("ub-crashes", "Undefined behaviour always crashes",
     "Anything may happen, including appearing to work until it does not.", "undefined-behavior"),
    ("shared-always-safe", "shared_ptr is always safe",
     "A shared_ptr cycle leaks both nodes; a weak_ptr cycle break is needed.", "cycle-shared"),
    ("std-move-moves", "std::move moves the object",
     "std::move only casts; move semantics in the constructor perform the transfer.", "move-semantics"),
]

BOUNDARIES = [
    ("ub-no-fence", "Undefined behaviour has no fence",
     "Once triggered, the whole program run is unconstrained.", "undefined-behavior"),
    ("abi-frozen", "ABI stability pins layouts",
     "A frozen ABI limits how vtable dispatch layouts may change.", "vtable-dispatch"),
    ("constexpr-gates", "Compile-time code has gates",
     "Constant evaluation forbids side effects at compile time.", "template-instantiation"),
]

EXAMPLES = [
    ("file-guard", "A file guard class",
     "A guard holds the handle; its deterministic destructor closes it on every path.",
     ["raii", "destructor-deterministic", "exception-unwinding"]),
    ("push-back-dangle", "Holding an element pointer across push_back",
     "Growing vector contiguous storage triggers iterator invalidation of old pointers.",
     ["vector-contiguous", "iterator-invalidation", "dangling-pointer"]),
    ("tree-parent-links", "Tree nodes with parent links",
     "Back edges held by shared_ptr refcount create a cycle that a weak_ptr cycle break fixes.",
     ["shared-refcount", "cycle-shared", "weak-breaks-cycle"]),
    ("shape-hierarchy", "A shape hierarchy",
     "Base-reference virtual function calls reach the derived override while by-value copies cause object slicing.",
     ["virtual-function", "vtable-dispatch", "object-slicing"]),
]

CONTROLS = [
    ("freed-memory-defined", "Using freed memory is defined",
     "A dangling pointer must not be treated as safe to use."),
    ("references-reseat", "References can be re-seated",
     "Reference binding must not be treated as retargetable."),
    ("override-changes-runtime", "override changes run-time dispatch",
     "Override checking must not be treated as altering run-time dispatch."),
    ("sliced-stays-polymorphic", "Sliced objects stay polymorphic",
     "Object slicing must not be treated as keeping derived behaviour."),
]
