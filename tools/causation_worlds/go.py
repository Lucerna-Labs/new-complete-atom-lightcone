"""Go causation: goroutines, channels, scheduling, interfaces, errors, defers, slices."""

WORLD = "go-causation-v0"
PREFIX = "gol"
DOMAIN = "language-ecosystems"
SUBJECT = "language-ecosystems.go"
SOURCES = ["go-spec-127"]
SCOPE = "Everyday Go semantics: goroutines and channels, the scheduler, interfaces, error values, defer and panic, slices and maps, context"
ROOT_LABEL = "Go causation world"
ROOT_STATEMENT = "Root of the Go causation world: how channels, goroutines, implicit interfaces and value semantics cause Go programs to behave as they do."

CONCEPTS = [
    ("goroutine", "Goroutine launch", "A function running concurrently on a growable stack for a small cost.", []),
    ("channel-send", "Channel send", "Placing a value into a channel for another goroutine to take.", []),
    ("channel-receive", "Channel receive", "Taking a value from a channel, blocking until one arrives.", []),
    ("channel-blocking", "Unbuffered channel blocking", "An unbuffered channel parking the sender until a receiver arrives.", []),
    ("buffered-channel", "Buffered channel", "A channel with room to queue values before blocking.", []),
    ("channel-deadlock", "Channel deadlock", "Every goroutine stuck waiting on channel operations that can never finish.", []),
    ("select-statement", "Select statement", "Waiting on several channel operations at once and taking the ready one.", []),
    ("share-by-communicating", "Share memory by communicating", "Passing ownership through channels instead of locking shared data.", []),
    ("wait-group", "WaitGroup completion", "A counter that waits for a set of goroutines to report done.", []),
    ("mutex-protect", "Mutex protection", "A lock serialising access to shared state.", []),
    ("data-race-go", "Data race in Go", "Two goroutines touching the same memory with one writing, uncoordinated.", []),
    ("scheduler-mn", "M-N goroutine scheduling", "The runtime multiplexing many goroutines onto a few OS threads.", []),
    ("escape-analysis", "Escape analysis to heap", "The compiler deciding a value must live on the heap.", []),
    ("stack-allocation-go", "Stack allocation in Go", "Values living on a goroutine's stack, freed by a frame pop.", []),
    ("concurrent-gc", "Concurrent garbage collector", "Collection running mostly alongside the program.", []),
    ("implicit-interface", "Implicit interface satisfaction", "A type satisfying an interface just by having the methods.", []),
    ("nil-interface", "Nil interface versus nil pointer", "An interface holding a typed nil pointer still compares non-nil.", []),
    ("error-value", "Error value returns", "Failures reported as ordinary returned values.", []),
    ("multiple-returns", "Multiple return values", "A function handing back several values at once.", []),
    ("defer-stack", "Defer stack", "Deferred calls queued and run last-registered-first at function exit.", []),
    ("panic-recover", "Panic and recover", "A panic unwinding until a deferred recover stops it.", []),
    ("slice-backing", "Slice backing array", "The hidden array a slice views into.", []),
    ("append-growth", "Append reallocation", "Append moving the data to a bigger array when capacity runs out.", []),
    ("map-random-order", "Map iteration random order", "Map ranges visiting keys in a deliberately shuffled order.", []),
    ("embedding-composition", "Embedding composition", "Promoting an embedded type's methods to the outer type.", []),
    ("exported-capitals", "Exported capital naming", "Capitalised identifiers visible outside their package.", []),
    ("context-cancel", "Context cancellation", "A cancellation signal flowing down a call tree.", []),
    ("zero-values", "Zero values on declaration", "Every declaration starting at a usable zero value.", []),
    ("package-init", "Package initialisation order", "Init functions and imports running before main.", []),
    ("loop-var-capture", "Loop variable capture", "Whether loop-made closures capture one variable or one per iteration.", []),
]

