# Condensed C++ Core Guidelines

Source basis: ISO C++ Core Guidelines, https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines, source page dated 2025-07-08.

## Contents

- Operating Model
- High-Signal Review Checklist
- Philosophy
- Interfaces
- Functions
- Classes And Types
- Enumerations
- Resource Management
- Expressions And Statements
- Performance
- Concurrency And Parallelism
- Error Handling
- Constants And Immutability
- Templates And Generic Programming
- C Interop And C-Style Code
- Source Files And Namespaces
- Standard Library
- Architecture
- Profiles, Tools, And GSL
- Naming And Layout
- Applying The Guidelines Pragmatically

## How To Use This Reference

Start with High-Signal Review Checklist for code review. Jump to Resource Management and Interfaces for ownership, lifetime, nullability, spans, and parameter design. Use Classes And Types for invariants, rule-of-zero/five, hierarchies, and operators. Use Concurrency And Parallelism for async, locks, atomics, and data races. Use Error Handling for exceptions, `noexcept`, and invariant recovery. Use Templates And Generic Programming for concepts and template APIs. Use Source Files And Namespaces, Standard Library, and C Interop And C-Style Code for project structure and modernization.

## Operating Model

Optimize for readable, type-safe, resource-safe, maintainable C++ that can be checked by compilers, static analysis, tests, and human review. Prefer direct expression of intent over comments that explain obscure code. Prefer abstractions with no avoidable runtime cost over hand-coded low-level mechanics.

The strongest recurring themes are:

- Make contracts explicit: types, names, preconditions, postconditions, ownership, nullability, lifetimes, and failure modes.
- Let scopes and objects manage resources through RAII.
- Use the standard library and well-designed foundation libraries before inventing local mechanisms.
- Prefer compile-time checking, then systematic runtime checking, then documented exceptions.
- Keep interfaces small, strongly typed, and hard to misuse.
- Keep implementation complexity behind stable interfaces.
- Make invalid states unrepresentable where practical.
- Gradually improve old code; do not demand a full rewrite to get value.

## High-Signal Review Checklist

Check these first:

- Ownership: no raw owning `T*`; ownership flows through values, `std::unique_ptr`, `std::shared_ptr`, RAII handles, or explicitly marked legacy `gsl::owner`.
- Lifetime: no references, pointers, iterators, lambdas, coroutines, or async work outliving the object they touch.
- Bounds: arrays and pointer-count pairs become `std::span` or `gsl::span`; prefer `std::array` or `std::vector` over C arrays.
- Nullability: use references for required objects and `not_null` where a pointer shape is unavoidable.
- Initialization: every object starts initialized; invariants are established by constructors or factories.
- Exceptions: constructors throw if they cannot establish invariants; destructors, deallocation, `swap`, and exception moves/copies do not throw.
- Concurrency: no data races; lock with RAII; no unknown callbacks while holding locks; no `volatile` for synchronization.
- C-style constructs: avoid macros, C casts, `malloc`/`free`, naked `new`/`delete`, `memset`/`memcpy` on non-trivial objects, varargs, `setjmp`/`longjmp`, and naked unions.
- Interfaces: argument order and types make misuse hard; related values are grouped into domain types.
- Performance: no optimization claims without measurements; avoid allocations and context switches on hot paths only after identifying them.

## Philosophy

Express intent in code through names, types, scopes, and APIs. Prefer ISO C++, static type safety, compile-time checking, early error detection, immutability by default, non-leaking resource management, and appropriate tools/libraries. Encapsulate necessary low-level or messy code so violations do not spread across interfaces.

Use guideline violations as design pressure: replace error-prone constructs with safer library abstractions, not just comments. For legacy constraints, isolate and document the exception.

## Interfaces

Treat every interface as a contract. Make dependencies explicit, avoid writable globals and singletons, and use strong domain types instead of adjacent same-type parameters. State preconditions and postconditions with `Expects` and `Ensures` where the project uses GSL-style contracts.

Prefer:

- Return values over out parameters.
- `T&` for required mutable objects.
- `const T&` for required read-only non-cheap objects.
- `T*` only when absence is meaningful and ownership is not transferred.
- `not_null<T*>` when pointer syntax is necessary but null is invalid.
- `std::span<T>` for contiguous sequences.
- `std::string_view` for read-only string views.
- `std::unique_ptr<T>` to transfer unique ownership only when value return is unsuitable.
- `std::shared_ptr<T>` only to express shared ownership.

Do not pass arrays as single pointers or transfer ownership through raw pointers/references. Keep argument lists short; group related values into named types. For ABI stability, consider Pimpl or C-compatible boundaries, while keeping calling C++ code idiomatic.

