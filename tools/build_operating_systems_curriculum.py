#!/usr/bin/env python3
"""Author operating-system and low-level systems causal foundations."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "operating-systems" / "foundations.jsonl"
WORLD = "operating-systems-v0"
LANES = ["thinking.bottom_up", "reasoning.causal", "reasoning.deductive"]
SOURCES = [
    "ostep-110", "linux-kernel-docs", "posix-2024", "windows-kernel-drivers",
    "apple-kernel-guide", "xv6-riscv-book", "freertos-kernel-docs",
]


CONCEPTS = [
    ("root", "Operating-system causal machine", "An operating system virtualizes and protects processor, memory, device, storage, time, identity, and communication resources through kernel mechanisms, user interfaces, persistent metadata, scheduling, and recovery.", "operating-systems-systems.kernels"),
    ("process", "Process", "A process is a protected execution and resource container with an address space, credentials, handles, and one or more threads.", "operating-systems-systems.processes-threads"),
    ("thread", "Thread", "A thread is a schedulable execution context with registers, stack, instruction position, and membership in a process resource context.", "operating-systems-systems.processes-threads"),
    ("address-space", "Virtual address space", "A virtual address space maps process-visible addresses to memory objects and permissions independently for each protection context.", "operating-systems-systems.processes-threads"),
    ("context-switch", "Context switch", "A context switch saves one execution context and restores another, incurring scheduler, cache, translation, and accounting effects.", "operating-systems-systems.processes-threads"),
    ("system-call", "System call", "A system call enters a controlled kernel service boundary with validated arguments, caller identity, and defined result or error semantics.", "operating-systems-systems.processes-threads"),
    ("trap", "Trap", "A trap transfers control to a privileged handler because of an instruction, exception, fault, or system-call mechanism while preserving restart or termination context.", "operating-systems-systems.processes-threads"),
    ("ipc", "Interprocess communication", "IPC communicates data, capabilities, synchronization, or notifications across process boundaries through kernel-mediated channels.", "operating-systems-systems.processes-threads"),
    ("signal", "Process signal", "A signal delivers an asynchronous process notification under masking, disposition, interruption, and reentrancy rules.", "operating-systems-systems.processes-threads"),
    ("descriptor", "Resource descriptor", "A descriptor or handle names a kernel-managed object within a process table and carries access mode, position, lifetime, and inheritance rules.", "operating-systems-systems.processes-threads"),
    ("ready-queue", "Scheduler ready queue", "A ready queue contains runnable threads organized by the scheduler's policy, priority, affinity, and timing rules.", "operating-systems-systems.scheduling"),
    ("dispatcher", "Dispatcher", "The dispatcher selects a runnable thread and transfers processor control by changing execution context and accounting state.", "operating-systems-systems.scheduling"),
    ("preemption", "Preemption", "Preemption suspends a running thread so a scheduler can run another according to priority, timeslice, deadline, or system policy.", "operating-systems-systems.scheduling"),
    ("timeslice", "Timeslice", "A timeslice bounds uninterrupted CPU allocation for a scheduling class but can be shortened by blocking, preemption, or interrupts.", "operating-systems-systems.scheduling"),
    ("priority", "Scheduling priority", "Scheduling priority ranks runnable work within a class and does not by itself guarantee a deadline or eliminate starvation.", "operating-systems-systems.scheduling"),
    ("fairness", "Scheduler fairness", "Fairness defines how processor service is distributed across runnable entities over a chosen interval and weighting policy.", "operating-systems-systems.scheduling"),
    ("starvation", "Scheduling starvation", "Starvation occurs when eligible work waits without sufficient progress because other work repeatedly wins resource allocation.", "operating-systems-systems.scheduling"),
    ("priority-inversion", "Priority inversion", "Priority inversion occurs when high-priority work waits on a resource held by lower-priority work that is delayed by intermediate priorities.", "operating-systems-systems.scheduling"),
    ("affinity", "Processor affinity", "Affinity constrains or prefers where a thread runs to preserve locality, hardware access, or policy while reducing load-balancing freedom.", "operating-systems-systems.scheduling"),
    ("load-balance", "Scheduler load balancing", "Load balancing migrates runnable work among processors to improve utilization while trading cache locality and migration cost.", "operating-systems-systems.scheduling"),
    ("virtual-address", "Virtual address", "A virtual address is interpreted in an address-space context and translated through page tables or related hardware structures.", "operating-systems-systems.memory"),
    ("physical-frame", "Physical page frame", "A physical frame is a fixed-size memory resource that can back virtual mappings, kernel data, caches, or devices.", "operating-systems-systems.memory"),
    ("page-table", "Page table", "A page table maps virtual pages to frames or states with permissions and attributes enforced by hardware and kernel updates.", "operating-systems-systems.memory"),
    ("tlb", "Translation lookaside buffer", "A TLB caches recent address translations and permissions, requiring invalidation or tagging when mappings change.", "operating-systems-systems.memory"),
    ("page-fault", "Page fault", "A page fault transfers control when translation or permission cannot satisfy a memory access, allowing demand resolution or a process-visible error.", "operating-systems-systems.memory"),
    ("demand-paging", "Demand paging", "Demand paging postpones frame allocation and data loading until an access faults on a valid but nonresident mapping.", "operating-systems-systems.memory"),
    ("copy-on-write", "Copy on write", "Copy on write shares read-only backing until a writer faults, then gives the writer a private copy under reference and permission tracking.", "operating-systems-systems.memory"),
    ("memory-map", "Memory mapping", "A memory mapping relates file, anonymous, device, or shared memory objects to virtual address ranges with permissions and lifecycle.", "operating-systems-systems.memory"),
    ("allocator", "Kernel memory allocator", "A kernel allocator provides aligned objects or pages under context, fragmentation, reclaim, concurrency, and failure constraints.", "operating-systems-systems.memory"),
    ("fragmentation", "Memory fragmentation", "Fragmentation leaves free capacity unusable for a requested shape because of placement, size classes, alignment, or physical contiguity.", "operating-systems-systems.memory"),
    ("reclaim", "Memory reclaim", "Reclaim recovers frames by evicting caches, writing dirty data, compressing, swapping, or terminating work under policy and latency constraints.", "operating-systems-systems.memory"),
    ("numa", "Non-uniform memory access", "NUMA makes memory latency and bandwidth depend on processor and memory-node placement, so scheduling and allocation interact.", "operating-systems-systems.memory"),
    ("file", "File", "A file is a persistent or virtual byte-oriented object with metadata, permissions, namespace links, and open-instance state defined by a filesystem interface.", "operating-systems-systems.filesystems"),
    ("inode", "Filesystem object metadata", "An inode-like object records identity and metadata separate from directory names that link to it.", "operating-systems-systems.filesystems"),
    ("directory", "Directory", "A directory maps names to filesystem object identities under lookup, mutation, permission, and crash-consistency rules.", "operating-systems-systems.filesystems"),
    ("mount", "Mount", "A mount attaches a filesystem root into a process-visible namespace with propagation, permission, and lifetime behavior.", "operating-systems-systems.filesystems"),
    ("open-file", "Open file description", "An open file description stores access mode, current offset, status flags, and object reference shared by duplicated descriptors according to the OS model.", "operating-systems-systems.filesystems"),
    ("page-cache", "Filesystem page cache", "A page cache retains file data in memory and coordinates reads, writes, mapping, dirty state, reclaim, and persistence.", "operating-systems-systems.filesystems"),
    ("block-allocation", "Filesystem block allocation", "Block allocation maps logical file ranges and metadata to storage extents under locality, fragmentation, growth, and failure constraints.", "operating-systems-systems.filesystems"),
    ("journal", "Filesystem journal", "A journal records ordered metadata or data intentions so recovery can restore a consistent state after interruption.", "operating-systems-systems.filesystems"),
    ("fs-cow", "Copy-on-write filesystem", "A copy-on-write filesystem writes changed blocks to new locations and atomically redirects metadata roots, enabling snapshots while retaining reference and space complexity.", "operating-systems-systems.filesystems"),
    ("fsync", "Persistence synchronization", "A persistence call requests that selected data and metadata reach a durability boundary, whose exact guarantees depend on filesystem, device, and OS contracts.", "operating-systems-systems.filesystems"),
    ("crash-consistency", "Crash consistency", "Crash consistency defines which filesystem invariants and update prefixes remain valid after power or system interruption.", "operating-systems-systems.filesystems"),
    ("device", "Device", "A device is a hardware or virtual endpoint with registers, queues, interrupts, DMA, lifecycle, and a driver-facing contract.", "operating-systems-systems.io-drivers"),
    ("mmio", "Memory-mapped I/O", "MMIO maps device registers into an address space where access width, ordering, volatility, and side effects differ from ordinary memory.", "operating-systems-systems.io-drivers"),
    ("interrupt", "Hardware interrupt", "An interrupt asynchronously transfers control to a privileged handler that acknowledges the source and schedules bounded follow-up work.", "operating-systems-systems.io-drivers"),
    ("dma", "Direct memory access", "DMA lets a device transfer data to memory using mappings, descriptors, coherency, ownership, and completion rules coordinated by the driver and IOMMU where present.", "operating-systems-systems.io-drivers"),
    ("driver", "Device driver", "A device driver translates kernel operations into device commands and interrupts while enforcing state, concurrency, power, memory, and error contracts.", "operating-systems-systems.io-drivers"),
    ("io-queue", "I/O queue", "An I/O queue orders and batches requests between software and a device while applying priority, fairness, merging, and completion policy.", "operating-systems-systems.io-drivers"),
    ("blocking-io", "Blocking I/O", "Blocking I/O suspends the calling thread until progress, completion, timeout, signal, or error makes the operation return.", "operating-systems-systems.io-drivers"),
    ("async-io", "Asynchronous I/O", "Asynchronous I/O separates submission from completion and therefore requires operation identity, buffer lifetime, cancellation, ordering, and error handling.", "operating-systems-systems.io-drivers"),
    ("hotplug", "Device hotplug", "Hotplug changes device presence while operations may be active, requiring reference lifetimes, quiescence, notification, and safe failure.", "operating-systems-systems.io-drivers"),
    ("user-mode", "User mode", "User mode restricts privileged instructions and address access so processes must use mediated system interfaces.", "operating-systems-systems.kernels"),
    ("kernel-mode", "Kernel mode", "Kernel mode can alter global machine state and therefore requires strict validation, synchronization, fault containment, and minimal trusted code.", "operating-systems-systems.kernels"),
    ("monolithic", "Monolithic kernel", "A monolithic kernel runs core scheduling, memory, filesystems, networking, and many drivers in one privileged address space with direct-call efficiency and shared-failure risk.", "operating-systems-systems.kernels"),
    ("microkernel", "Microkernel", "A microkernel keeps a small set of scheduling, memory, and IPC mechanisms privileged while moving services into isolated user processes, trading isolation against communication complexity.", "operating-systems-systems.kernels"),
    ("hybrid-kernel", "Hybrid kernel", "A hybrid kernel combines microkernel-derived abstractions with major services linked into one privileged address space for pragmatic performance and compatibility.", "operating-systems-systems.kernels"),
    ("kernel-module", "Kernel module", "A kernel module adds privileged code and symbols at runtime under version, signature, reference, unload, and ABI constraints.", "operating-systems-systems.kernels"),
    ("kernel-lock", "Kernel synchronization", "Kernel synchronization coordinates shared state across threads, processors, interrupts, and preemption contexts under ordering and blocking restrictions.", "operating-systems-systems.kernels"),
    ("capability", "Kernel capability", "A capability is an unforgeable authority reference whose possession permits a bounded operation on an object.", "operating-systems-systems.kernels"),
    ("kernel-invariant", "Kernel invariant", "A kernel invariant must hold across every reachable privileged state and transition because one violation can compromise the whole protection boundary.", "operating-systems-systems.kernels"),
    ("reset", "Processor reset state", "Reset places processors into architecture-defined initial state from which firmware establishes enough hardware and memory context to load later stages.", "operating-systems-systems.boot-firmware"),
    ("firmware", "Platform firmware", "Platform firmware initializes hardware and exposes a versioned handoff contract to boot software without becoming the operating system runtime itself.", "operating-systems-systems.boot-firmware"),
    ("bootloader", "Bootloader", "A bootloader selects, verifies where configured, loads, and transfers control to a kernel image with parameters and hardware information.", "operating-systems-systems.boot-firmware"),
    ("kernel-image", "Kernel image", "A kernel image contains executable privileged code, data, metadata, and entry assumptions for a target architecture and boot protocol.", "operating-systems-systems.boot-firmware"),
    ("early-memory", "Early memory initialization", "Early memory initialization discovers usable regions, reserves firmware and image areas, establishes page tables, and creates initial allocators before normal memory services exist.", "operating-systems-systems.boot-firmware"),
    ("initramfs", "Initial RAM filesystem", "An initial RAM filesystem supplies early user-space tools and drivers needed to discover and mount the eventual root filesystem.", "operating-systems-systems.boot-firmware"),
    ("init-process", "Initial user process", "The initial user-space process becomes ancestor and service manager for later system processes and handles orphaned lifecycle responsibilities according to the OS.", "operating-systems-systems.boot-firmware"),
    ("hypervisor", "Hypervisor", "A hypervisor multiplexes processors, memory, interrupts, and devices among virtual machines while mediating privileged operations.", "operating-systems-systems.virtualization"),
    ("virtual-machine", "Virtual machine", "A virtual machine presents a hardware-like execution environment with virtual CPUs, memory, firmware, and devices to a guest OS.", "operating-systems-systems.virtualization"),
    ("vcpu", "Virtual CPU", "A virtual CPU is schedulable guest execution state mapped onto host processors under hypervisor policy.", "operating-systems-systems.virtualization"),
    ("nested-paging", "Nested address translation", "Nested translation combines guest virtual-to-physical and host physical mappings in hardware-cached translation paths.", "operating-systems-systems.virtualization"),
    ("paravirtual", "Paravirtualized device", "A paravirtualized device exposes a virtualization-aware queue interface that avoids emulating all physical-device details.", "operating-systems-systems.virtualization"),
    ("container", "Operating-system container", "A container isolates processes using shared-kernel namespaces, resource controls, filesystem views, and security policy rather than a separate guest kernel.", "operating-systems-systems.virtualization"),
    ("namespace", "Kernel namespace", "A namespace gives a process group a distinct view of selected global identifiers or resources.", "operating-systems-systems.virtualization"),
    ("cgroup", "Control group", "A control group accounts for, limits, prioritizes, or isolates resource use by a process hierarchy.", "operating-systems-systems.virtualization"),
    ("container-image", "Container image", "A container image is an immutable layered filesystem and metadata input whose runtime behavior also depends on configuration, kernel, mounts, secrets, and network.", "operating-systems-systems.virtualization"),
    ("linux-vfs", "Linux virtual filesystem", "The Linux VFS provides common inode, dentry, file, mount, and operation abstractions over diverse filesystem implementations.", "operating-systems-systems.linux"),
    ("linux-proc", "Linux proc and sysfs", "Procfs and sysfs expose selected process, kernel, device, and configuration state through virtual filesystem interfaces with versioned semantics.", "operating-systems-systems.linux"),
    ("linux-cgroup", "Linux cgroups", "Linux cgroups organize tasks for resource accounting, limits, and controllers independently of namespace visibility.", "operating-systems-systems.linux"),
    ("linux-namespace", "Linux namespaces", "Linux namespaces isolate views of process IDs, mounts, networks, users, IPC, hostnames, time, and related resources by namespace type.", "operating-systems-systems.linux"),
    ("linux-ebpf", "Linux eBPF", "eBPF runs verifier-constrained programs at supported kernel hooks with maps, helpers, capabilities, and version-dependent program types.", "operating-systems-systems.linux"),
    ("linux-io-uring", "Linux io_uring", "io_uring uses shared submission and completion rings for asynchronous operations under buffer, ordering, cancellation, and kernel-version contracts.", "operating-systems-systems.linux"),
    ("windows-executive", "Windows executive", "The Windows executive provides kernel-mode object, process, thread, memory, I/O, configuration, security, and other services above low-level kernel mechanisms.", "operating-systems-systems.windows"),
    ("windows-object", "Windows object manager", "The object manager gives kernel objects typed identities, namespaces, handles, access checks, references, and lifecycle.", "operating-systems-systems.windows"),
    ("windows-io", "Windows I/O manager", "The I/O manager routes request packets through layered device stacks and coordinates completion, cancellation, buffers, power, and plug-and-play state.", "operating-systems-systems.windows"),
    ("windows-irql", "Windows interrupt request level", "IRQL constrains which interrupts, code paths, memory, and synchronization operations are permitted at a given processor priority level.", "operating-systems-systems.windows"),
    ("windows-driver", "Windows driver stack", "Windows drivers attach device objects in ordered stacks so requests can be created, filtered, forwarded, completed, canceled, and removed under framework rules.", "operating-systems-systems.windows"),
    ("windows-registry", "Windows registry", "The registry stores hierarchical system and application configuration with hives, keys, values, security descriptors, transactions or notifications, and versioned policy.", "operating-systems-systems.windows"),
    ("xnu", "XNU hybrid kernel", "XNU combines Mach scheduling, virtual memory, and IPC abstractions with BSD processes, networking, filesystems, security, and I/O Kit services in one kernel address space.", "operating-systems-systems.apple"),
    ("mach-task", "Mach task", "A Mach task owns a virtual address space and port-right namespace and contains one or more schedulable threads.", "operating-systems-systems.apple"),
    ("mach-port", "Mach port right", "A Mach port right is a capability-like authority to send, receive, or otherwise act on a message endpoint under right-transfer rules.", "operating-systems-systems.apple"),
    ("bsd-process", "Darwin BSD process", "The BSD layer supplies POSIX-facing process, credential, signal, filesystem, socket, and system-call semantics integrated with Mach tasks and threads.", "operating-systems-systems.apple"),
    ("iokit", "I/O Kit", "I/O Kit structures Darwin drivers and device relationships through object-oriented matching, lifecycle, power, and user-client boundaries.", "operating-systems-systems.apple"),
    ("hard-realtime", "Hard real-time system", "A hard real-time system treats any missed deadline as a system failure and therefore requires bounded worst-case timing evidence.", "operating-systems-systems.real-time"),
    ("soft-realtime", "Soft real-time system", "A soft real-time system degrades in value when deadlines are missed but can tolerate a bounded miss distribution.", "operating-systems-systems.real-time"),
    ("wcet", "Worst-case execution time", "WCET bounds execution duration for a task under declared hardware, cache, interrupt, path, compiler, and input assumptions.", "operating-systems-systems.real-time"),
    ("deadline", "Real-time deadline", "A deadline is the latest acceptable completion time relative to release or another event and must be paired with period, jitter, and consequence.", "operating-systems-systems.real-time"),
    ("rt-priority", "Fixed-priority real-time scheduling", "Fixed-priority scheduling always selects the highest-priority ready real-time task, requiring schedulability and blocking analysis.", "operating-systems-systems.real-time"),
    ("priority-inheritance", "Priority inheritance", "Priority inheritance temporarily raises a lock holder to the highest waiting priority to bound one source of priority inversion.", "operating-systems-systems.real-time"),
    ("isr", "Interrupt service routine", "An ISR performs the minimum bounded hardware acknowledgment and defers longer work to an appropriate schedulable context.", "operating-systems-systems.real-time"),
    ("bounded-latency", "Bounded interrupt latency", "Bounded interrupt latency requires upper bounds on masking, nonpreemptible sections, higher-priority work, and hardware delivery.", "operating-systems-systems.real-time"),
    ("static-allocation", "Static real-time allocation", "Static allocation reserves required memory and objects before critical operation to avoid unbounded allocator and exhaustion behavior.", "operating-systems-systems.real-time"),
]


RELATIONS = [
    ("process-thread", "os.thread", "os.process", "part_of", "Threads execute within a process resource context."),
    ("process-address", "os.address-space", "os.process", "part_of", "A protected address space forms part of a process."),
    ("descriptor-process", "os.descriptor", "os.process", "part_of", "Resource descriptors are owned through a process table."),
    ("syscall-trap", "os.system-call", "os.trap", "implements", "A system-call instruction implements one intentional trap path into the kernel."),
    ("trap-mode", "os.trap", "os.kernel-mode", "causes", "A valid trap transfers controlled execution into kernel mode."),
    ("ipc-process", "os.ipc", "os.process", "qualifies", "IPC qualifies how isolated processes exchange data and authority."),
    ("signal-thread", "os.signal", "os.thread", "qualifies", "Signal delivery qualifies interruption and handling in a target process thread."),
    ("switch-thread", "os.context-switch", "os.thread", "transforms_to", "A context switch transforms the currently running thread state."),
    ("thread-ready", "os.thread", "os.ready-queue", "part_of", "A runnable thread is represented in a scheduler ready structure."),
    ("ready-dispatch", "os.ready-queue", "os.dispatcher", "prerequisite", "A ready-set policy is prerequisite to dispatch selection."),
    ("dispatch-switch", "os.dispatcher", "os.context-switch", "causes", "Dispatching a different thread causes a context switch."),
    ("preempt-dispatch", "os.preemption", "os.dispatcher", "causes", "Preemption causes the dispatcher to reconsider runnable work."),
    ("slice-preempt", "os.timeslice", "os.preemption", "causes", "Timeslice expiration can cause preemption."),
    ("priority-ready", "os.priority", "os.ready-queue", "qualifies", "Priority qualifies ready-queue ordering within a scheduling class."),
    ("fair-starve", "os.fairness", "os.starvation", "prevents", "A suitable fairness guarantee prevents indefinite starvation for covered work."),
    ("inversion-priority", "os.priority-inversion", "os.priority", "undercuts", "Unbounded priority inversion undercuts response-time assumptions based on priority alone."),
    ("affinity-balance", "os.affinity", "os.load-balance", "qualifies", "Affinity constraints qualify which migrations load balancing may perform."),
    ("virtual-address-space", "os.virtual-address", "os.address-space", "part_of", "Virtual addresses are interpreted inside an address-space context."),
    ("page-frame", "os.physical-frame", "os.page-table", "part_of", "Page-table mappings can reference physical frames."),
    ("table-address", "os.page-table", "os.virtual-address", "transforms_to", "Page-table translation maps a virtual page toward physical backing or a fault state."),
    ("tlb-table", "os.tlb", "os.page-table", "supports", "A TLB supports fast reuse of page-table translations."),
    ("fault-table", "os.page-table", "os.page-fault", "causes", "A missing or disallowed translation causes a page fault."),
    ("demand-fault", "os.page-fault", "os.demand-paging", "implements", "Page faults implement demand loading of valid nonresident pages."),
    ("cow-fault", "os.page-fault", "os.copy-on-write", "implements", "A write-protection fault implements copy-on-write separation."),
    ("map-address", "os.memory-map", "os.address-space", "transforms_to", "Mapping transforms an address-space region by attaching memory-object backing."),
    ("allocator-frame", "os.allocator", "os.physical-frame", "qualifies", "Allocator policy qualifies which frames or objects satisfy a request."),
    ("fragment-allocator", "os.fragmentation", "os.allocator", "inhibits", "Fragmentation inhibits allocation despite remaining aggregate capacity."),
    ("reclaim-frame", "os.reclaim", "os.physical-frame", "transforms_to", "Reclaim transforms occupied reclaimable frames into available capacity."),
    ("numa-affinity", "os.numa", "os.affinity", "qualifies", "NUMA locality qualifies scheduler affinity and placement."),
    ("inode-file", "os.inode", "os.file", "part_of", "Filesystem metadata and identity form part of file representation."),
    ("directory-inode", "os.directory", "os.inode", "supports", "Directory entries support name lookup to filesystem object identity."),
    ("mount-directory", "os.mount", "os.directory", "transforms_to", "Mounting transforms namespace lookup at a directory attachment point."),
    ("descriptor-open", "os.descriptor", "os.open-file", "supports", "A process descriptor references an open file description."),
    ("cache-file", "os.page-cache", "os.file", "supports", "The page cache supports buffered and mapped file access."),
    ("block-file", "os.block-allocation", "os.file", "implements", "Block allocation implements persistent placement of file data and metadata."),
    ("journal-crash", "os.journal", "os.crash-consistency", "supports", "Ordered journaling supports recovery to a consistent update boundary."),
    ("cow-crash", "os.fs-cow", "os.crash-consistency", "supports", "Atomic copy-on-write root updates support crash consistency."),
    ("fsync-cache", "os.fsync", "os.page-cache", "transforms_to", "Persistence synchronization transforms selected dirty cached state toward the durability boundary."),
    ("driver-device", "os.driver", "os.device", "implements", "A driver implements the operating-system side of a device contract."),
    ("mmio-device", "os.mmio", "os.device", "part_of", "MMIO exposes selected device registers to software."),
    ("interrupt-device", "os.device", "os.interrupt", "causes", "A device event can cause a hardware interrupt."),
    ("dma-device", "os.dma", "os.device", "qualifies", "DMA qualifies device access to mapped memory buffers."),
    ("queue-driver", "os.io-queue", "os.driver", "part_of", "I/O queues form part of many driver-device protocols."),
    ("blocking-thread", "os.blocking-io", "os.thread", "causes", "Blocking I/O can cause the calling thread to leave the runnable set."),
    ("async-queue", "os.async-io", "os.io-queue", "implements", "Asynchronous I/O implements separated submission and completion queues."),
    ("hotplug-driver", "os.hotplug", "os.driver", "qualifies", "Hotplug qualifies driver object lifetime and in-flight operations."),
    ("user-syscall", "os.user-mode", "os.system-call", "prerequisite", "User-mode code uses mediated system calls for privileged services."),
    ("kernel-syscall", "os.kernel-mode", "os.system-call", "implements", "Kernel-mode handlers implement system-call services."),
    ("monolithic-kernel", "os.monolithic", "os.root", "qualifies", "A monolithic organization qualifies which services share privileged address space."),
    ("micro-ipc", "os.microkernel", "os.ipc", "qualifies", "A microkernel organization qualifies service communication through IPC."),
    ("hybrid-monolithic", "os.hybrid-kernel", "os.monolithic", "analogous_to", "Hybrid and monolithic kernels share privileged in-process services while differing in inherited abstractions and modular structure."),
    ("module-kernel", "os.kernel-module", "os.kernel-mode", "part_of", "A loaded module becomes part of privileged kernel code."),
    ("lock-invariant", "os.kernel-lock", "os.kernel-invariant", "supports", "Correct synchronization supports preservation of shared kernel invariants."),
    ("capability-mediation", "os.capability", "os.system-call", "qualifies", "Capability possession qualifies authority checked at system interfaces."),
    ("reset-firmware", "os.reset", "os.firmware", "causes", "Processor reset causes execution to enter the platform firmware path."),
    ("firmware-bootloader", "os.firmware", "os.bootloader", "causes", "Firmware policy selects and transfers control to a bootloader or OS loader."),
    ("loader-image", "os.bootloader", "os.kernel-image", "transforms_to", "A bootloader maps and prepares the kernel image for execution."),
    ("image-memory", "os.kernel-image", "os.early-memory", "prerequisite", "Image placement and platform memory information are prerequisites to early memory setup."),
    ("memory-initramfs", "os.early-memory", "os.initramfs", "prerequisite", "Early allocation and mappings are prerequisite to using an initial RAM filesystem."),
    ("initramfs-init", "os.initramfs", "os.init-process", "supports", "The initial RAM filesystem supports discovery of the real root and launch of early user space."),
    ("hypervisor-vm", "os.hypervisor", "os.virtual-machine", "implements", "A hypervisor implements the resource boundary of a virtual machine."),
    ("vcpu-vm", "os.vcpu", "os.virtual-machine", "part_of", "Virtual CPUs form part of a VM."),
    ("nested-vm", "os.nested-paging", "os.virtual-machine", "supports", "Nested translation supports guest virtual memory over host memory."),
    ("para-device", "os.paravirtual", "os.virtual-machine", "part_of", "Paravirtual devices form part of a guest hardware interface."),
    ("container-process", "os.process", "os.container", "part_of", "Host processes compose an operating-system container."),
    ("namespace-container", "os.namespace", "os.container", "part_of", "Namespaces form one container isolation mechanism."),
    ("cgroup-container", "os.cgroup", "os.container", "part_of", "Control groups form one container resource mechanism."),
    ("image-container", "os.container-image", "os.container", "qualifies", "An image qualifies a container's initial filesystem and metadata."),
    ("vfs-file", "os.linux-vfs", "os.file", "implements", "The Linux VFS implements common file-object operations."),
    ("proc-vfs", "os.linux-proc", "os.linux-vfs", "part_of", "Procfs and sysfs are virtual filesystem implementations."),
    ("linux-cgroup", "os.linux-cgroup", "os.cgroup", "implements", "Linux cgroups implement resource-control groups."),
    ("linux-namespace", "os.linux-namespace", "os.namespace", "implements", "Linux namespace types implement isolated resource views."),
    ("ebpf-kernel", "os.linux-ebpf", "os.kernel-mode", "qualifies", "The eBPF verifier and helper policy qualify safe execution at kernel hooks."),
    ("uring-async", "os.linux-io-uring", "os.async-io", "implements", "io_uring implements ring-based asynchronous submission and completion."),
    ("windows-exec-kernel", "os.windows-executive", "os.kernel-mode", "part_of", "Windows executive services run in kernel mode."),
    ("windows-object-cap", "os.windows-object", "os.descriptor", "implements", "Windows handles implement references to object-manager objects."),
    ("windows-io-driver", "os.windows-io", "os.windows-driver", "qualifies", "The I/O manager qualifies request flow through driver stacks."),
    ("irql-interrupt", "os.windows-irql", "os.interrupt", "qualifies", "IRQL qualifies interrupt masking and permissible driver operations."),
    ("registry-file", "os.windows-registry", "os.file", "analogous_to", "Registry hives and files both persist named data under distinct object and transaction semantics."),
    ("xnu-hybrid", "os.xnu", "os.hybrid-kernel", "implements", "XNU implements a hybrid Mach and BSD kernel organization."),
    ("task-process", "os.mach-task", "os.process", "analogous_to", "Mach tasks and POSIX processes overlap in resource ownership but are not identical abstractions."),
    ("port-capability", "os.mach-port", "os.capability", "implements", "Mach port rights implement capability-like IPC authority."),
    ("bsd-task", "os.bsd-process", "os.mach-task", "qualifies", "Darwin BSD process state qualifies and integrates with a Mach task."),
    ("iokit-driver", "os.iokit", "os.driver", "implements", "I/O Kit implements a Darwin driver and device framework."),
    ("hard-deadline", "os.deadline", "os.hard-realtime", "qualifies", "A missed deadline qualifies hard real-time system failure."),
    ("soft-deadline", "os.deadline", "os.soft-realtime", "qualifies", "Deadline misses qualify degraded value in a soft real-time system."),
    ("wcet-deadline", "os.wcet", "os.deadline", "prerequisite", "A credible WCET bound is prerequisite to schedulability against deadlines."),
    ("rt-priority", "os.rt-priority", "os.ready-queue", "qualifies", "Fixed-priority policy qualifies ready selection in a real-time scheduler."),
    ("inherit-inversion", "os.priority-inheritance", "os.priority-inversion", "inhibits", "Priority inheritance inhibits unbounded inversion from a lower-priority lock holder."),
    ("isr-interrupt", "os.isr", "os.interrupt", "implements", "An ISR implements bounded interrupt acknowledgment and deferral."),
    ("latency-isr", "os.bounded-latency", "os.isr", "qualifies", "Latency bounds qualify the permitted ISR and masking duration."),
    ("static-allocator", "os.static-allocation", "os.allocator", "inhibits", "Preallocated critical objects inhibit runtime allocator jitter and exhaustion."),
    ("bridge-vm-container", "os.virtual-machine", "os.container", "analogous_to", "VMs and containers both isolate workloads but virtualize hardware and shared-kernel resources respectively."),
    ("bridge-scheduler-memory", "os.load-balance", "os.numa", "qualifies", "NUMA placement qualifies whether CPU load migration improves or harms locality."),
    ("bridge-dma-security", "os.dma", "os.address-space", "qualifies", "IOMMU and driver mappings qualify which physical memory a device can reach outside process page tables."),
    ("bridge-crash-boot", "os.crash-consistency", "os.init-process", "prerequisite", "Recoverable persistent state is prerequisite to reliable system restart after interruption."),
]


CONTROLS = [
    ("process-program", "Process equals program file", "A process must not be treated as identical to an executable file; it includes live state, resources, identity, and threads."),
    ("thread-process", "Thread owns independent process resources", "A thread must not be described as owning an independent address space and handle table when those are shared through its process."),
    ("syscall-trust", "System-call arguments are trusted", "Kernel entry must not trust user pointers, lengths, handles, or state without validation and safe copying."),
    ("priority-deadline", "High priority guarantees deadline", "High scheduling priority must not be treated as deadline proof without execution, blocking, interference, and scheduler analysis."),
    ("fair-no-starve", "Average fairness prevents starvation", "Average CPU fairness must not be treated as a per-request progress guarantee without a bounded interval."),
    ("virtual-physical", "Virtual address is physical address", "A process virtual address must not be treated as a globally meaningful physical location."),
    ("fault-bug", "Every page fault is a bug", "A page fault must not be classified as an error when it validly implements demand paging or copy on write."),
    ("free-total", "Free memory total proves allocation", "Aggregate free memory must not prove a contiguous, aligned, zone-specific, or atomic allocation can succeed."),
    ("write-durable", "Write completion proves persistence", "A successful buffered write must not be treated as durable storage without the documented synchronization and hardware boundary."),
    ("rename-everything", "Rename makes all updates atomic", "Atomic namespace rename must not be generalized to durability or atomicity of every related data and metadata write."),
    ("checksum-auth", "Filesystem checksum authenticates data", "An integrity checksum must not be treated as proof against a malicious writer with the ability to recompute it."),
    ("mmio-memory", "MMIO behaves like ordinary memory", "Device-register access must not be optimized, reordered, cached, or repeated as ordinary memory without the architecture and driver contract."),
    ("interrupt-sleep", "Interrupt handler can block freely", "Interrupt context must not call operations that can sleep or take incompatible locks when the OS forbids it."),
    ("dma-process", "Process page table contains DMA", "CPU virtual mappings must not be assumed to govern device DMA without the device and IOMMU mapping contract."),
    ("kernel-recover", "Kernel fault is process-local", "A privileged memory or synchronization error must not be assumed containable to one process."),
    ("module-safe", "Signed kernel module is safe", "A signature must not establish that privileged module logic, version compatibility, or runtime behavior is correct."),
    ("micro-secure", "Microkernel automatically secure", "A small privileged core must not be treated as sufficient security without correct policy, IPC, drivers, services, and capability use."),
    ("boot-runtime", "Firmware service remains available", "A firmware boot service must not be assumed available after the kernel takes ownership unless the handoff contract says so."),
    ("image-root", "Kernel image includes working root filesystem", "Loading a kernel image must not be treated as proof that drivers, storage, initramfs, and the real root can initialize."),
    ("vm-container", "Container is a virtual machine", "A shared-kernel container must not be described as having an independent guest kernel protection boundary."),
    ("image-running", "Container image defines running system", "An image alone must not be treated as complete runtime identity without kernel, configuration, mounts, secrets, network, and entry state."),
    ("namespace-security", "Namespace alone is sandbox", "Namespace isolation must not substitute for capabilities, resource limits, syscall policy, filesystem restrictions, and kernel security."),
    ("proc-stable", "Procfs path is timeless API", "A procfs or sysfs entry must not be treated as a timeless cross-version interface without documented stability."),
    ("ebpf-safe-all", "eBPF verification proves policy safety", "Verifier acceptance must not establish that allowed helpers, hooks, data access, or program logic meets the operator's security policy."),
    ("irql-priority", "Windows IRQL is thread priority", "IRQL must not be confused with schedulable thread priority."),
    ("handle-pointer", "Windows handle is kernel pointer", "A user handle must not be treated as a directly dereferenceable kernel object address."),
    ("mach-port-message", "Mach port name is global", "A Mach port name must not be treated as globally meaningful outside its task's right namespace."),
    ("rt-average", "Average latency proves real-time bound", "Mean or percentile latency must not be substituted for a worst-case bound in a hard real-time claim."),
    ("wcet-benchmark", "Longest observed run equals WCET", "The longest measured execution must not be labeled WCET without proof that all relevant paths and interference are bounded."),
    ("static-no-failure", "Static allocation eliminates failure", "Preallocation must not be treated as eliminating capacity exhaustion, corruption, deadline, device, or logic failures."),
]


WORKED_EXAMPLES = [
    ("cow-fork", "Copy-on-write fork", "A parent and child initially map one read-only frame; a child write faults, allocates a new frame, copies data, changes only the child mapping, and invalidates its translation.", "operating-systems-systems.memory"),
    ("journal-crash", "Journal crash recovery", "A metadata transaction writes journal data and commit evidence before home locations; recovery replays only complete committed transactions and restores filesystem invariants.", "operating-systems-systems.filesystems"),
    ("async-buffer", "Asynchronous I/O buffer lifetime", "A request pins or owns its buffer until the completion identity arrives; cancellation reconciles whether the device already consumed or produced bytes.", "operating-systems-systems.io-drivers"),
    ("priority-inversion", "Priority-inversion schedule", "A low-priority task holds a lock, a high-priority task blocks on it, and an intermediate task preempts the holder; priority inheritance lets the holder finish and bounds the inversion.", "operating-systems-systems.scheduling"),
    ("boot-chain", "Boot dependency chain", "Reset enters firmware, a loader verifies and maps the kernel, early memory creates page tables, initramfs discovers storage, and the first user process mounts services with each handoff checked.", "operating-systems-systems.boot-firmware"),
    ("container-limit", "Container resource boundary", "A workload receives PID and mount namespaces plus CPU and memory cgroup limits; a test shows namespace isolation does not cap memory until the cgroup policy is applied.", "operating-systems-systems.virtualization"),
    ("linux-uring", "io_uring completion identity", "Two reads are submitted with distinct user data; completions arrive out of order and are matched to buffers by identity rather than submission position.", "operating-systems-systems.linux"),
    ("windows-driver", "Windows driver request lifecycle", "A request enters a layered device stack, each driver preserves ownership and cancellation state, completion unwinds in reverse, and removal waits for outstanding references.", "operating-systems-systems.windows"),
    ("mach-right", "Mach right transfer", "A task sends a message carrying a send right; the receiver gains only the declared right while the original receive right remains in its owning namespace.", "operating-systems-systems.apple"),
    ("deadline-test", "Hard-deadline evidence", "A task set combines WCET, periods, deadlines, blocking, interrupt latency, scheduler overhead, and release jitter before a schedulability claim is made.", "operating-systems-systems.real-time"),
    ("tlb-shootdown", "TLB shootdown", "A kernel removes a shared mapping, publishes the page-table change, requests invalidation on processors that may cache it, waits for acknowledgment, and only then reuses the frame.", "operating-systems-systems.memory"),
    ("timeout-unknown", "System-call interruption", "A blocking operation is interrupted after partial progress; the caller uses the returned count and error contract instead of retrying the entire request blindly.", "operating-systems-systems.processes-threads"),
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
    subject: str,
    sources: list[str],
    split: str,
    kind: str,
    epistemic: str = "established",
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": identifier,
        "world_id": WORLD,
        "domain_id": "operating-systems-systems",
        "subject_id": subject,
        "lanes": LANES,
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"],
        "source_ids": sorted(set(sources)),
        "scope": "operating-system and low-level systems foundation tranche",
        "limitations": [
            "Hardware, kernel, ABI, driver, filesystem, and operating-system statements are version and target sensitive.",
            "Privileged implementation examples require isolated owned targets and cannot establish production safety alone.",
            "Platform-specific subsystems and the open hardware and standards frontier remain incomplete.",
        ],
        "as_of": "2026-09-03",
        "version_boundary": "operating-systems-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", "operating-systems-systems"],
    }


def source_for_subject(subject: str) -> list[str]:
    if subject == "operating-systems-systems.linux":
        return ["linux-kernel-docs", "posix-2024"]
    if subject == "operating-systems-systems.windows":
        return ["windows-kernel-drivers"]
    if subject == "operating-systems-systems.apple":
        return ["apple-kernel-guide", "posix-2024"]
    if subject == "operating-systems-systems.real-time":
        return ["freertos-kernel-docs", "ostep-110"]
    return ["ostep-110", "xv6-riscv-book", "posix-2024", "linux-kernel-docs"]


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, (identifier, label, statement, subject) in enumerate(CONCEPTS):
        node_id = f"os.{identifier}"
        sources = source_for_subject(subject)
        records.append(
            {
                **make_base(node_id, subject, sources, split_for(index, root=identifier == "root"), "concept"),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()],
            }
        )
        if identifier != "root":
            membership_id = f"os.membership.{identifier}"
            records.append(
                {
                    **make_base(membership_id, subject, sources, edge_split_for(index), "relation"),
                    "label": f"{label} operating-system membership",
                    "statement": f"{label} is a distinct component of the operating-system causal machine under its target and version constraints.",
                    "aliases": [],
                    "relation": {
                        "source_node": node_id,
                        "target_node": "os.root",
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": ["the declared operating-system, architecture, and version apply"],
                        "exceptions": [],
                    },
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                }
            )

    splitter = RelationSplitter(
        [kind for _identifier, _source, _target, kind, _statement in RELATIONS],
        cross_plan=[
            identifier.startswith("bridge-")
            for identifier, _source, _target, _kind, _statement in RELATIONS
        ],
    )
    for identifier, source_node, target_node, kind, statement in RELATIONS:
        records.append(
            {
                **make_base(
                    f"os.relation.{identifier}", "operating-systems-systems.kernels", SOURCES,
                    splitter.split(kind),
                    "relation",
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
                    "conditions": ["the stated privilege, timing, architecture, state, and persistence assumptions hold"],
                    "exceptions": [],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
            }
        )

    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        record_id = f"os.control.{identifier}"
        records.append(
            {
                **make_base(
                    record_id, "operating-systems-systems.kernels", [], control_splits[index % 4],
                    "synthetic_control", "synthetic_control",
                ),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()],
                "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
                "synthetic": True,
                "tags": ["negative-control", "operating-systems-systems"],
            }
        )

    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement, subject) in enumerate(WORKED_EXAMPLES):
        split = example_splits[index % 4]
        sources = source_for_subject(subject)
        node_id = f"os.example.{identifier}"
        records.append(
            {
                **make_base(node_id, subject, sources, split, "worked_example"),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"],
                "tags": ["worked-example", "operating-systems-systems"],
            }
        )
        membership_id = f"os.example-membership.{identifier}"
        records.append(
            {
                **make_base(membership_id, subject, sources, split, "relation"),
                "label": f"{label} membership",
                "statement": f"The {label.lower()} operationalizes one bounded operating-system mechanism composition.",
                "aliases": [],
                "relation": {
                    "source_node": node_id,
                    "target_node": "os.root",
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the example remains target-specific and illustrative"],
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
