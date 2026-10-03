"""Go causation: synchronization, interfaces, slices, cancellation and lifetime."""

WORLD = "go-causation-v0"
PREFIX = "gol"
DOMAIN = "language-ecosystems"
SUBJECT = "language-ecosystems.go"
SOURCES = ["go-spec-127", "go-memory-model", "go-runtime-gc-guide", "go-loopvar-122", "go-sync", "go-context"]
SCOPE = "Go 1 language semantics with Go 1.22 module-version loop boundaries and implementation-specific gc runtime behavior: channels, races, interfaces, defer, slices, maps and cancellation"
ROOT_LABEL = "Go causation world"
ROOT_STATEMENT = "Root of the Go causation world: how communication, ownership and runtime mechanisms affect Go program behavior."

CONCEPTS = [
    ("goroutine", "Goroutine launch", "A go statement starting a function call that executes concurrently in the same address space.", []),
    ("channel-send", "Channel send", "An operation transferring a value into a channel; readiness depends on channel state and receivers.", []),
    ("channel-receive", "Channel receive", "An operation obtaining a channel value, or the zero value with false status after closure and buffer exhaustion.", []),
    ("channel-blocking", "Channel send blocking", "A send waiting because an open channel has neither an available receiver nor spare buffer capacity.", []),
    ("buffered-channel", "Buffered channel", "A channel with positive capacity that can queue sent values before they are received.", []),
    ("channel-deadlock", "Channel deadlock", "A set of goroutines whose channel waits have no possible progress-producing partner.", []),
    ("select-statement", "Select statement", "A statement choosing one ready communication, or default when present and no communication can proceed.", []),
    ("share-by-communicating", "Share memory by communicating", "An ownership convention in which synchronized messages transfer exclusive access to shared mutable data.", []),
    ("wait-group", "WaitGroup completion", "sync.WaitGroup.Wait returning once all registered work has decremented the counter to zero.", []),
    ("mutex-protect", "Mutex protection", "Use of the same mutex to order conflicting accesses in a critical section.", []),
    ("data-race-go", "Data race in Go", "Conflicting memory accesses in different goroutines, at least one write and at least one non-atomic access, not ordered by happens-before.", []),
    ("scheduler-mn", "M-N goroutine scheduling", "The gc runtime multiplexing goroutines onto OS threads rather than assigning one permanent thread per goroutine.", []),
    ("escape-analysis", "Escape analysis to heap", "A compiler decision to place an allocation on the heap when it cannot keep the allocation safely within a stack frame.", []),
    ("stack-allocation-go", "Stack allocation in Go", "Compiler placement of a value in stack storage whose duration covers all uses.", []),
    ("concurrent-gc", "Concurrent garbage collector", "The gc runtime's tracing collector performing much work alongside mutators while retaining stop-the-world phases.", []),
    ("implicit-interface", "Implicit interface satisfaction", "A type satisfying a basic interface through its method set without an implements declaration.", []),
    ("nil-interface", "Nil interface versus nil pointer", "An interface with a dynamic pointer type and nil dynamic value is not the nil interface.", []),
    ("error-value", "Error value returns", "Returning a value of the error interface type to report success or failure through an explicit convention.", []),
    ("multiple-returns", "Multiple return values", "A function signature and return statement supplying more than one result.", []),
    ("defer-stack", "Defer stack", "Deferred calls executed in reverse registration order on function return or panic unwinding; call arguments are evaluated at registration.", []),
    ("panic-recover", "Panic and recover", "Panic unwinding within a goroutine and direct recover calls in deferred functions that can stop the panic.", []),
    ("slice-backing", "Slice backing array", "The array storage referenced by one or more slice descriptors.", []),
    ("append-growth", "Append beyond capacity", "Appending enough elements that the required length exceeds the current slice capacity.", []),
    ("map-random-order", "Unspecified map iteration order", "The language specifies no map traversal order; runtime randomization does not promise a different order on every traversal.", []),
    ("embedding-composition", "Embedding composition", "Embedded fields can contribute promoted methods to a containing type's method set under the selector rules.", []),
    ("exported-capitals", "Exported capital naming", "Package-level or field/method identifiers beginning with an uppercase Unicode letter can be exported under the spec's rules.", []),
    ("context-cancel", "Context cancellation", "Closing a context's Done channel to signal cancellation to code that observes and acts on it.", []),
    ("zero-values", "Type zero values", "The default values of Go types, including numeric zero, false, empty strings and nil for pointer-like types; not every zero value permits every operation.", []),
    ("package-init", "Package initialisation order", "Initialization of imported packages and then dependent packages before execution of main.main.", []),
    ("loop-var-capture", "Loop variable capture", "Closures retaining references to loop variables; the creation or reuse of those variables depends on loop syntax and language version.", []),
    ("early-main-return", "Early main return", "main.main returning while worker goroutines still have unfinished work, ending the program without waiting for them.", []),
    ("goroutine-leak", "Goroutine leak", "A goroutine retained indefinitely after its useful work should have ended, often at a blocking operation.", []),
    ("program-termination", "Program termination from panic", "The program exiting after an unrecovered panic reaches the top of a goroutine's call stack.", []),
    ("receive-blocking", "Channel receive blocking", "A channel receive waiting because neither buffered data nor a sender nor closed-channel completion is available.", []),
    ("heap-allocation-rate", "Heap allocation rate", "Heap memory allocated per unit of execution or time, affecting garbage-collection workload.", []),
    ("order-dependent-output", "Order-dependent output variation", "Output changing when processing the same entries in different orders.", []),
    ("unexported-interface-method", "Unexported interface method", "An interface method whose package-qualified identity cannot be recreated by declaring a same-spelled method in another package.", []),
    ("successful-recovery", "Successful panic recovery", "A direct recover call in a deferred function stopping the active panic in its own goroutine.", []),
    ("unrecovered-panic", "Unrecovered panic", "An active panic that no deferred function successfully recovers while the goroutine unwinds.", []),
    ("main-entry", "Main function entry", "Beginning execution of main.main after program initialization completes.", []),
]

