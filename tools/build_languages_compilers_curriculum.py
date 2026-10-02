#!/usr/bin/env python3
"""Author compiler foundations and versioned modern-language ecosystem profiles."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "languages-compilers" / "foundations.jsonl"
WORLD = "languages-compilers-v0"
COMPILER_LANES = ["reasoning.deductive", "thinking.bottom_up", "geometry.structural"]
LANGUAGE_LANES = ["thinking.bottom_up", "reasoning.deductive", "creativity.constraint_based"]
COMPILER_SOURCES = ["llvm-langref", "rust-book", "go-spec-127", "ecmascript-2026"]


COMPILER = [
    ("root", "Programming-language implementation pipeline", "A language implementation maps source programs through syntax, static and dynamic semantics, intermediate representations, transformation, code generation, linking, loading, runtime services, and tools while preserving declared observable behavior.", "programming-languages-compilers.syntax-semantics"),
    ("source-text", "Source text", "Source text is a sequence of encoded characters interpreted under a language version, lexical grammar, normalization policy, and file/module context.", "programming-languages-compilers.syntax-semantics"),
    ("grammar", "Grammar", "A grammar defines which token or character sequences form syntactic constructs, independently of whether those constructs are semantically valid.", "programming-languages-compilers.syntax-semantics"),
    ("static-semantics", "Static semantics", "Static semantics defines compile-time constraints and derived properties such as binding, typing, definite assignment, and control-flow validity.", "programming-languages-compilers.syntax-semantics"),
    ("dynamic-semantics", "Dynamic semantics", "Dynamic semantics defines how valid programs evaluate, transition state, interact with a host, and produce observable effects.", "programming-languages-compilers.syntax-semantics"),
    ("undefined-behavior", "Undefined behavior", "Undefined behavior removes requirements on an execution after specified preconditions are violated and must not be treated as a predictable implementation extension.", "programming-languages-compilers.syntax-semantics"),
    ("unspecified-behavior", "Unspecified behavior", "Unspecified behavior permits an implementation to choose among documented possibilities without requiring the choice to be recorded each time.", "programming-languages-compilers.syntax-semantics"),
    ("implementation-defined", "Implementation-defined behavior", "Implementation-defined behavior permits a choice that the implementation must document for its version and target.", "programming-languages-compilers.syntax-semantics"),
    ("observable-behavior", "Observable behavior", "Observable behavior is the language-defined projection of execution that conforming transformations must preserve under stated assumptions.", "programming-languages-compilers.syntax-semantics"),
    ("binding", "Name binding", "Name binding associates an identifier occurrence with a declaration or entity according to scope, namespace, shadowing, import, and overload rules.", "programming-languages-compilers.syntax-semantics"),
    ("scope", "Lexical scope", "Lexical scope determines name visibility from program structure, while dynamic object lifetime and runtime call chains are separate relations.", "programming-languages-compilers.syntax-semantics"),
    ("evaluation-order", "Evaluation order", "Evaluation order determines which subexpressions and side effects occur first and must be distinguished from precedence, associativity, and source layout.", "programming-languages-compilers.syntax-semantics"),
    ("type", "Type", "A type classifies values or expressions and constrains supported operations, representations, effects, or proofs according to a particular type system.", "programming-languages-compilers.type-systems"),
    ("static-type", "Static type", "A static type is assigned or inferred before execution and may approximate a broader set than the value observed at runtime.", "programming-languages-compilers.type-systems"),
    ("dynamic-type", "Dynamic type", "A dynamic type is the runtime classification governing an actual value's representation or operations.", "programming-languages-compilers.type-systems"),
    ("type-safety", "Type safety", "Type safety states that well-typed programs avoid a declared class of invalid operations under the language's semantics, not every software defect.", "programming-languages-compilers.type-systems"),
    ("subtyping", "Subtyping", "A subtype can be used where a supertype is expected under the language's substitutability and variance rules.", "programming-languages-compilers.type-systems"),
    ("variance", "Type variance", "Variance describes how a type constructor preserves, reverses, or rejects subtyping relationships among its arguments.", "programming-languages-compilers.type-systems"),
    ("parametric-polymorphism", "Parametric polymorphism", "Parametric polymorphism defines behavior uniformly over type parameters subject to declared bounds or capabilities.", "programming-languages-compilers.type-systems"),
    ("ad-hoc-polymorphism", "Ad-hoc polymorphism", "Ad-hoc polymorphism selects behavior through overloads, protocols, traits, type classes, or dispatch according to language rules.", "programming-languages-compilers.type-systems"),
    ("inference", "Type inference", "Type inference solves constraints to derive types omitted from source, within a decidable and implementation-bounded fragment.", "programming-languages-compilers.type-systems"),
    ("effect-system", "Effect system", "An effect system tracks selected computational effects such as mutation, exceptions, I/O, async work, or capability use in static judgments.", "programming-languages-compilers.type-systems"),
    ("ownership-type", "Ownership and borrowing", "Ownership and borrowing encode authority over resource use and aliases so lifetime and mutation constraints can be checked statically or dynamically.", "programming-languages-compilers.type-systems"),
    ("token", "Lexical token", "A token is a classified source span such as an identifier, keyword, literal, operator, or delimiter produced under lexical rules.", "programming-languages-compilers.parsing"),
    ("lexer", "Lexer", "A lexer transforms source characters into tokens while tracking spans, trivia, escapes, and lexical modes needed for diagnostics and parsing.", "programming-languages-compilers.parsing"),
    ("parser", "Parser", "A parser recognizes token structure under a grammar and constructs syntax while recovering or failing at invalid input according to tool goals.", "programming-languages-compilers.parsing"),
    ("cst", "Concrete syntax tree", "A concrete syntax tree preserves grammar and source-level punctuation or trivia needed for faithful formatting and transformation.", "programming-languages-compilers.parsing"),
    ("ast", "Abstract syntax tree", "An abstract syntax tree removes selected surface detail and represents semantically relevant program structure.", "programming-languages-compilers.parsing"),
    ("precedence", "Operator precedence", "Operator precedence groups an unparenthesized operator expression and does not determine runtime operand evaluation order by itself.", "programming-languages-compilers.parsing"),
    ("associativity", "Operator associativity", "Associativity resolves repeated operators of the same precedence into a syntax tree and does not imply algebraic associativity.", "programming-languages-compilers.parsing"),
    ("parse-recovery", "Parse error recovery", "Parse recovery constructs bounded partial syntax and resumes at synchronization points so one error does not create an uncontrolled cascade.", "programming-languages-compilers.parsing"),
    ("source-span", "Source span", "A source span maps a token, syntax node, semantic entity, diagnostic, or generated instruction back to a versioned source range.", "programming-languages-compilers.parsing"),
    ("ir", "Intermediate representation", "An intermediate representation encodes program operations and structure for analysis and transformation at a chosen abstraction level.", "programming-languages-compilers.ir"),
    ("ssa", "Static single assignment", "SSA gives each virtual definition one assignment and connects uses through explicit values and control-flow joins.", "programming-languages-compilers.ir"),
    ("basic-block", "Basic block", "A basic block is a maximal straight-line instruction sequence with one entry and control transfer only at its boundary.", "programming-languages-compilers.ir"),
    ("cfg", "Control-flow graph", "A control-flow graph represents basic blocks as nodes and possible control transfers as directed edges.", "programming-languages-compilers.ir"),
    ("dominator", "Dominator", "A block dominates another when every entry-to-target path includes it, supporting SSA construction and control analysis.", "programming-languages-compilers.ir"),
    ("phi", "SSA phi node", "A phi node selects the incoming SSA value corresponding to the control-flow predecessor at a join.", "programming-languages-compilers.ir"),
    ("def-use", "Def-use chain", "A def-use chain connects each value definition to the operations that consume it and supports data-flow analysis and transformation.", "programming-languages-compilers.ir"),
    ("call-graph", "Call graph", "A call graph approximates possible call relationships under dynamic dispatch, indirect calls, reflection, and separate compilation limits.", "programming-languages-compilers.ir"),
    ("lowering", "IR lowering", "Lowering transforms operations into more target-specific or primitive forms while preserving required semantics and metadata.", "programming-languages-compilers.ir"),
    ("pass", "Compiler pass", "A compiler pass analyzes or transforms one representation under declared prerequisites, preserved analyses, and verification conditions.", "programming-languages-compilers.optimization"),
    ("dataflow", "Data-flow analysis", "Data-flow analysis computes facts over a control-flow graph to a fixed point using transfer and merge functions.", "programming-languages-compilers.optimization"),
    ("constant-fold", "Constant folding", "Constant folding evaluates compile-time-known operations only when target semantics, overflow, exceptions, floating point, and side effects permit it.", "programming-languages-compilers.optimization"),
    ("dead-code", "Dead-code elimination", "Dead-code elimination removes operations whose results and effects cannot influence observable behavior under the analysis assumptions.", "programming-languages-compilers.optimization"),
    ("inlining", "Function inlining", "Inlining substitutes a callee body at a call site and trades call overhead and optimization context against code size, compilation time, and instruction-cache pressure.", "programming-languages-compilers.optimization"),
    ("loop-transform", "Loop transformation", "Loop transformations change iteration structure to improve locality, parallelism, or overhead while preserving dependences and exceptional behavior.", "programming-languages-compilers.optimization"),
    ("alias-analysis", "Alias analysis", "Alias analysis approximates which memory references may designate the same storage and therefore which reordering is safe.", "programming-languages-compilers.optimization"),
    ("escape-analysis", "Escape analysis", "Escape analysis determines whether a value can outlive or become reachable outside a region, call, thread, or allocation context.", "programming-languages-compilers.optimization"),
    ("vectorization", "Vectorization", "Vectorization transforms scalar operations into data-parallel instructions when dependences, alignment, exceptions, and target capabilities permit it.", "programming-languages-compilers.optimization"),
    ("pgo", "Profile-guided optimization", "Profile-guided optimization uses workload observations to guide layout and transformations, so representativeness and profile-version identity qualify the result.", "programming-languages-compilers.optimization"),
    ("proof-obligation", "Optimization proof obligation", "An optimization is valid only if every changed execution preserves the language's required observable behavior under stated preconditions.", "programming-languages-compilers.optimization"),
    ("instruction-selection", "Instruction selection", "Instruction selection maps IR operations and patterns to target instructions under legality, cost, feature, and calling-convention constraints.", "programming-languages-compilers.codegen"),
    ("register-allocation", "Register allocation", "Register allocation assigns live values to finite machine registers and inserts spills or reloads when simultaneous demand exceeds capacity.", "programming-languages-compilers.codegen"),
    ("calling-convention", "Calling convention", "A calling convention defines argument and return locations, register preservation, stack layout, alignment, unwinding, and symbol interaction across calls.", "programming-languages-compilers.codegen"),
    ("machine-code", "Machine code", "Machine code is an encoded instruction and data stream for a target ISA under platform ABI and relocation assumptions.", "programming-languages-compilers.codegen"),
    ("object-file", "Object file", "An object file contains code, data, symbols, relocations, sections, and metadata awaiting or supporting linking and loading.", "programming-languages-compilers.codegen"),
    ("debug-info", "Debug information", "Debug information maps optimized machine state to source entities imperfectly because variables, frames, and control can be transformed or eliminated.", "programming-languages-compilers.codegen"),
    ("symbol", "Linker symbol", "A symbol names code or data with binding, visibility, version, section, and resolution attributes.", "programming-languages-compilers.linkers-loaders"),
    ("relocation", "Relocation", "A relocation records how an address-dependent field must be adjusted when symbol and section locations become known.", "programming-languages-compilers.linkers-loaders"),
    ("static-link", "Static linking", "Static linking resolves and copies required object code into a final artifact under archive selection and symbol rules.", "programming-languages-compilers.linkers-loaders"),
    ("dynamic-link", "Dynamic linking", "Dynamic linking resolves shared-library dependencies at load time or lazily according to platform search, symbol, version, and relocation rules.", "programming-languages-compilers.linkers-loaders"),
    ("loader", "Program loader", "A loader maps executable segments, applies required relocations, establishes runtime state, and transfers control to an entry sequence.", "programming-languages-compilers.linkers-loaders"),
    ("abi", "Application binary interface", "An ABI defines binary contracts for data layout, calls, symbols, exceptions, object format, system interfaces, and platform conventions.", "programming-languages-compilers.linkers-loaders"),
    ("odr", "Definition consistency", "Separate compilation requires language-specific consistency rules so independently compiled declarations and definitions agree when linked.", "programming-languages-compilers.linkers-loaders"),
    ("runtime", "Language runtime", "A language runtime supplies execution services such as allocation, type metadata, exceptions, scheduling, reflection, dynamic loading, and foreign calls.", "programming-languages-compilers.runtime-gc"),
    ("allocation", "Runtime allocation", "Allocation reserves storage with size, alignment, lifetime, initialization, ownership, and failure behavior defined by language and runtime.", "programming-languages-compilers.runtime-gc"),
    ("tracing-gc", "Tracing garbage collection", "A tracing collector begins from roots, discovers reachable objects, and reclaims unreachable storage under pause, movement, and concurrency policies.", "programming-languages-compilers.runtime-gc"),
    ("reference-count", "Reference counting", "Reference counting reclaims an object when tracked strong references reach zero but needs additional handling for cycles and concurrency.", "programming-languages-compilers.runtime-gc"),
    ("stack-unwind", "Stack unwinding", "Stack unwinding transfers control across frames while running required cleanup and using platform exception metadata.", "programming-languages-compilers.runtime-gc"),
    ("memory-model", "Language memory model", "A memory model defines which inter-thread reads and writes are data races, synchronized, ordered, atomic, or observable.", "programming-languages-compilers.runtime-gc"),
    ("safepoint", "Runtime safepoint", "A safepoint is an execution state where the runtime can reliably inspect or suspend managed threads for collection, deoptimization, or coordination.", "programming-languages-compilers.runtime-gc"),
    ("jit", "Just-in-time compilation", "A JIT compiler translates or specializes code during execution using observed types and profiles under latency, memory, and deoptimization constraints.", "programming-languages-compilers.jit"),
    ("tiering", "JIT tiering", "Tiering begins with fast low-optimization execution and promotes hot code to more expensive optimized forms using runtime evidence.", "programming-languages-compilers.jit"),
    ("speculation", "Speculative optimization", "Speculative optimization assumes a guarded runtime property and records a recovery path when the guard fails.", "programming-languages-compilers.jit"),
    ("deoptimization", "Deoptimization", "Deoptimization reconstructs a less optimized execution state when speculative assumptions fail or debugging requires it.", "programming-languages-compilers.jit"),
    ("ffi", "Foreign-function interface", "An FFI maps calls, types, ownership, errors, threading, callbacks, and lifetimes across language and ABI boundaries.", "programming-languages-compilers.ffi-abi"),
    ("marshalling", "Marshalling", "Marshalling transforms values across representation or process boundaries and must preserve schema, ownership, encoding, and error semantics.", "programming-languages-compilers.ffi-abi"),
    ("unsafe-boundary", "Unsafe language boundary", "An unsafe boundary admits operations the compiler cannot fully validate and requires a documented invariant around the smallest possible scope.", "programming-languages-compilers.ffi-abi"),
    ("lsp", "Language Server Protocol role", "A language server derives diagnostics, completion, navigation, and refactoring from versioned document state through an editor protocol.", "programming-languages-compilers.tooling"),
    ("formatter", "Source formatter", "A formatter maps valid or recoverable syntax to a stable layout while preserving program semantics and selected comments.", "programming-languages-compilers.tooling"),
    ("linter", "Linter", "A linter reports patterns associated with defects, portability, security, or maintainability under configurable rules and false-positive tradeoffs.", "programming-languages-compilers.tooling"),
    ("debugger", "Debugger", "A debugger controls execution and inspects state through runtime and debug metadata whose relationship to optimized source may be incomplete.", "programming-languages-compilers.tooling"),
    ("build-system", "Language build system", "A build system resolves modules and dependencies into a task graph with declared inputs, outputs, target, profile, caching, and reproducibility behavior.", "programming-languages-compilers.tooling"),
    ("package-manager", "Package manager", "A package manager resolves version and platform constraints, verifies sources and hashes, and records a reproducible dependency solution.", "programming-languages-compilers.tooling"),
]


# Root names for languages whose bare name is also an everyday English word, so
# the word alone never becomes a seed term for the language.
ROOT_NAMES = {
    "go": ("Go programming language", ["golang", "go language"]),
}


# Each profile is version-scoped and intentionally separates language semantics
# from one compiler, runtime, package registry, or host platform.
LANGUAGES = [
    ("rust", "Rust", "language-ecosystems.rust", "rust-book",
     "Rust is a statically typed systems language whose ownership and borrowing rules constrain aliasing and resource lifetime without requiring tracing garbage collection.",
     "Rust combines algebraic data types, traits, generics, pattern matching, inference, lifetimes, and explicit unsafe boundaries.",
     "Values have ownership and deterministic drop behavior; reference validity and permitted mutation are checked through borrowing except inside justified unsafe code.",
     "Threads, channels, async futures, Send and Sync bounds, atomics, and synchronization express concurrency while data-race freedom depends on all unsafe implementations preserving invariants.",
     "Cargo resolves packages and features, invokes rustc across target profiles, runs tests and documentation, and records dependency versions in a lockfile.",
     "FFI uses platform ABIs and unsafe contracts; panics, Results, Options, allocator ownership, layout, and unwinding must be declared at boundaries."),
    ("go", "Go", "language-ecosystems.go", "go-spec-127",
     "Go is a statically typed, garbage-collected language organized into packages with explicit support for concurrent programming.",
     "Go uses nominal defined types, structural interfaces, inference, generics with constraints, multiple results, and explicit conversion rules.",
     "The runtime manages heap storage with garbage collection while values, pointers, slices, maps, interfaces, and channels have distinct representation and alias behavior.",
     "Goroutines and channels coordinate concurrent work, but shared memory still requires synchronization and goroutine lifetime must have an owner.",
     "The go command resolves modules, builds packages, tests, formats, vets, and produces binaries under a declared Go language and toolchain version.",
     "Errors are ordinary values, panic and recover serve different control boundaries, and cgo crosses an expensive ownership and runtime boundary."),
    ("swift", "Swift", "language-ecosystems.swift", "swift-language-guide",
     "Swift is a statically typed language combining value and reference types, protocol-oriented abstraction, optionals, generics, and memory-safe defaults for Apple and other platforms.",
     "Swift types include structures, classes, enumerations, protocols, generics, existentials, opaque results, optionals, and pattern matching with inference.",
     "Automatic reference counting manages class instances while value types, ownership features, closures, and unsafe pointers retain explicit lifetime and cycle considerations.",
     "Async functions, tasks, task groups, actors, Sendable checking, and cancellation support structured concurrency with reentrancy and isolation rules.",
     "Swift Package Manager and Xcode build modules and targets through swiftc, platform SDKs, conditional compilation, tests, and signed application products.",
     "Throwing errors, optionals, Objective-C interoperability, C ABI calls, reference cycles, and actor isolation require distinct boundary handling."),
    ("python", "Python", "language-ecosystems.python", "python-language-314",
     "Python is a dynamically typed language whose reference defines syntax and core semantics separately from implementation details such as CPython object layout.",
     "Python names bind objects dynamically; annotations and static checkers add optional analysis but do not by themselves enforce runtime types.",
     "Object lifetime is implementation-dependent; CPython uses reference counting plus cycle collection while context managers express deterministic cleanup protocols.",
     "Threads, processes, asyncio tasks, subinterpreters, and native extensions have different parallelism, cancellation, serialization, and interpreter-lock boundaries.",
     "Imports construct a module graph; virtual environments and packaging metadata resolve distributions, while bytecode and native extension behavior depend on implementation and ABI.",
     "Exceptions, iterators, generators, context managers, descriptors, metaclasses, and the Python C API define powerful dynamic boundaries that require explicit contracts."),
    ("c", "C", "language-ecosystems.c", "c23-wg14",
     "C is a compiled systems language with direct object representation, pointer arithmetic, separate translation, implementation-defined choices, and specified undefined behavior.",
     "C types include arithmetic, pointer, array, function, structure, union, enumeration, qualified, atomic, and incomplete types under conversion and compatibility rules.",
     "Storage duration, effective type, alignment, provenance, allocation, lifetime, and manual release govern memory correctness.",
     "C atomics and threads expose a formal memory model; data races, signal handlers, and library thread safety require strict constraints.",
     "Preprocessing, translation units, compilation, object generation, and platform linking produce executables or libraries under a selected implementation and ABI.",
     "Return codes, errno, long jumps, variadic functions, foreign calls, and unchecked pointer operations require defensive contracts because the type system cannot enforce all invariants."),
    ("cpp", "C++", "language-ecosystems.cpp", "cpp-standard",
     "C++ is a statically typed multi-paradigm systems language with deterministic object lifetime, templates, classes, value semantics, exceptions, and a large versioned standard library.",
     "C++ combines nominal classes, structural template constraints, overload resolution, concepts, deduction, references, value categories, and compile-time evaluation.",
     "RAII ties resource lifetime to object lifetime while raw pointers, ownership cycles, allocators, placement, and undefined behavior retain explicit risk.",
     "Threads, atomics, mutexes, futures, coroutines, and execution facilities operate under the C++ memory model and require race-free lifetime coordination.",
     "Preprocessing, modules or headers, templates, translation units, object files, and ABI-specific linking make build identity and one-definition consistency critical.",
     "Exceptions, error codes, expected-like values, templates, C interoperability, name mangling, ABI compatibility, and compiler extensions must be separated at interfaces."),
    ("csharp", "C Sharp and .NET", "language-ecosystems.csharp", "csharp-language-spec",
     "C Sharp is a statically typed managed language targeting the Common Language Infrastructure with object, generic, functional, asynchronous, and low-level facilities.",
     "Its type system includes value and reference types, nullable analysis, generics, interfaces, delegates, records, pattern matching, variance, and dynamic binding.",
     "The .NET runtime garbage collects managed objects while IDisposable and using statements govern deterministic external-resource cleanup; unsafe and native memory remain explicit.",
     "Tasks, async and await, threads, channels, synchronization, and the CLI memory model distinguish asynchronous progress from parallel execution.",
     "The .NET SDK and MSBuild resolve projects, packages, target frameworks, analyzers, source generators, tests, IL, ahead-of-time or JIT compilation, and deployment artifacts.",
     "Exceptions, cancellation tokens, nullable contracts, reflection, P/Invoke, COM, and runtime version compatibility define important boundaries."),
    ("java", "Java and JVM", "language-ecosystems.java", "java-se25-spec",
     "Java is a statically typed language compiled to class files for the JVM, with garbage collection, nominal classes and interfaces, generics, exceptions, and a formal memory model.",
     "Java types include primitives, classes, interfaces, arrays, type variables, parameterized types, records, sealed types, and pattern constructs under erasure and conversion rules.",
     "The JVM manages object storage while try-with-resources closes external resources; reachability, finalization alternatives, and native handles remain distinct.",
     "Threads, virtual threads, executors, futures, synchronization, volatile fields, and atomics interact under happens-before rules.",
     "javac produces class files; module and class paths, build tools, artifacts, JVM verification, class loading, JIT compilation, and target runtime versions shape execution.",
     "Checked and unchecked exceptions, erasure, reflection, serialization, JNI, class-loader identity, and binary compatibility require explicit interface design."),
    ("kotlin", "Kotlin", "language-ecosystems.kotlin", "kotlin-documentation",
     "Kotlin is a statically typed language with null safety, extension functions, algebraic-style sealed hierarchies, coroutines, and targets including JVM, native, JavaScript, and WebAssembly.",
     "Kotlin combines nullable types, generics, variance, smart casts, interfaces, data classes, sealed types, function types, and multiplatform expect-actual declarations.",
     "Memory and lifetime follow the selected target runtime; JVM collection, Kotlin Native management, resources, and interop references have distinct rules.",
     "Coroutines, suspend functions, flows, structured scopes, dispatchers, and cancellation express asynchronous concurrency over target-specific threads and event loops.",
     "Gradle and the Kotlin compiler coordinate source sets, plugins, dependencies, target backends, metadata, tests, and multiplatform artifacts.",
     "Exceptions, null platform types, Java interop, native interop, JavaScript exports, and cross-target API differences require explicit boundary contracts."),
    ("javascript", "JavaScript", "language-ecosystems.javascript", "ecmascript-2026",
     "JavaScript is the common implementation of ECMAScript, a dynamically typed language whose core semantics execute within host environments such as browsers and servers.",
     "Values have runtime types; objects use prototype chains and property descriptors, while coercion, equality, lexical bindings, closures, and modules follow specification algorithms.",
     "Garbage collection is host implementation behavior; object reachability, weak references, external resources, typed buffers, and host handles have different lifetimes.",
     "Promises and async functions schedule jobs; workers or host threads provide parallelism, and shared memory uses atomics under the ECMAScript memory model.",
     "Modules form URL or host-resolved graphs; engines parse, interpret or JIT code while package managers and bundlers add non-language resolution layers.",
     "Thrown values, promise rejection, host APIs, prototype mutation, proxies, realms, native addons, and runtime validation define dynamic boundaries."),
    ("typescript", "TypeScript", "language-ecosystems.typescript", "typescript-handbook",
     "TypeScript adds an erasable structural static type system and source syntax to JavaScript while intentionally preserving JavaScript runtime behavior.",
     "Its types include unions, intersections, generics, conditional and mapped types, narrowing, structural compatibility, any, unknown, never, and declaration merging.",
     "TypeScript introduces no independent runtime memory model because emitted JavaScript and the selected host govern values and resources.",
     "Async and concurrency behavior follows emitted JavaScript and host APIs; static types do not make effects, races, or external inputs safe automatically.",
     "tsc checks projects and emits JavaScript or declarations under tsconfig options; module resolution, build references, bundlers, and runtime targets remain separate layers.",
     "Types are erased, so JSON, DOM, database, and foreign data require runtime validation; declaration files can be wrong despite successful compilation."),
    ("dart", "Dart and Flutter", "language-ecosystems.dart", "dart-language",
     "Dart is a soundly typed language with classes, mixins, extensions, generics, null safety, asynchronous constructs, and JIT and ahead-of-time implementations used prominently by Flutter.",
     "Dart supports inferred static types, nullable types, generics, records, patterns, extension methods and types, and class-based interfaces.",
     "Managed objects are garbage collected while external resources and native handles require explicit lifecycle; isolates do not share ordinary mutable heaps.",
     "Futures and streams express async work, and isolates provide concurrent execution through message passing and transferable data constraints.",
     "The Dart tool resolves packages, analyzes, formats, tests, compiles JIT or AOT targets, and coordinates Flutter assets and platform builds.",
     "Exceptions, async cancellation conventions, platform channels, FFI, generated bindings, and target-specific web or native behavior require boundary design."),
    ("zig", "Zig", "language-ecosystems.zig", "zig-language",
     "Zig is a compiled systems language emphasizing explicit control, compile-time execution, manual allocation, error unions, optionals, and cross-compilation.",
     "Zig types include integers with explicit widths, pointers with qualifiers, arrays, slices, structs, unions, optionals, error unions, comptime values, and inferred anonymous forms.",
     "Allocators are passed explicitly and resource cleanup uses defer or errdefer; undefined values, pointer alignment, and lifetime remain programmer obligations.",
     "Threads and atomics expose target concurrency, while async language facilities are version-sensitive and must not be assumed across releases.",
     "zig build and the compiler coordinate modules, target triples, optimization modes, C/C++ compilation, tests, linking, and reproducible cross-target artifacts.",
     "Error unions, optionals, panics, C ABI interoperability, translated headers, comptime execution, and unstable master behavior require versioned contracts."),
    ("ocaml", "OCaml", "language-ecosystems.ocaml", "ocaml-55-manual",
     "OCaml is a statically typed functional language with inference, algebraic data types, pattern matching, modules, objects, effects, and native or bytecode implementations.",
     "OCaml combines Hindley-Milner-style inference with parametric polymorphism, variants, records, GADTs, modules, functors, objects, and controlled mutation.",
     "The runtime garbage collects managed values while resources, finalizers, custom blocks, C pointers, and multicore domains require explicit lifetime care.",
     "Domains provide parallel execution; systhreads, effects, promises in libraries, atomics, and the memory model distinguish shared-memory and cooperative concurrency.",
     "ocamlc, ocamlopt, dune, opam, interfaces, compilation units, functors, and package constraints produce bytecode or native artifacts.",
     "Exceptions, result types, exhaustive pattern checks, C stubs, representation attributes, effect handlers, and compiler extensions define boundary risks."),
    ("haskell", "Haskell", "language-ecosystems.haskell", "haskell-2010-report",
     "Haskell is a statically typed non-strict functional language whose standard report defines pure expressions, algebraic data types, type classes, modules, and monadic I/O.",
     "Haskell uses parametric polymorphism, type inference, algebraic data types, type classes, newtypes, pattern matching, and language extensions beyond the 2010 report in common implementations.",
     "Managed values are garbage collected and laziness changes allocation and retention; external resources require bracketed or region-aware cleanup.",
     "Evaluation sparks, threads, software transactional memory, async libraries, and monadic effects depend on implementation extensions and runtime scheduling.",
     "GHC and Cabal or Stack resolve packages, compile modules and extensions, optimize lazy code, link native artifacts, and expose versioned package databases.",
     "Bottom values, partial functions, exceptions in lazy evaluation, unsafePerformIO, FFI, and extension-specific semantics require explicit containment."),
    ("scala", "Scala", "language-ecosystems.scala", "scala3-reference",
     "Scala 3 is a statically typed JVM language combining object-oriented and functional programming with algebraic types, contextual abstractions, metaprogramming, and Java interoperation.",
     "Scala types include classes, traits, unions, intersections, match types, opaque types, generics, variance, path-dependent types, givens, and extension methods.",
     "Memory and object lifetime follow JVM management while resources, lazy values, closures, and native interop need explicit lifecycle patterns.",
     "Futures and effect libraries express async work over JVM executors; shared state follows the Java memory model and library-specific structured concurrency.",
     "The Scala compiler, sbt or other build tools, JVM target, dependencies, macros, TASTy metadata, tests, and cross-version publishing shape artifacts.",
     "Exceptions, Option and Either, implicit resolution, binary compatibility, Java nulls, reflection, macros, and effect runtimes require careful boundaries."),
    ("elixir-erlang", "Elixir and Erlang", "language-ecosystems.elixir-erlang", "elixir-language",
     "Elixir and Erlang target the BEAM virtual machine and organize fault-tolerant concurrent systems around immutable data, isolated processes, messages, supervision, and hot-code-aware runtimes.",
     "Their dynamic types include tagged tuples, maps, lists, binaries, functions, atoms, and pattern matching; Elixir protocols and Erlang behaviors structure polymorphism.",
     "BEAM garbage collects per-process heaps, reducing shared-heap coupling while binaries, ETS, NIF resources, and message copies have distinct lifetime behavior.",
     "Lightweight processes communicate asynchronously through mailboxes; links, monitors, supervisors, selective receive, timeouts, and distribution determine failure propagation.",
     "Mix, Hex, rebar3, compilers, applications, releases, OTP behaviors, supervision trees, and upgrade metadata produce deployable BEAM systems.",
     "Errors, exits, throws, supervision restarts, mailbox growth, atoms, NIF blocking, node trust, and distributed ordering require explicit operational contracts."),
    ("ruby", "Ruby", "language-ecosystems.ruby", "ruby-language",
     "Ruby is a dynamically typed object language with classes, modules, blocks, closures, metaprogramming, exceptions, and multiple implementation runtimes.",
     "Ruby values are objects with dynamic method lookup; modules, mixins, refinements, singleton classes, pattern matching, and duck typing shape abstraction.",
     "Implementations garbage collect managed objects while external handles, finalizers, native extensions, and object retention require explicit resource control.",
     "Threads, fibers, ractors, event libraries, and processes provide different concurrency and isolation under implementation-specific locks and schedulers.",
     "RubyGems and Bundler resolve packages; implementations parse or compile Ruby, run tests, build native extensions, and lock dependency solutions.",
     "Exceptions, nil, open classes, method_missing, eval, native extensions, serialization, and implementation differences create dynamic boundaries."),
    ("php", "PHP", "language-ecosystems.php", "php-language",
     "PHP is a dynamically and gradually typed language commonly executed per request by a server runtime, with functions, classes, traits, namespaces, generators, attributes, and evolving type declarations.",
     "PHP types include scalar and compound values, classes, interfaces, unions, intersections, nullable types, literal forms, and runtime-enforced declarations under coercive or strict calls.",
     "Reference-counted values and cycle collection manage request memory while resources, persistent workers, extensions, streams, and globals need explicit lifecycle handling.",
     "Traditional request isolation differs from fibers, event-loop frameworks, process managers, and persistent application servers; shared external state still needs coordination.",
     "Composer resolves packages and autoloading; the PHP engine parses and compiles opcodes, optional JIT executes hot code, and deployment config shapes semantics.",
     "Errors, exceptions, warnings, type coercion, superglobals, file inclusion, serialization, database drivers, extensions, and runtime configuration require explicit boundaries."),
    ("lua", "Lua", "language-ecosystems.lua", "lua54-manual",
     "Lua 5.4 is a small dynamically typed embeddable language with first-class functions, tables, metatables, coroutines, lexical closures, and a C API.",
     "Lua values have runtime types; tables unify array and map roles, while metatables and metamethods customize operations and lookup.",
     "Lua uses automatic memory management and supports to-be-closed variables, while C userdata, registry references, finalizers, and allocator callbacks cross lifetime boundaries.",
     "Coroutines provide cooperative suspension within a state; host threads, multiple states, and C callbacks require implementation-specific synchronization.",
     "Lua source compiles to virtual-machine instructions; modules, package searchers, embedding hosts, bytecode compatibility, and C build settings define deployment.",
     "Errors use protected calls and long-jump-like runtime behavior; metatables, dynamic loading, C API stack discipline, and untrusted code require containment."),
    ("julia", "Julia", "language-ecosystems.julia", "julia-manual",
     "Julia is a dynamically typed technical-computing language using multiple dispatch, generic functions, type inference, metaprogramming, and LLVM-based JIT compilation.",
     "Julia's type system includes abstract and concrete parametric types, unions, tuples, invariance, dispatch signatures, and values that can also serve as types.",
     "Managed objects are garbage collected while arrays may alias storage, views retain parents, finalizers are nondeterministic, and C or GPU memory needs explicit ownership.",
     "Tasks, threads, distributed processes, channels, atomics, and accelerator kernels have distinct scheduling, memory, and data-movement boundaries.",
     "Pkg resolves project and manifest environments; Julia lowers and specializes methods through inference and LLVM, with precompilation and artifacts affecting startup and portability.",
     "Exceptions, missing and nothing, world age, type piracy, generated functions, ccall, binary artifacts, and numerical reproducibility require boundary discipline."),
    ("r", "R", "language-ecosystems.r", "r-language-definition",
     "R is a dynamically typed language for statistical computing with vectors, lists, functions, lazy promises, environments, formulae, attributes, and multiple object systems.",
     "R values carry runtime types and attributes; vectors recycle under rules, missing values differ from null, and S3, S4, and reference classes dispatch differently.",
     "Implementations garbage collect objects and often use copy-on-modify semantics, while external pointers, connections, large arrays, and native code require explicit care.",
     "Parallel packages use processes, clusters, futures, or threads in native libraries; random streams, serialization, and shared external systems determine reproducibility.",
     "Packages declare metadata, namespaces, R and native source, documentation, tests, dependencies, and compiled artifacts installed into versioned library trees.",
     "Conditions, warnings, errors, restarts, nonstandard evaluation, formulas, environments, native interfaces, locale, and numerical backends require explicit interpretation."),
    ("sql", "SQL dialects", "language-ecosystems.sql", "postgresql18-docs",
     "SQL is a family of declarative relational languages whose concrete types, syntax, transactions, optimization, and procedural extensions vary by database dialect and version.",
     "SQL values, rows, tables, domains, arrays, composites, null markers, collations, and implicit conversions follow dialect-specific type and three-valued-logic rules.",
     "Database storage is owned by the engine through pages, indexes, logs, caches, vacuum or collection, and transactional lifetime rather than application pointers.",
     "Concurrent transactions interact through isolation, locks, multiversion state, deadlock handling, serialization anomalies, and durability mechanisms.",
     "The database parses, rewrites, plans, optimizes, and executes statements; schemas, migrations, extensions, clients, and server configuration define the deployed language environment.",
     "Null semantics, parameter binding, transaction boundaries, search paths, privileges, time zones, collations, dynamic SQL, and dialect differences require explicit contracts."),
    ("shell", "Shell languages", "language-ecosystems.shell", "bash-manual",
     "Shell languages compose processes, redirections, expansions, pipelines, conditionals, functions, and environment state under syntax where quoting and exit status are semantic.",
     "Shell values are primarily strings and arrays with context-sensitive expansion; commands, functions, aliases, variables, and files occupy distinct namespaces and phases.",
     "Processes, file descriptors, temporary files, traps, working directories, subshells, and environment inheritance require explicit lifecycle and cleanup.",
     "Pipelines and background jobs create concurrent processes whose exit status, signals, waiting, ordering, and shared filesystem effects need coordination.",
     "The shell parses and expands commands at runtime; scripts depend on interpreter version, utilities, locale, filesystem, environment, and operating-system behavior.",
     "Quoting, word splitting, globbing, command substitution, eval, untrusted filenames, partial pipeline failure, and secret-bearing arguments are critical boundaries."),
    ("assembly", "Assembly languages", "language-ecosystems.assembly", "riscv-unprivileged",
     "Assembly languages expose symbolic forms of target instructions, registers, addressing, directives, labels, relocations, and ABI conventions for one architecture and toolchain.",
     "Operand widths, register classes, instruction encodings, privilege levels, extensions, and pseudo-instructions define target-specific validity rather than a portable type system.",
     "Memory correctness depends on explicit addresses, alignment, calling convention, stack discipline, protection, and the architecture's memory-order rules.",
     "Atomic instructions, fences, interrupts, privilege transitions, and device interactions expose hardware concurrency and ordering directly.",
     "An assembler produces object sections and relocations; linker scripts, ABI, loader, firmware, target features, and debug metadata determine the executable image.",
     "Inline assembly, syscalls, MMIO, calling convention, clobbers, relocation models, self-modifying code, and architecture versions require exact boundaries."),
    ("webassembly", "WebAssembly", "language-ecosystems.webassembly", "webassembly-core",
     "WebAssembly is a validated portable stack-machine binary format and execution model embedded by a host that supplies imports, resources, and external effects.",
     "Core value, reference, function, table, memory, tag, and module types are validated before instantiation under a versioned feature set.",
     "Linear memory is a bounded byte array distinct from host object memory; growth, aliasing, shared memory, garbage-collected references, and host buffers have separate rules.",
     "Threads proposals use shared memories and atomics, while async behavior is primarily host-mediated and may require stack switching or component abstractions.",
     "Toolchains lower source languages to modules, validate, optimize, link, componentize, and instantiate them with host imports and capability policy.",
     "Traps, imports, exports, linear-memory bounds, interface types, WASI capabilities, host calls, feature detection, and engine versions define boundaries."),
    ("solidity", "Solidity", "language-ecosystems.solidity", "solidity-language",
     "Solidity is a statically typed contract language compiled primarily for Ethereum virtual-machine execution under immutable deployed bytecode and transaction semantics.",
     "Solidity types include value and reference forms, mappings, arrays, structs, enums, contracts, function types, data locations, and explicit conversions.",
     "Storage, transient storage where supported, memory, calldata, stack, gas, and account state have distinct lifetime, cost, alias, and persistence rules.",
     "Transactions execute deterministically within blocks, while reentrant external calls, ordering, asynchronous confirmation, forks, and cross-contract state create concurrency-like hazards.",
     "solc compiles source and metadata to bytecode and ABI; optimizer settings, EVM version, libraries, deployment, verification, tests, and upgrade patterns define artifacts.",
     "Reverts, external calls, reentrancy, delegatecall, authorization, oracle input, integer behavior, upgrade storage layout, gas, and chain finality require defensive contracts."),
]


COMPILER_RELATIONS = [
    ("source-lexer", "comp.source-text", "comp.lexer", "transforms_to", "Lexical analysis transforms versioned source characters into tokens and spans."),
    ("grammar-parser", "comp.grammar", "comp.parser", "qualifies", "The grammar qualifies which token structures a parser accepts."),
    ("lexer-token", "comp.lexer", "comp.token", "causes", "A lexer produces classified token occurrences."),
    ("token-parser", "comp.token", "comp.parser", "prerequisite", "A token stream is prerequisite to token-based parsing."),
    ("parser-cst", "comp.parser", "comp.cst", "causes", "A concrete parser can produce a concrete syntax tree."),
    ("cst-ast", "comp.cst", "comp.ast", "transforms_to", "Syntax lowering transforms a concrete tree into an abstract syntax tree."),
    ("precedence-ast", "comp.precedence", "comp.ast", "qualifies", "Precedence qualifies the grouping represented by an abstract syntax tree."),
    ("associativity-ast", "comp.associativity", "comp.ast", "qualifies", "Associativity qualifies grouping among equal-precedence operators."),
    ("recovery-cst", "comp.parse-recovery", "comp.cst", "supports", "Parse recovery supports a bounded partial syntax tree for tooling."),
    ("span-diagnostic", "comp.source-span", "comp.ast", "supports", "Source spans support mapping semantic structure back to authored text."),
    ("ast-binding", "comp.ast", "comp.binding", "prerequisite", "Parsed declarations and references are prerequisite to name binding."),
    ("scope-binding", "comp.scope", "comp.binding", "qualifies", "Scope rules qualify the declaration associated with each name."),
    ("binding-static", "comp.binding", "comp.static-semantics", "part_of", "Resolved names form part of static semantic analysis."),
    ("type-static", "comp.type", "comp.static-semantics", "part_of", "Type judgments form part of static semantics."),
    ("static-dynamic", "comp.static-semantics", "comp.dynamic-semantics", "qualifies", "Static validity qualifies which programs receive defined dynamic evaluation."),
    ("evaluation-dynamic", "comp.evaluation-order", "comp.dynamic-semantics", "qualifies", "Evaluation-order rules qualify dynamic side-effect order."),
    ("observable-opt", "comp.observable-behavior", "comp.proof-obligation", "grounds", "Required observable behavior grounds optimization proof obligations."),
    ("undefined-observable", "comp.undefined-behavior", "comp.observable-behavior", "undercuts", "Undefined behavior undercuts claims about required observations after a violated precondition."),
    ("implementation-version", "comp.implementation-defined", "comp.dynamic-semantics", "qualifies", "Documented implementation choices qualify actual dynamic behavior."),
    ("static-type", "comp.static-type", "comp.type", "part_of", "Static type is one type-system classification."),
    ("dynamic-type", "comp.dynamic-type", "comp.type", "part_of", "Runtime type is one dynamic classification."),
    ("safety-type", "comp.type-safety", "comp.static-type", "qualifies", "A type-safety claim qualifies what well-typed programs cannot do."),
    ("subtype-variance", "comp.variance", "comp.subtyping", "qualifies", "Variance qualifies how constructed types participate in subtyping."),
    ("param-type", "comp.parametric-polymorphism", "comp.type", "implements", "Type parameters implement one form of reusable typed abstraction."),
    ("adhoc-type", "comp.ad-hoc-polymorphism", "comp.type", "implements", "Overload or capability selection implements ad-hoc polymorphism."),
    ("inference-static", "comp.inference", "comp.static-type", "causes", "Constraint solving derives static types for omitted annotations."),
    ("effect-static", "comp.effect-system", "comp.static-semantics", "part_of", "Effect judgments can form part of static semantics."),
    ("ownership-safety", "comp.ownership-type", "comp.type-safety", "supports", "Ownership rules support selected memory- and race-safety guarantees."),
    ("ast-ir", "comp.ast", "comp.ir", "transforms_to", "Semantic lowering transforms typed syntax into an intermediate representation."),
    ("ir-block", "comp.basic-block", "comp.ir", "part_of", "Basic blocks compose a control-flow intermediate representation."),
    ("block-cfg", "comp.basic-block", "comp.cfg", "part_of", "Basic blocks are nodes of a control-flow graph."),
    ("cfg-dominator", "comp.cfg", "comp.dominator", "prerequisite", "A control-flow graph is prerequisite to dominance computation."),
    ("ssa-defuse", "comp.ssa", "comp.def-use", "enables", "Single-assignment definitions enable direct def-use chains."),
    ("phi-ssa", "comp.phi", "comp.ssa", "part_of", "Phi nodes represent merged definitions in SSA."),
    ("dominator-ssa", "comp.dominator", "comp.ssa", "supports", "Dominance relations support SSA construction and verification."),
    ("callgraph-ir", "comp.call-graph", "comp.ir", "part_of", "A call graph is one interprocedural representation derived from program IR."),
    ("lowering-ir", "comp.lowering", "comp.ir", "transforms_to", "Lowering transforms higher-level IR into more target-specific IR."),
    ("pass-ir", "comp.pass", "comp.ir", "transforms_to", "A transformation pass maps one verified IR state to another."),
    ("dataflow-cfg", "comp.cfg", "comp.dataflow", "prerequisite", "The control-flow graph is prerequisite to many data-flow analyses."),
    ("alias-dead", "comp.alias-analysis", "comp.dead-code", "supports", "Alias analysis supports proving that memory operations have no observable use."),
    ("escape-allocation", "comp.escape-analysis", "comp.allocation", "qualifies", "Escape analysis qualifies whether storage can be stack, region, or heap allocated."),
    ("constant-proof", "comp.proof-obligation", "comp.constant-fold", "qualifies", "Target and language semantics qualify safe constant folding."),
    ("dead-observable", "comp.observable-behavior", "comp.dead-code", "qualifies", "Observable effects qualify which apparently unused operations can be removed."),
    ("inline-call", "comp.inlining", "comp.call-graph", "transforms_to", "Inlining transforms call relationships and exposes new optimization context."),
    ("loop-dataflow", "comp.dataflow", "comp.loop-transform", "supports", "Dependence analysis supports valid loop transformations."),
    ("vector-loop", "comp.loop-transform", "comp.vectorization", "enables", "A legal loop form enables vectorization."),
    ("pgo-pass", "comp.pgo", "comp.pass", "qualifies", "Profile evidence qualifies optimization and layout decisions."),
    ("ir-select", "comp.ir", "comp.instruction-selection", "prerequisite", "Lowered IR is prerequisite to target instruction selection."),
    ("select-machine", "comp.instruction-selection", "comp.machine-code", "transforms_to", "Instruction selection transforms operations toward machine instructions."),
    ("register-machine", "comp.register-allocation", "comp.machine-code", "qualifies", "Register allocation qualifies physical register and spill locations."),
    ("calling-code", "comp.calling-convention", "comp.machine-code", "qualifies", "Calling convention qualifies emitted call sequences and frame layout."),
    ("machine-object", "comp.machine-code", "comp.object-file", "part_of", "Encoded machine instructions form sections in an object file."),
    ("debug-span", "comp.source-span", "comp.debug-info", "supports", "Source spans support generation of debug line and entity mappings."),
    ("symbol-object", "comp.symbol", "comp.object-file", "part_of", "Symbols form part of object-file linking metadata."),
    ("reloc-object", "comp.relocation", "comp.object-file", "part_of", "Relocations form part of an object file."),
    ("object-static", "comp.object-file", "comp.static-link", "prerequisite", "Object files are inputs to static linking."),
    ("object-dynamic", "comp.object-file", "comp.dynamic-link", "prerequisite", "Shared object artifacts are inputs to dynamic linking."),
    ("abi-link", "comp.abi", "comp.dynamic-link", "qualifies", "ABI compatibility qualifies whether binary objects can link and call safely."),
    ("dynamic-loader", "comp.dynamic-link", "comp.loader", "part_of", "Dynamic resolution forms part of loading an executable process."),
    ("loader-runtime", "comp.loader", "comp.runtime", "causes", "The loader establishes process state and transfers control into runtime startup."),
    ("runtime-allocation", "comp.runtime", "comp.allocation", "implements", "The runtime implements managed or language-specific allocation services."),
    ("trace-allocation", "comp.tracing-gc", "comp.allocation", "qualifies", "Tracing collection qualifies managed object lifetime and movement."),
    ("refcount-allocation", "comp.reference-count", "comp.allocation", "qualifies", "Reference counts qualify reclamation of acyclic strongly referenced objects."),
    ("unwind-runtime", "comp.stack-unwind", "comp.runtime", "part_of", "Stack unwinding can form part of runtime exception handling."),
    ("memory-concurrency", "comp.memory-model", "comp.dynamic-semantics", "qualifies", "The memory model qualifies concurrent program observations."),
    ("safepoint-gc", "comp.safepoint", "comp.tracing-gc", "supports", "Safepoints support precise runtime inspection for collection."),
    ("jit-runtime", "comp.jit", "comp.runtime", "part_of", "Just-in-time compilation is one runtime execution service."),
    ("tier-jit", "comp.tiering", "comp.jit", "qualifies", "Tiering qualifies when execution moves to optimized JIT code."),
    ("spec-jit", "comp.speculation", "comp.jit", "enables", "Guarded runtime observations enable speculative JIT optimization."),
    ("deopt-spec", "comp.deoptimization", "comp.speculation", "prevents", "Deoptimization prevents a failed speculation from silently changing required semantics."),
    ("ffi-abi", "comp.abi", "comp.ffi", "prerequisite", "A compatible ABI is prerequisite to direct foreign calls."),
    ("marshal-ffi", "comp.marshalling", "comp.ffi", "part_of", "Representation conversion can form part of a foreign interface."),
    ("unsafe-ffi", "comp.unsafe-boundary", "comp.ffi", "qualifies", "An unsafe contract qualifies foreign calls the type system cannot validate."),
    ("lsp-span", "comp.source-span", "comp.lsp", "supports", "Versioned source spans support language-server edits and diagnostics."),
    ("formatter-cst", "comp.cst", "comp.formatter", "supports", "Concrete syntax supports semantics-preserving formatting with comments."),
    ("linter-static", "comp.static-semantics", "comp.linter", "supports", "Static semantic facts support linter diagnostics."),
    ("debug-info-debugger", "comp.debug-info", "comp.debugger", "supports", "Debug information supports mapping machine state to source."),
    ("build-package", "comp.package-manager", "comp.build-system", "supports", "A resolved package graph supports a reproducible build graph."),
]


CONTROL_SPECS = [
    ("compile-correct", "Successful compilation proves correctness", "A program compiling without diagnostics must not be treated as proof of functional correctness, safety, or requirement satisfaction."),
    ("type-input", "Static type validates external data", "A static type annotation must not substitute for runtime validation of untrusted bytes, JSON, database rows, or foreign values."),
    ("gc-resource", "Garbage collection closes resources", "Garbage collection must not be relied on for timely release of files, locks, sockets, transactions, or other external resources."),
    ("async-parallel", "Async means parallel", "Suspending asynchronous work must not be described as parallel execution without a scheduler and execution resources that actually run tasks concurrently."),
    ("lock-race", "Lock use eliminates races", "The presence of a lock must not establish race freedom unless every conflicting access follows the same synchronization protocol and lifetime."),
    ("optimizer-algebra", "Algebraic rewrite is always valid", "A mathematical identity must not justify compiler rewriting when overflow, floating point, exceptions, evaluation order, or side effects change observable behavior."),
    ("undefined-prediction", "Undefined behavior has stable output", "Observed compiler behavior after undefined behavior must not be promoted to a portable language guarantee."),
    ("precedence-order", "Precedence determines evaluation order", "Parser precedence must not be used to infer runtime operand evaluation order unless the language separately specifies it."),
    ("ir-source", "IR is identical to source", "An intermediate representation must not be treated as a lossless identity with source structure, types, or debugging state."),
    ("debug-optimized", "Debugger shows exact source state", "Optimized debug variables and control positions must not be treated as exact when transformations eliminate, merge, or move them."),
    ("abi-source", "Source compatibility implies ABI compatibility", "Source code continuing to compile must not prove existing binaries can link or exchange data safely."),
    ("package-name", "Package name proves provenance", "A registry name or matching version string must not establish artifact origin, integrity, maintainer identity, or safety."),
    ("lock-security", "Lockfile proves dependency safety", "A lockfile preserves a resolution but must not be treated as proof that dependencies are trustworthy or vulnerability-free."),
    ("ffi-safe", "FFI declaration makes call safe", "A foreign declaration must not establish layout, ownership, lifetime, threading, error, or unwinding correctness by itself."),
    ("benchmark-language", "One benchmark ranks languages", "One program and environment must not be used to rank whole languages without workload, implementation, optimization, expertise, and uncertainty boundaries."),
]


LANGUAGE_CONTROLS = {
    "rust": ("Unsafe Rust is unchecked permission", "An unsafe block permits specific unchecked operations but still requires every surrounding safety invariant to hold."),
    "go": ("Goroutine without owner", "A goroutine must not be launched without a completion, cancellation, error, and resource-ownership path."),
    "swift": ("Actor prevents stale state", "Actor isolation must not hide that state can change while an actor method is suspended at await."),
    "python": ("Annotation enforces runtime type", "A Python annotation must not be treated as runtime validation unless an explicit mechanism enforces it."),
    "c": ("Observed C behavior is defined", "One compiler's output must not establish defined C semantics after lifetime, bounds, alias, or other undefined-behavior violations."),
    "cpp": ("RAII prevents every leak", "RAII must not be treated as preventing ownership cycles, intentional release, global lifetime hazards, or foreign-resource mistakes."),
    "csharp": ("Async void is ordinary task", "An async void operation must not be treated as an awaitable task with ordinary error and completion propagation."),
    "java": ("Volatile makes compound update atomic", "A volatile field must not be treated as making a multi-step read-modify-write operation atomic."),
    "kotlin": ("Double bang proves non-null", "A non-null assertion must not be treated as evidence; it converts possible absence into a runtime failure."),
    "javascript": ("Promise catches synchronous caller", "Creating or returning a promise must not be assumed to catch errors thrown before the promise chain is established."),
    "typescript": ("TypeScript type exists at runtime", "An erased TypeScript type must not be used as runtime authorization or validation evidence."),
    "dart": ("Isolates share ordinary objects", "Ordinary mutable Dart objects must not be treated as shared state across isolates."),
    "zig": ("Undefined is a zero value", "Zig undefined must not be treated as initialized zero or safely readable storage."),
    "ocaml": ("Pattern warning is impossible case", "A non-exhaustive pattern warning must not be dismissed without proving the omitted runtime value cannot occur."),
    "haskell": ("Pure type proves termination", "A pure Haskell expression must not be assumed to terminate or avoid exceptions and bottom values."),
    "scala": ("Given resolution is obvious", "Contextual implicit resolution must not be treated as self-evident when scope and priority can change selected behavior."),
    "elixir-erlang": ("Restart repairs root cause", "A supervisor restart must not be treated as removing poisoned input, bad configuration, mailbox pressure, or persistent corruption."),
    "ruby": ("Duck typing validates protocol", "Responding to one method name must not establish the full behavioral protocol expected by a Ruby caller."),
    "php": ("Request validation persists globally", "Validation in one PHP request must not be assumed to govern later workers, jobs, or external state transitions."),
    "lua": ("Sandbox by removed globals", "Removing selected Lua globals must not be treated as a secure sandbox while metatables, loaders, debug hooks, C APIs, or resource exhaustion remain reachable."),
    "julia": ("Inferred type is language guarantee", "A Julia compiler's inferred type must not be treated as a stable public language contract across methods, worlds, and versions."),
    "r": ("Vector recycling is intended", "Silent or warned R vector recycling must not be accepted as intended alignment without checking dimensions and keys."),
    "sql": ("Query order without order by", "SQL result row order must not be treated as stable without an explicit ordering clause that uniquely resolves ties."),
    "shell": ("Quoted variable always one argument", "Shell quoting must account for arrays, empty values, expansions, and command context rather than assuming one scalar pattern covers every case."),
    "assembly": ("Instruction sequence is ABI-correct", "Valid assembly instructions must not be treated as a callable function until stack, clobber, alignment, unwind, and calling-convention rules hold."),
    "webassembly": ("WebAssembly module is harmless", "Validation of a WebAssembly module must not establish that granted host imports, resource use, or application logic are safe."),
    "solidity": ("Private state is secret", "A Solidity private declaration must not be treated as hiding on-chain storage from observers."),
}


WORKED_EXAMPLES = [
    ("comp", "precedence-order", "Precedence versus evaluation", "A parser groups multiplication inside addition, while a separate language rule determines which operand call executes first; the worked example records both trees and event order.", "programming-languages-compilers.syntax-semantics", COMPILER_LANES, COMPILER_SOURCES),
    ("comp", "ssa-join", "SSA join", "Two control-flow predecessors define different values; a join block uses one phi result selected by the actual predecessor, and later uses point only to that single definition.", "programming-languages-compilers.ir", COMPILER_LANES, COMPILER_SOURCES),
    ("comp", "constant-overflow", "Constant-folding boundary", "A candidate integer fold is accepted only after checking the target width and language overflow rule; a floating rewrite is rejected because it changes NaN or rounding behavior.", "programming-languages-compilers.optimization", COMPILER_LANES, COMPILER_SOURCES),
    ("comp", "ffi-buffer", "FFI buffer contract", "A foreign buffer contract records allocator, pointer and length, alignment, mutation authority, valid call duration, release function, callback threading, and error mapping.", "programming-languages-compilers.ffi-abi", COMPILER_LANES, COMPILER_SOURCES),
    ("lang", "rust-resource", "Rust resource boundary", "A Rust wrapper owns one foreign handle, closes it exactly once in Drop, marks the raw constructor unsafe, and converts foreign error codes into a Result.", "language-ecosystems.rust", LANGUAGE_LANES, ["rust-book"]),
    ("lang", "go-cancel", "Go goroutine cancellation", "A Go worker receives a context, selects on cancellation while sending results, closes only the channel it owns, and is joined before the request scope returns.", "language-ecosystems.go", LANGUAGE_LANES, ["go-spec-127"]),
    ("lang", "python-cleanup", "Python deterministic cleanup", "A Python context manager acquires a file and releases it in exit handling even when the body raises, instead of depending on garbage-collection timing.", "language-ecosystems.python", LANGUAGE_LANES, ["python-language-314"]),
    ("lang", "typescript-boundary", "TypeScript runtime boundary", "A TypeScript client receives unknown JSON, validates a discriminated schema at runtime, then narrows to a typed domain value instead of casting it.", "language-ecosystems.typescript", LANGUAGE_LANES, ["typescript-handbook"]),
    ("lang", "sql-transaction", "SQL transaction anomaly", "Two transactions read the same invariant and write disjoint rows; a serializable execution rejects one commit even though row locks alone did not reveal the predicate conflict.", "language-ecosystems.sql", LANGUAGE_LANES, ["postgresql18-docs"]),
    ("lang", "shell-array", "Shell argument preservation", "A shell script stores filenames in an array and expands each as one quoted argument, preserving spaces, glob characters, leading hyphens, and an empty list.", "language-ecosystems.shell", LANGUAGE_LANES, ["bash-manual"]),
    ("lang", "wasm-capability", "WebAssembly host capability", "A validated module receives only a bounded logging import and no filesystem or network capability, demonstrating that host imports determine external authority.", "language-ecosystems.webassembly", LANGUAGE_LANES, ["webassembly-core"]),
    ("lang", "solidity-reentrancy", "Solidity reentrancy state order", "A contract validates authority, records the withdrawal before the external call, limits reentry, and tests rollback behavior under a hostile owned fixture.", "language-ecosystems.solidity", LANGUAGE_LANES, ["solidity-language"]),
]


def split_for(index: int, *, root: bool = False) -> str:
    if root:
        return "train"
    if index % 37 == 0:
        return "cross_domain_holdout"
    if index % 29 == 0:
        return "sealed_test"
    if index % 19 == 0:
        return "validation"
    return "train"


def edge_split_for(index: int) -> str:
    if index and index % 31 == 0:
        return "cross_domain_holdout"
    if index and index % 23 == 0:
        return "sealed_test"
    if index and index % 17 == 0:
        return "validation"
    return "train"


def make_base(
    identifier: str,
    domain: str,
    subject: str,
    lanes: list[str],
    sources: list[str],
    split: str,
    kind: str,
    epistemic: str = "established",
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": identifier,
        "world_id": WORLD,
        "domain_id": domain,
        "subject_id": subject,
        "lanes": sorted(set(lanes)),
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"],
        "source_ids": sorted(set(sources)),
        "scope": "compiler pipeline and modern programming-language ecosystem foundation tranche",
        "limitations": [
            "Every language and toolchain statement is version-scoped; implementations, extensions, libraries, and targets continue to evolve.",
            "The registered ecosystem list is a mandatory initial set, not a closed inventory of programming languages.",
            "Compiler correctness and language conformance require stronger formal and differential evidence than this foundation alone supplies.",
        ],
        "as_of": "2026-09-03",
        "version_boundary": "languages-compilers-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", domain],
    }


def language_sources(language_id: str, source: str) -> list[str]:
    sources = [source]
    if language_id == "elixir-erlang":
        sources.append("erlang-reference")
    return sources


def build_relations() -> list[tuple[str, str, str, str, str]]:
    relations = list(COMPILER_RELATIONS)
    for language_id, _label, _subject, _source, _semantics, _types, _resources, _concurrency, _toolchain, _boundaries in LANGUAGES:
        root = f"lang.{language_id}.root"
        relations.extend(
            [
                (f"lang-{language_id}-types", f"lang.{language_id}.types", root, "qualifies", f"The {language_id} type system qualifies which programs and operations the language accepts."),
                (f"lang-{language_id}-resources", f"lang.{language_id}.resources", root, "qualifies", f"The {language_id} resource model qualifies lifetime and cleanup behavior."),
                (f"lang-{language_id}-concurrency", f"lang.{language_id}.concurrency", root, "qualifies", f"The {language_id} concurrency model qualifies ordering, isolation, cancellation, and failure propagation."),
                (f"lang-{language_id}-toolchain", f"lang.{language_id}.toolchain", "comp.build-system", "implements", f"The {language_id} toolchain implements language-specific build and package behavior."),
                (f"lang-{language_id}-boundary", f"lang.{language_id}.boundaries", "comp.ffi", "qualifies", f"The {language_id} boundary model qualifies error, interoperation, and unsafe transitions."),
                (f"lang-{language_id}-type-model", f"lang.{language_id}.types", "comp.type", "implements", f"The {language_id} type system implements one concrete language classification discipline."),
                (f"lang-{language_id}-runtime-model", f"lang.{language_id}.resources", "comp.runtime", "qualifies", f"The {language_id} resource model qualifies its compiler or runtime services."),
            ]
        )
    relations.extend(
        [
            ("bridge-rust-cpp", "lang.rust.resources", "lang.cpp.resources", "analogous_to", "Rust ownership and C++ RAII both connect values to resource lifetime but differ in alias checking and unsafe obligations."),
            ("bridge-go-erlang", "lang.go.concurrency", "lang.elixir-erlang.concurrency", "analogous_to", "Go channels and BEAM mailboxes both communicate between lightweight activities but have different identity, mailbox, failure, and sharing semantics."),
            ("bridge-swift-kotlin", "lang.swift.concurrency", "lang.kotlin.concurrency", "analogous_to", "Swift and Kotlin structured concurrency both attach tasks to scopes while actor and dispatcher models differ."),
            ("bridge-js-ts", "lang.typescript.types", "lang.javascript.root", "qualifies", "TypeScript static analysis qualifies source programs but emitted JavaScript retains ECMAScript runtime behavior."),
            ("bridge-c-assembly", "lang.c.boundaries", "lang.assembly.root", "qualifies", "C ABI and undefined-behavior rules qualify how source-level operations map to assembly."),
            ("bridge-wasm-host", "lang.webassembly.boundaries", "comp.ffi", "analogous_to", "WebAssembly imports and native FFIs both cross representation and authority boundaries with different validation and capability models."),
            ("bridge-python-ruby", "lang.python.types", "lang.ruby.types", "analogous_to", "Python and Ruby both use dynamic object typing but differ in data model, lookup, tooling, and implementation contracts."),
            ("bridge-ocaml-haskell", "lang.ocaml.types", "lang.haskell.types", "analogous_to", "OCaml and Haskell share inferred functional typing while differing in strictness, effects, modules, objects, and extension ecosystems."),
            ("bridge-sql-state", "lang.sql.concurrency", "comp.memory-model", "analogous_to", "Transaction isolation and language memory models both constrain concurrent observations at different abstraction levels."),
            ("bridge-solidity-state", "lang.solidity.resources", "lang.sql.resources", "analogous_to", "Contract storage and database storage both persist transactional state while authority, finality, cost, and execution models differ."),
        ]
    )
    return relations


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    for index, (identifier, label, statement, subject) in enumerate(COMPILER):
        node_id = f"comp.{identifier}"
        records.append(
            {
                **make_base(
                    node_id, "programming-languages-compilers", subject, COMPILER_LANES,
                    COMPILER_SOURCES, split_for(index, root=identifier == "root"), "concept",
                ),
                "label": label,
                "statement": statement,
                "aliases": [],
            }
        )
        if identifier != "root":
            membership_id = f"lc.membership.comp.{identifier}"
            records.append(
                {
                    **make_base(
                        membership_id, "programming-languages-compilers", subject, COMPILER_LANES,
                        COMPILER_SOURCES, edge_split_for(index), "relation",
                    ),
                    "label": f"{label} compiler-world membership",
                    "statement": f"{label} is a distinct component of the compiler pipeline with its own proof and version conditions.",
                    "aliases": [],
                    "relation": {
                        "source_node": node_id,
                        "target_node": "comp.root",
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": ["the declared language and compiler version apply"],
                        "exceptions": [],
                    },
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                }
            )

    all_language_sources = sorted({source for language in LANGUAGES for source in language_sources(language[0], language[3])})
    records.append(
        {
            **make_base(
                "lang.root", "language-ecosystems", "language-ecosystems.rust", LANGUAGE_LANES,
                all_language_sources, "train", "concept",
            ),
            "label": "Versioned programming-language ecosystems",
            "statement": "Programming-language ecosystems combine language semantics, one or more implementations, runtime and memory behavior, concurrency, modules, packages, build tools, testing, interoperation, and version-specific boundaries.",
            "aliases": ["programming language ecosystems"],
        }
    )

    for index, (language_id, label, subject, source, semantics, types, resources, concurrency, toolchain, boundaries) in enumerate(LANGUAGES, start=1):
        sources = language_sources(language_id, source)
        root_label, root_aliases = ROOT_NAMES.get(language_id, (label, []))
        node_specs = [
            ("root", root_label, semantics),
            ("types", f"{label} type model", types),
            ("resources", f"{label} resource model", resources),
            ("concurrency", f"{label} concurrency model", concurrency),
            ("toolchain", f"{label} toolchain", toolchain),
            ("boundaries", f"{label} error and interoperation boundaries", boundaries),
        ]
        for offset, (suffix, node_label, statement) in enumerate(node_specs):
            node_id = f"lang.{language_id}.{suffix}"
            position = index * len(node_specs) + offset
            records.append(
                {
                    **make_base(
                        node_id, "language-ecosystems", subject, LANGUAGE_LANES, sources,
                        split_for(position, root=suffix == "root"), "concept",
                    ),
                    "label": node_label,
                    "statement": statement,
                    "aliases": list(root_aliases) if suffix == "root" else [],
                    "tags": ["foundation", "language-ecosystems", f"language-{language_id}"],
                }
            )
        membership_id = f"lc.membership.lang.{language_id}"
        records.append(
            {
                **make_base(
                    membership_id, "language-ecosystems", subject, LANGUAGE_LANES, sources,
                    edge_split_for(index), "relation",
                ),
                "label": f"{label} ecosystem membership",
                "statement": f"The versioned {label} profile is a distinct member of the open programming-language ecosystem registry.",
                "aliases": [],
                "relation": {
                    "source_node": f"lang.{language_id}.root",
                    "target_node": "lang.root",
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the cited language and toolchain versions apply"],
                    "exceptions": [],
                },
                "coverage_axes": ["history_versions", "within_domain_composition"],
            }
        )

    relations = build_relations()
    splitter = RelationSplitter([kind for _identifier, _source, _target, kind, _statement in relations])
    for identifier, source_node, target_node, kind, statement in relations:
        is_compiler = identifier in {item[0] for item in COMPILER_RELATIONS}
        domain = "programming-languages-compilers" if is_compiler else "language-ecosystems"
        subject = "programming-languages-compilers.ir" if is_compiler else "language-ecosystems.rust"
        lanes = COMPILER_LANES if is_compiler else sorted(set(COMPILER_LANES + LANGUAGE_LANES))
        sources = COMPILER_SOURCES if is_compiler else sorted(set(COMPILER_SOURCES + all_language_sources))
        records.append(
            {
                **make_base(
                    f"lc.relation.{identifier}", domain, subject, lanes, sources,
                    splitter.split(kind, cross_requested=identifier.startswith("bridge-")), "relation",
                ),
                "label": identifier.replace("-", " "),
                "statement": statement,
                "aliases": [],
                "relation": {
                    "source_node": source_node,
                    "target_node": target_node,
                    "kind": kind,
                    "polarity": -1 if kind in {"inhibits", "prevents", "contradicts", "undercuts"} else 1,
                    "direction": "forward",
                    "conditions": ["the declared language, implementation, target, ABI, and optimization assumptions hold"],
                    "exceptions": [],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
            }
        )

    controls = [
        (identifier, "programming-languages-compilers", "programming-languages-compilers.optimization", COMPILER_LANES, label, statement)
        for identifier, label, statement in CONTROL_SPECS
    ]
    for language_id, label, subject, source, *_rest in LANGUAGES:
        control_label, control_statement = LANGUAGE_CONTROLS[language_id]
        controls.append(
            (
                f"lang-{language_id}", "language-ecosystems", subject, LANGUAGE_LANES,
                f"{label}: {control_label}", control_statement,
            )
        )
    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, domain, subject, lanes, label, statement) in enumerate(controls):
        record_id = f"lc.control.{identifier}"
        records.append(
            {
                **make_base(
                    record_id, domain, subject, lanes, [], control_splits[index % 4],
                    "synthetic_control", "synthetic_control",
                ),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
                "synthetic": True,
                "tags": ["negative-control", domain],
            }
        )

    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (prefix, identifier, label, statement, subject, lanes, sources) in enumerate(WORKED_EXAMPLES):
        domain = "programming-languages-compilers" if prefix == "comp" else "language-ecosystems"
        root = "comp.root" if prefix == "comp" else "lang.root"
        split = example_splits[index % 4]
        node_id = f"lc.example.{prefix}.{identifier}"
        records.append(
            {
                **make_base(node_id, domain, subject, lanes, sources, split, "worked_example"),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"],
                "tags": ["worked-example", domain],
            }
        )
        membership_id = f"lc.example-membership.{prefix}.{identifier}"
        records.append(
            {
                **make_base(membership_id, domain, subject, lanes, sources, split, "relation"),
                "label": f"{label} membership",
                "statement": f"The {label.lower()} operationalizes one bounded compiler or language mechanism composition.",
                "aliases": [],
                "relation": {
                    "source_node": node_id,
                    "target_node": root,
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the example remains versioned and illustrative"],
                    "exceptions": [],
                },
                "coverage_axes": ["applications_toolchains", "within_domain_composition"],
            }
        )

    return sorted(records, key=lambda record: record["record_id"])


def main() -> int:
    records = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    counts: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for record in records:
        counts[record["split"]] = counts.get(record["split"], 0) + 1
        kinds[record["record_kind"]] = kinds.get(record["record_kind"], 0) + 1
    print(f"wrote {OUTPUT} with {len(records)} records")
    print(f"splits: {dict(sorted(counts.items()))}")
    print(f"kinds: {dict(sorted(kinds.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