## Functions

Functions should do one logical operation, be short enough to understand, and be named when the operation is reusable. Use lambdas for local one-off function objects, especially captures or complex initialization.

Parameter rules:

- In: pass cheap scalars by value; pass larger inputs by `const&`.
- In-out: pass by non-const reference.
- Will-move-from: pass by `X&&` and move exactly when handing off.
- Forwarding: use forwarding references only in generic forwarding code and forward exactly once.
- Out: prefer return values; return a small named struct for multiple values.
- Optional object: prefer `T*` over nullable reference-like workarounds.

Return rules:

- Never return references or pointers to locals.
- Do not return `T&&`.
- Do not write `return std::move(local)`.
- Assignment returns `T&`.
- `main` returns `int`.

Lambda rules:

- Capture by reference only when the lambda is strictly local.
- Avoid reference captures for stored, returned, heap-owned, threaded, or asynchronous lambdas.
- Avoid `[=]` when capturing `this` or members; spell out intent.

## Classes And Types

Use classes to model invariants and implementation hiding. Use structs for passive aggregates whose members vary independently. Keep members private unless there is no invariant. Make helpers non-members in the same namespace unless they need representation access.

Concrete types:

- Prefer concrete value types over class hierarchies when runtime polymorphism is not needed.
- Make ordinary concrete types regular: copyable, assignable, comparable, and unsurprising.
- Avoid `const` and reference data members in copyable/movable types.
- Declare members in dependency order.

Construction and destruction:

- Follow the rule of zero when possible.
- If defining or deleting copy, move, or destructor behavior, define or delete the full related set.
- Constructors establish fully usable objects or throw.
- Prefer default member initializers and member initialization over assignment in constructor bodies.
- Make single-argument constructors `explicit` by default.
- Do not call virtual functions from constructors or destructors.
- Destructors do not fail and should be `noexcept` when there is doubt.
- Make move operations `noexcept` when possible.
- Use `=default` for explicit default semantics and `=delete` to suppress invalid operations.
- Do not use `memset` or `memcpy` to create or copy non-trivial objects.

Class hierarchies:

- Use inheritance only for real hierarchical concepts, not for simple reuse.
- Prefer pure abstract base classes as interfaces.
- Distinguish interface inheritance from implementation inheritance.
- A polymorphic base destructor is public virtual or protected non-virtual.
- Mark each virtual function with exactly one of `virtual`, `override`, or `final`.
- Avoid protected data and trivial getters/setters that expose representation.
- Use `dynamic_cast` only when hierarchy navigation is unavoidable; prefer virtual dispatch.
- Suppress public copy/move in polymorphic base classes.
- Avoid slicing, especially arrays of derived objects viewed as base objects.

Operators:

- Overload only for conventional meanings.
- Put symmetric operators as non-members in the operand namespace.
- Avoid implicit conversion operators.
- Use `using` declarations to restore overload sets from bases.

Unions:

- Prefer `std::variant` for tagged alternatives.
- Use unions only for deliberate storage overlap and wrap them with a discriminator.
- Do not use unions for type punning; use `std::byte`, `std::bit_cast`, or a named cast where appropriate.

## Enumerations

Use enums for related named constants, not macros. Prefer `enum class` to avoid implicit integer conversions and name collisions. Define operations when they make the enum easier and safer to use. Avoid all-caps enumerators, unnamed enums, unnecessary underlying types, and unnecessary explicit values.

## Resource Management

Resource means anything acquired and released: memory, files, sockets, locks, handles, transactions, and thread joins. Make ownership explicit and automatic.

Rules of thumb:

- Own resources with RAII handles.
- Raw `T*` and `T&` are non-owning by default.
- Prefer scoped objects over heap allocation.
- Avoid writable globals.
- Avoid `malloc`, `free`, explicit `new`, and explicit `delete` outside low-level resource handles.
- Hand explicit allocations immediately to manager objects.
- Do not perform multiple explicit allocations in one expression.
- Prefer `std::make_unique` and `std::make_shared`.
- Prefer `std::unique_ptr` over `std::shared_ptr` unless ownership is genuinely shared.
- Use `std::weak_ptr` to break shared ownership cycles.
- Take smart pointers as parameters only to express lifetime or ownership semantics.
- Do not pass raw pointers/references obtained from aliased smart pointers unless a local smart pointer copy pins the object.

## Expressions And Statements

Prefer standard algorithms and abstractions to hand-written loops and low-level primitives. Keep scopes small and declare variables when a value is available. Always initialize. Prefer braced initialization and `auto` when it removes redundant type noise without hiding important semantics.

Avoid:

- Similar-looking names, all-caps non-macros, reused names in nested scopes, and multi-name declarations.
- Macros for program text, constants, or functions.
- C-style variadic functions.
- Complicated expressions and dependency on evaluation order.
- Magic constants.
- Narrowing conversions.
- `0` or `NULL` for null pointers; use `nullptr`.
- Casts; if unavoidable, use named casts and never cast away `const`.
- Manual `new` and `delete` in ordinary code.
- Pointer comparisons across unrelated arrays.
- Object slicing.
- Dereferencing invalid pointers.

Control flow:

- Prefer `switch` when selecting among discrete cases.
- Prefer range-for when iterating a range.
- Prefer `for` when there is an obvious loop variable, `while` otherwise.
- Declare loop variables in the loop initializer.
- Avoid `do`, `goto`, implicit fallthrough, invisible empty statements, and modifications of raw loop control variables.
- Keep conditions simple and avoid redundant comparisons to boolean values.
- Prefer guard clauses over deep nesting where it improves clarity.

## Performance

Do not optimize without a reason, before measurement, or outside performance-critical paths. Simple high-level code is often faster after optimization than complicated low-level code.

When performance matters:

- Measure before and after.
- Design clean interfaces that leave room for optimization.
- Move safe computation to compile time with `constexpr` or templates only when it pays.
- Eliminate redundant aliases, indirections, allocations, and deallocations on hot paths.
- Avoid allocation and context switches on critical branches.
- Use compact data structures and predictable memory access.
- Remember that space is time on modern hardware.

## Concurrency And Parallelism

Assume library code may run in a multithreaded program. Avoid data races and minimize explicit sharing of writable data. Think in tasks rather than threads.

Concurrency rules:

- Use RAII locks; never rely on paired plain `lock` and `unlock`.
- Use `std::lock` or `std::scoped_lock` for multiple mutexes.
- Never call unknown code while holding a lock.
- Treat joining threads as scoped resources and detached threads as global-like hazards.
- Do not use `volatile` for synchronization; use atomics, mutexes, condition variables, channels, tasks, or higher-level libraries.
- Use tools such as sanitizers, static analysis, stress tests, and thread-aware testing.
- Prefer message passing and futures where it reduces shared state.
- Use `std::async`/futures for simple concurrent tasks when appropriate, but be aware execution policy and thread-pool behavior may matter.
- Keep coroutine captures and referenced state alive across suspension.
- Reserve lock-free code for proven needs and expert review.

## Error Handling

Choose an error strategy early. Exceptions are the default way to report that a function cannot perform its task. Use exceptions only for errors, not ordinary control flow. Design recovery around invariants: objects not destroyed remain valid.

Rules:

- Constructors establish invariants or throw.
- RAII prevents leaks during exceptions.
- State preconditions and postconditions.
- Use `noexcept` where failure is impossible or unacceptable.
- Never throw while directly owning a raw resource.
- Throw purpose-designed exception types by value; catch hierarchy exceptions by reference.
- Destructors, deallocation, `swap`, and exception copy/move operations do not fail.
- Do not catch every exception in every function; catch where useful recovery, translation, logging, or boundary handling occurs.
- Minimize explicit `try`/`catch`; RAII usually removes cleanup catches.
- Use `final_action` only when no proper resource handle exists.
- If exceptions are banned, simulate RAII, use systematic error returns, avoid global error state, and consider fail-fast for unrecoverable cases.
- Avoid deprecated exception specifications and order `catch` clauses from most-specific to most-general.

## Constants And Immutability

Make objects immutable by default. Mark member functions `const` unless they change observable state. Pass pointers/references to `const` unless mutation is intended. Use `const` for runtime values that do not change and `constexpr` for values computable at compile time. Do not cast away `const`.

## Templates And Generic Programming

Use templates to raise abstraction, express reusable algorithms, containers, ranges, and compile-time structure. Use concepts to state semantic requirements on template arguments.

Guidelines:

- Constrain template parameters with standard concepts when available.
- Define concepts by meaningful semantics and use patterns, not just syntax.
- Require a complete operation set for a concept and document axioms when important.
- Keep concepts positive and simple; use negation/disjunction sparingly.
- Pass operations to algorithms as function objects.
- Require only essential properties.
- Prefer `using` aliases over `typedef`.
- Hide template machinery behind aliases and implementation layers.
- Avoid highly visible unconstrained templates with common names.
- Avoid type erasure unless it buys a real boundary.
- Keep template definitions independent of unnecessary context.
- Avoid over-parameterized member templates; move non-dependent parts to non-template bases.
- Use specialization/tag dispatch for alternate implementations, but do not specialize function templates when overloads are the intended mechanism.
- Use `{}` inside templates to avoid parsing and narrowing surprises.
- Treat unqualified non-member calls as customization points only when intended.
- Avoid naively templated class hierarchies and virtual member templates.
- Use variadic templates for heterogeneous argument packs, not homogeneous lists.
- Use template metaprogramming only when ordinary code or `constexpr` functions are insufficient.
- Check intended concept conformance with `static_assert`.