RELATIONS = [
    ("goroutine-cheap-enables-scheduling", "scheduler-mn", "goroutine", "enables", "M-N goroutine scheduling enables Goroutine launch without requiring a dedicated permanent OS thread for each goroutine.", "Go 1.27 gc runtime; ordinary go statements create goroutines not explicitly locked to OS threads", ""),
    ("receive-pairs-send", "channel-receive", "channel-send", "prerequisite", "A matching Channel receive is a prerequisite for Channel send to complete on an open unbuffered channel.", "Go 1; the channel is non-nil, open and unbuffered and the send completes normally", ""),
    ("buffer-decouples", "buffered-channel", "channel-blocking", "prevents", "A Buffered channel prevents Channel send blocking of a send while spare buffer capacity is available.", "Go 1; the channel is open and non-nil and has room for the sent element at the moment of the send", ""),
    ("no-receiver-deadlocks", "channel-send", "channel-deadlock", "causes", "A Channel send causes Channel deadlock when every possible receiver is blocked with no path to progress.", "Go 1; all goroutines capable of releasing an unbuffered send are in a closed cycle of channel waits with no external unblock event", ""),
    ("select-prevents-deadlock", "select-statement", "channel-deadlock", "prevents", "A Select statement prevents Channel deadlock at its communication choice by taking default if no communication is ready.", "Go 1; select has a default clause, so selection itself never blocks, and evaluation of operands and the selected body do not block", "This prevents blocking at that select, not deadlock in other statements or goroutines."),
    ("communicating-prevents-races", "share-by-communicating", "data-race-go", "prevents", "Share memory by communicating prevents a Data race in Go when channel synchronization transfers exclusive mutable access.", "Go 1 memory model; the sender ceases access before sending ownership and the receiver alone accesses the data after receipt", ""),
    ("mutex-protects-state", "mutex-protect", "data-race-go", "prevents", "Mutex protection prevents a Data race in Go for accesses consistently ordered by the same mutex.", "Go 1 memory model; every conflicting access to the protected memory occurs while holding the same non-copied mutex", ""),
    ("escape-inhibits-stack", "escape-analysis", "stack-allocation-go", "prevents", "Escape analysis to heap prevents Stack allocation in Go for an allocation that the compiler assigns to the heap.", "Go 1.27 gc compiler; an escaping allocation remains after optimization and is assigned to the heap rather than the current frame", "Escape-analysis results are implementation decisions and can change with compiler versions and inlining."),
    ("stack-eases-gc", "stack-allocation-go", "heap-allocation-rate", "inhibits", "Stack allocation in Go inhibits Heap allocation rate by satisfying the corresponding storage request in a stack frame.", "Go 1.27 gc compiler; otherwise equivalent executed allocations use stack storage instead of heap storage and are not optimized away", "Stack roots may still require GC scanning."),
    ("gc-keeps-running", "concurrent-gc", "goroutine", "enables", "A Concurrent garbage collector enables Goroutine launch and execution during its concurrent collection phases.", "Go 1.27 gc runtime; the collector is in a concurrent phase rather than a stop-the-world phase and runnable mutator work is scheduled", "Collection assists and stop-the-world phases can still delay goroutine work."),
    ("nil-box-surprise", "nil-interface", "error-value", "predicts", "Nil interface versus nil pointer predicts non-nil Error value returns when a typed nil pointer is boxed as error.", "Go 1; a nil pointer whose type implements error is returned directly from a function with an error result", ""),
    ("errors-enable-returns", "multiple-returns", "error-value", "enables", "Using Multiple return values enables Error value returns alongside a separate successful result.", "Go 1; a function declares a result pair such as (Value, error) and follows the nil-error success convention", ""),
    ("defer-enables-recover", "defer-stack", "panic-recover", "enables", "The Defer stack enables Panic and recover to stop an active panic in a deferred function.", "Go 1; the deferred function directly invokes recover while unwinding an active panic in the same goroutine", ""),
    ("recover-prevents-crash", "successful-recovery", "program-termination", "prevents", "Successful panic recovery prevents Program termination from panic for the recovered panic.", "Go 1; recover is called directly by a deferred function in the panicking goroutine and cleanup raises no replacement panic", "Runtime fatal errors are not necessarily recoverable panics."),
    ("slice-aliasing-races", "slice-backing", "data-race-go", "causes", "A shared Slice backing array causes a Data race in Go when goroutines make unordered conflicting accesses to the same element.", "Go 1 memory model; different goroutines access overlapping array cells through slices, at least one writes, and no synchronization orders them", "Disjoint element accesses do not race merely because the slices share an array."),
    ("append-reallocates", "append-growth", "slice-backing", "causes", "Append beyond capacity causes a replacement Slice backing array to be allocated and the existing elements copied into it.", "Go 1; the new length exceeds the old capacity and the append succeeds rather than failing allocation", "No fixed growth factor is guaranteed by the language."),
    ("embedding-promotes-methods", "embedding-composition", "implicit-interface", "enables", "Embedding composition enables Implicit interface satisfaction through methods promoted into the containing type's method set.", "Go 1; the promoted methods are unambiguous, have the required signatures and belong to the relevant value or pointer method set", ""),
    ("export-prereq-interface", "unexported-interface-method", "implicit-interface", "prevents", "An Unexported interface method prevents Implicit interface satisfaction by an independently declared same-spelled method in another package.", "Go 1; the implementing type is in a different package and does not inherit the original package's method through embedding", "Embedding a type that already supplies the originating package's method can satisfy the interface."),
    ("context-prevents-stuck-wait", "context-cancel", "channel-blocking", "prevents", "Context cancellation prevents Channel send blocking from waiting forever when the wait selects a cancellation alternative.", "Go 1.7+ context; the blocked select includes the context Done channel and returns when cancellation closes it", "A plain blocking send without a cancellation case is not interrupted by context cancellation."),
    ("zero-values-cause-nil-box", "zero-values", "nil-interface", "causes", "Type zero values causes the Nil interface versus nil pointer distinction when a zero-initialized pointer is boxed.", "Go 1; an uninitialized variable of type *T is nil and is then returned or assigned as an interface that *T implements", "An uninitialized interface variable itself is nil until it is given a dynamic type and value."),
    ("package-init-prereq-main", "package-init", "main-entry", "prerequisite", "Completed Package initialisation order is a prerequisite for Main function entry.", "Go 1; a Go program executes imported package initializers and main package initializers successfully before calling main.main", "Initializers may launch goroutines that run before main starts."),
    ("loop-var-prevents-capture-race", "loop-var-capture", "data-race-go", "prevents", "Per-iteration Loop variable capture prevents the Data race in Go caused by closures sharing a single loop iteration variable.", "Go 1.22+ compiler with module go version >= 1.22 in go.mod; the loop declares its iteration variable, each closure only reads its own captured variable and no explicit outer-variable assignment is used", "Shared pointees and variables declared outside the loop can still race; older language-version files retain the older rules."),
    ("escape-drives-gc-work", "escape-analysis", "heap-allocation-rate", "causes", "Escape analysis to heap causes Heap allocation rate to increase when executed values require additional heap allocations.", "Go 1.27 gc compiler; compared with the same workload using stack storage, retained escaping allocations execute repeatedly and are not eliminated", ""),
    ("select-multiplexes-receives", "select-statement", "channel-receive", "enables", "A Select statement enables one Channel receive to proceed from the available ready alternatives.", "Go 1; select has receive cases with at least one ready channel and chooses one ready communication", "If multiple cases are ready, select does not receive from all of them simultaneously."),
    ("buffer-holds-receives", "buffered-channel", "receive-blocking", "prevents", "A Buffered channel prevents Channel receive blocking when a queued value is available to that receive.", "Go 1; the buffer still contains an element at the moment the receive is performed", ""),
    ("stuck-send-stalls-goroutine", "channel-send", "goroutine-leak", "causes", "A Channel send causes a Goroutine leak when it remains blocked after its useful work should have ended.", "Go 1; a live program leaves a worker sending forever on an open unbuffered channel with no future receiver or cancellation alternative", ""),
    ("waitgroup-prevents-early-exit", "wait-group", "early-main-return", "prevents", "WaitGroup completion prevents Early main return while registered workers still have unfinished work.", "Go 1 sync.WaitGroup; main calls Wait before returning, positive Add calls precede the wait and each worker calls Done only after finishing its required work", "A worker that never calls Done can make Wait block forever; WaitGroup does not resolve deadlock."),
    ("closed-channel-returns-zero", "channel-receive", "zero-values", "predicts", "Channel receive predicts Type zero values as the returned elements after a closed channel's buffer has drained.", "Go 1; the channel is closed and empty, so receive returns the element type's zero value immediately and the comma-ok result is false", "Buffered values sent before close are received first with ok true."),
    ("send-on-closed-panics", "channel-send", "panic-recover", "causes", "Channel send causes Panic and recover control flow when executed on a closed channel.", "Go 1; a send is actually executed on a closed channel, including a selected send case", "A closed receive case instead completes normally; recover is optional."),
    ("unrecovered-panic-kills-program", "unrecovered-panic", "program-termination", "causes", "An Unrecovered panic causes Program termination from panic when it reaches the top of its goroutine.", "Go 1; an active panic reaches the top of a goroutine after its deferred calls finish without recovery", ""),
    ("context-prevents-leaks", "context-cancel", "goroutine-leak", "prevents", "Context cancellation prevents a Goroutine leak when the worker responds by ending all waits and returning.", "Go 1.7+ context; every potentially indefinite worker wait observes Done and the worker exits on cancellation without launching untracked work", "Cancellation is cooperative and cannot force a non-cooperating goroutine to stop."),
    ("map-order-enables-variation", "map-random-order", "order-dependent-output", "enables", "Unspecified map iteration order enables Order-dependent output variation between traversals of unchanged entries.", "Go 1; a program derives output directly from map range order without sorting keys or using an order-independent operation", "Two traversals can coincidentally use the same order; variation is permitted rather than guaranteed."),
]