RELATIONS = [
    ("goroutine-cheap-enables-scheduling", "goroutine", "scheduler-mn", "enables", "A cheap goroutine launch enables M-N goroutine scheduling to multiplex thousands onto few threads.", "many goroutines exist at once", ""),
    ("unbuffered-synchronizes", "channel-blocking", "channel-send", "causes", "Unbuffered channel blocking causes the channel send to wait for a ready receiver.", "the channel has no buffer", ""),
    ("receive-pairs-send", "channel-receive", "channel-send", "prerequisite", "A matching channel receive is a prerequisite for an unbuffered channel send to finish.", "the channel is unbuffered", ""),
    ("buffer-decouples", "buffered-channel", "channel-blocking", "inhibits", "A buffered channel inhibits unbuffered channel blocking until the buffer fills.", "the buffer has spare capacity", ""),
    ("no-receiver-deadlocks", "channel-send", "channel-deadlock", "causes", "A channel send with no matching channel receive causes a channel deadlock.", "every goroutine waits at once", ""),
    ("select-prevents-deadlock", "select-statement", "channel-deadlock", "prevents", "A select statement with a default case prevents a channel deadlock while probing several channels.", "at least one case must be able to proceed", ""),
    ("communicating-prevents-races", "share-by-communicating", "data-race-go", "prevents", "Share memory by communicating prevents a data race in Go by handing ownership through channels.", "only one goroutine holds a value at a time", ""),
    ("mutex-protects-state", "mutex-protect", "data-race-go", "prevents", "Mutex protection prevents a data race in Go around shared state.", "every access locks the same mutex", ""),
    ("waitgroup-orders-completion", "wait-group", "goroutine", "enables", "A WaitGroup completion counter enables every goroutine launch to be awaited before moving on.", "Add and Done calls stay balanced", ""),
    ("escape-inhibits-stack", "escape-analysis", "stack-allocation-go", "inhibits", "Failing escape analysis to heap inhibits stack allocation in Go for the captured value.", "a value outlives its frame", ""),
    ("stack-eases-gc", "stack-allocation-go", "concurrent-gc", "inhibits", "Stack allocation in Go inhibits concurrent garbage collector pressure for short-lived values.", "values die with their frame", ""),
    ("gc-keeps-running", "concurrent-gc", "goroutine", "enables", "A concurrent garbage collector enables goroutine launch-heavy programs to keep running during collection.", "the collector runs alongside mutators", ""),
    ("implicit-decouples", "implicit-interface", "embedding-composition", "enables", "Implicit interface satisfaction enables embedding composition without declaring dependencies.", "a type has the needed methods", ""),
    ("nil-box-surprise", "nil-interface", "error-value", "causes", "The nil interface versus nil pointer split causes error value returns of a typed nil to still be non-nil.", "a nil pointer is assigned to an interface", ""),
    ("errors-enable-returns", "error-value", "multiple-returns", "enables", "The error value returns pattern enables the multiple return values pattern of value plus error.", "a function can fail", ""),
    ("defer-enables-recover", "defer-stack", "panic-recover", "enables", "The defer stack enables panic and recover cleanup to run last-registered-first.", "a panic unwinds the stack", ""),
    ("recover-prevents-crash", "panic-recover", "goroutine", "prevents", "A deferred panic and recover pair prevents a panicking goroutine launch from killing the program.", "recover is deferred in the same goroutine", ""),
    ("slice-aliasing-races", "slice-backing", "data-race-go", "causes", "A shared slice backing array causes a data race in Go when two slices write the same cells.", "appends or writes overlap", ""),
    ("append-reallocates", "append-growth", "slice-backing", "causes", "A growing append reallocation causes the slice backing array to be replaced by a bigger one.", "capacity is exceeded", ""),
    ("embedding-promotes-methods", "embedding-composition", "implicit-interface", "enables", "Embedding composition enables implicit interface satisfaction through promoted methods.", "the embedded type has the methods", ""),
    ("export-prereq-interface", "exported-capitals", "implicit-interface", "prerequisite", "Exported capital naming is a prerequisite for implicit interface satisfaction outside the package.", "a method must be visible", ""),
    ("context-prevents-stuck-wait", "context-cancel", "channel-blocking", "prevents", "A propagated context cancellation prevents unbuffered channel blocking from waiting forever.", "a select watches the done channel", ""),
    ("zero-values-cause-nil-box", "zero-values", "nil-interface", "causes", "The zero values on declaration rule causes the nil interface versus nil pointer case before assignment.", "a pointer field is declared but not set", ""),
    ("package-init-prereq-main", "package-init", "goroutine", "prerequisite", "Completed package initialisation order is a prerequisite for goroutine launches in main.", "init graphs must finish first", ""),
    ("loop-var-prevents-capture-race", "loop-var-capture", "data-race-go", "prevents", "Per-iteration loop variable capture prevents the classic data race in Go of goroutines sharing one variable.", "Go 1.22 or later per-iteration variables", ""),
    ("errors-prevent-panic-flow", "error-value", "panic-recover", "prevents", "Checking error value returns prevents panic and recover control flow for expected failures.", "each call inspects its error", ""),
    ("ok-idiom-rests-on-zeros", "multiple-returns", "zero-values", "enables", "The multiple return values pair enables the value, ok idiom resting on the zero values on declaration rule.", "a map or type assertion is checked", ""),
    ("scheduler-runs-others", "scheduler-mn", "channel-blocking", "enables", "M-N goroutine scheduling enables another goroutine to run while unbuffered channel blocking waits.", "a goroutine blocks on a channel", ""),
    ("escape-drives-gc-work", "escape-analysis", "concurrent-gc", "causes", "Heavy escape analysis to heap traffic causes concurrent garbage collector work to grow.", "many values escape per request", ""),
    ("select-multiplexes-receives", "select-statement", "channel-receive", "enables", "A select statement enables simultaneous channel receive readiness across cases.", "several channels are ready", ""),
    ("buffer-holds-receives", "buffered-channel", "channel-receive", "inhibits", "A buffered channel inhibits the channel receive from blocking while the buffer holds items.", "the buffer is non-empty", ""),
    ("stuck-send-stalls-goroutine", "channel-send", "goroutine", "inhibits", "A forever-waiting channel send inhibits that goroutine launch from ever finishing.", "no receiver will ever come", ""),
    ("waitgroup-prevents-early-exit", "wait-group", "channel-deadlock", "prevents", "A balanced WaitGroup completion wait prevents a channel deadlock style early exit while workers still send.", "the main goroutine waits for Done", ""),
    ("nil-box-wraps-typed-nil", "nil-interface", "implicit-interface", "enables", "The nil interface versus nil pointer split enables implicit interface satisfaction to wrap typed nils.", "a concrete nil sits inside an interface", ""),
    ("append-enables-streaming", "append-growth", "share-by-communicating", "enables", "Amortised append reallocation enables share memory by communicating buffers to keep flowing.", "capacity doubles on growth", ""),
    ("closed-channel-returns-zero", "channel-receive", "zero-values", "causes", "A closed channel causes the channel receive to return immediately with the type's zero values on declaration.", "the sender closed the channel", ""),
    ("send-on-closed-panics", "channel-send", "channel-receive", "inhibits", "A channel send on a closed channel inhibits safe channel receive reasoning by panicking.", "a send hits a closed channel", ""),
    ("unrecovered-panic-kills-program", "panic-recover", "goroutine", "causes", "An unrecovered panic and recover event causes that goroutine launch to crash the program.", "no deferred recover exists", ""),
    ("escape-predicts-slice-life", "escape-analysis", "slice-backing", "predicts", "Escape analysis to heap predicts whether a slice backing array survives its frame.", "the slice is returned or escapes", ""),
    ("context-prevents-leaks", "context-cancel", "goroutine", "prevents", "A respected context cancellation prevents leaked goroutine launches from outliving their work.", "handlers check the done channel", ""),
]