## C Interop And C-Style Code

Prefer C++ to C. If C must be used, keep the common subset and compile it as C++ where practical. Wrap C APIs in C++ interfaces that express ownership, lifetimes, errors, and resources with RAII and strong types.

Avoid C-style habits in C++:

- `void*` conversions.
- `malloc` and `free`.
- raw arrays and pointer arithmetic outside narrow low-level code.
- macros for constants or functions.
- C casts.
- `setjmp`/`longjmp`, which bypass destructors.
- `memset` and `memcpy` on non-trivially-copyable objects.

## Source Files And Namespaces

Separate declarations from definitions. Headers represent interfaces and must be self-contained. A source file includes the header that declares its interface. Avoid cyclic dependencies and hidden include dependencies.

Rules:

- Follow the project file suffix convention; otherwise use common `.cpp` and `.h` style.
- Headers contain declarations, templates, inline/constexpr definitions, aliases, and includes; avoid ordinary object definitions and non-inline function definitions.
- Include headers before other declarations.
- Use include guards or the project-standard equivalent.
- Avoid `using namespace` at global scope in headers.
- Use namespaces for logical structure.
- Use unnamed namespaces for internal implementation entities in source files, not headers.
- Prefer quoted includes for project-relative files and angle includes for external/standard headers.
- Keep include paths portable.

## Standard Library

Use libraries wherever possible, prefer the standard library, and do not add non-standard names to namespace `std`. Use the library in a type-safe way.

Container and string defaults:

- Prefer `std::array` or `std::vector` over C arrays.
- Prefer `std::vector` unless another container has a measured or semantic advantage.
- Avoid bounds errors with ranges, spans, iterators, and algorithms.
- Do not use `memset` or `memcpy` on non-trivially-copyable values.
- Use `std::string` for owning strings.
- Use `std::string_view` for read-only non-owning string views.
- Use `zstring`/`czstring` only to make C-style zero-terminated string assumptions explicit.
- Use `std::byte` for raw bytes that are not characters.
- Use `<chrono>` duration and time-point types instead of raw numeric time units.

## Architecture

Separate stable code from less stable code. Express reusable parts as libraries. Avoid dependency cycles among libraries. Put messy implementation details behind stable interfaces so bad designs do not leak outward.

## Profiles, Tools, And GSL

The guideline profiles focus tool enforcement:

- `type`: avoid type violations through casts, unions, and varargs.
- `bounds`: avoid out-of-range access.
- `lifetime`: avoid leaks, null dereferences, dangling pointers/references, and invalid object access.

Use compilers, warnings, sanitizers, static analysis, linters, formatters, tests, and code review. Suppress guideline diagnostics only locally and intentionally, using the project's accepted suppression mechanism.

GSL concepts and aliases:

- Views are non-owning: raw `T*`, `T&`, spans, string views, `zstring`, and `czstring`.
- Ownership is represented by `std::unique_ptr`, `std::shared_ptr`, resource handles, or legacy `owner<T*>`.
- Assertions use `Expects` and `Ensures`.
- Utilities include `not_null`, `narrow`, `narrow_cast`, and `final_action` where available.

Prefer standard library equivalents when the project baseline supports them, such as `std::span`, `std::byte`, `std::variant`, and `std::string_view`.

## Naming And Layout

Follow local style first. Where no local convention exists, optimize for readability and conventional C++:

- Use meaningful names; short names only for small scopes and conventional roles.
- Avoid all-caps except macros.
- Avoid visually confusable names.
- Keep declarations narrow in scope.
- Keep formatting mechanically consistent with the project.
- Do not turn naming and layout advice into blocking review feedback unless it hides a bug or violates project policy.

## Applying The Guidelines Pragmatically

Do not mechanically rewrite working code to satisfy every rule. Prioritize:

1. Undefined behavior, leaks, data races, dangling lifetimes, and bounds bugs.
2. Interface misuse hazards and unclear ownership.
3. Error handling that leaks resources or leaves invalid state.
4. Simplifications that reduce code while preserving behavior.
5. Performance changes backed by measurement.
6. Style-only consistency issues.

When a rule cannot be followed because of ABI, hardware, real-time, legacy, or interoperability constraints, isolate the exception behind a small interface and explain the tradeoff in code or docs.