MYTHS = [
    ("map-iteration-stable", "Go map iteration order is stable", "The specification leaves order unspecified; runtime randomization does not guarantee a new order each time, so sort keys for reproducible output.", "map-random-order"),
    ("defer-runs-immediately", "defer runs its call right away", "The function value and arguments evaluate at defer registration, while the deferred invocation runs on function exit or panic unwinding.", "defer-stack"),
    ("goroutines-are-threads", "Every goroutine is an OS thread", "The gc runtime multiplexes goroutines onto OS threads; one goroutine is not inherently one permanent thread.", "scheduler-mn"),
    ("nil-interface-simple", "A nil pointer in an interface is a nil interface", "Boxing a typed nil pointer preserves its dynamic type, so the resulting interface does not compare equal to nil.", "nil-interface"),
    ("gc-stops-world", "Go's collector stops all application work throughout collection", "The gc collector has concurrent phases and shorter stop-the-world phases, so collection does not imply one continuous global pause.", "concurrent-gc"),
]

BOUNDARIES = [
    ("loop-var-version", "Loop variables depend on the module language version", "Per-iteration variables require a Go 1.22+ compiler and module go version >= 1.22 in go.mod, subject to per-file language-version selection; assigning to pre-existing variables with = still reuses them.", "loop-var-capture"),
    ("recover-same-goroutine", "Recover must run directly in the right deferred function", "recover only stops an active panic when called directly by a deferred function in that same goroutine; an ordinary helper call or another goroutine cannot recover it.", "panic-recover"),
    ("channels-not-always", "Channel transfer does not revoke aliases", "Sending a slice or pointer copies a descriptor or pointer, not the referenced data; ownership transfer is a program discipline, and both sides retaining access can still race.", "share-by-communicating"),
    ("zero-not-fully-usable", "Zero initialization does not make every operation valid", "A nil map permits reads but panics on writes, and communication on a nil channel blocks indefinitely unless a select chooses another case.", "zero-values"),
]