MYTHS = [
    ("map-iteration-stable", "Go map iteration order is stable",
     "Map iteration random order is deliberate; sort keys when order matters.", "map-random-order"),
    ("defer-runs-immediately", "defer runs its call right away",
     "The defer stack runs at function exit, though arguments evaluate immediately.", "defer-stack"),
    ("goroutines-are-threads", "Every goroutine is an OS thread",
     "Thousands of goroutines multiplex onto a few threads by M-N goroutine scheduling.", "scheduler-mn"),
    ("nil-interface-simple", "A nil pointer in an interface is a nil interface",
     "The nil interface versus nil pointer split means the interface still compares non-nil.", "nil-interface"),
    ("gc-stops-world", "Go's collector stops the world constantly",
     "The concurrent garbage collector mostly runs alongside the program with short pauses.", "concurrent-gc"),
]

BOUNDARIES = [
    ("loop-var-version", "Loop variable semantics changed",
     "Before Go 1.22 one loop variable was shared; since then each iteration gets its own.", "loop-var-capture"),
    ("recover-same-goroutine", "Recover works only in the panicking goroutine",
     "A deferred panic and recover in another goroutine cannot stop a panic.", "panic-recover"),
    ("channels-not-always", "Not all sharing belongs on channels",
     "Plain mutex protection fits simple shared counters better than channel choreography.", "mutex-protect"),
]

EXAMPLES = [
    ("worker-pool", "A worker pool",
     "A fixed set of goroutines drains a buffered channel of jobs.",
     ["goroutine", "buffered-channel", "wait-group"]),
    ("timeout-select", "A timeout with select",
     "A select statement races work against a timer's channel receive.",
     ["select-statement", "channel-receive", "context-cancel"]),
    ("http-handler-errors", "HTTP handlers returning errors",
     "Handlers pass error value returns up as multiple return values instead of panicking.",
     ["error-value", "multiple-returns", "panic-recover"]),
    ("append-in-loop", "Growing a slice in a loop",
     "Repeated append reallocation ends with a fresh slice backing array far from the first.",
     ["append-growth", "slice-backing", "escape-analysis"]),
]

CONTROLS = [
    ("channels-schedule-threads", "Channels schedule OS threads",
     "A channel must not be treated as a thread scheduler."),
    ("defer-runs-during", "deferred calls run during the function",
     "The defer stack must not be treated as running inside the function body."),
    ("gc-prevents-races", "The garbage collector prevents data races",
     "The concurrent garbage collector must not be treated as synchronising access."),
    ("nil-map-writes", "Writing to a nil map works",
     "A nil map must not be treated as accepting writes."),
]