EXAMPLES = [
    ("worker-pool", "A worker pool", "main registers workers before launch, workers drain a jobs channel and call Done after processing, and main waits before returning so unfinished jobs are not abandoned by program exit.", ["goroutine", "buffered-channel", "wait-group", "early-main-return"]),
    ("timeout-select", "A timeout with select", "A worker selects between an unbuffered receive and ctx.Done; a canceled context makes the cancellation case ready even when no sender exists.", ["select-statement", "channel-receive", "context-cancel"]),
    ("http-handler-errors", "Returning a typed nil error", "If *MyError implements error, returning a nil *MyError as error makes err != nil; return an untyped nil error result to report success.", ["error-value", "multiple-returns", "nil-interface"]),
    ("append-in-loop", "Growing a slice in a loop", "With len(s) == cap(s), appending one element allocates a new backing array; an earlier slice view still refers to the old array, and the growth factor is not specified.", ["append-growth", "slice-backing", "escape-analysis"]),
]

CONTROLS = [
    ("channels-schedule-threads", "Channels allocate dedicated OS threads", "A channel operation must not be treated as requiring a dedicated OS thread per waiting goroutine."),
    ("defer-runs-during", "Deferred calls run at registration", "Registering defer must not be treated as immediately invoking the deferred function."),
    ("gc-prevents-races", "The garbage collector prevents data races", "The concurrent garbage collector must not be treated as synchronising application memory accesses."),
    ("nil-map-writes", "Writing to a nil map works", "A nil map must not be treated as accepting writes."),
]
