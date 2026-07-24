# CWE Review Views

Use these views to scope coverage and navigate the catalog. A view is not itself a finding or a root-cause mapping.

## Contents

- [CWE-699 Software Development](#cwe-699)
- [CWE-1000 Research Concepts](#cwe-1000)
- [CWE-1003 Weaknesses for Simplified Mapping of Published Vulnerabilities](#cwe-1003)
- [CWE-1435 Weaknesses in the 2025 CWE Top 25 Most Dangerous Software Weaknesses](#cwe-1435)
- [CWE-1344 Weaknesses in OWASP Top Ten (2021)](#cwe-1344)
- [CWE-1450 Weaknesses in OWASP Top Ten RC1 (2025)](#cwe-1450)
- [CWE-1448 Weaknesses Related to AI/ML Products](#cwe-1448)
- [CWE-658 Weaknesses in Software Written in C](#cwe-658)
- [CWE-659 Weaknesses in Software Written in C++](#cwe-659)
- [CWE-660 Weaknesses in Software Written in Java](#cwe-660)
- [CWE-661 Weaknesses in Software Written in PHP](#cwe-661)
- [CWE-701 Weaknesses Introduced During Design](#cwe-701)
- [CWE-702 Weaknesses Introduced During Implementation](#cwe-702)
- [CWE-919 Weaknesses in Mobile Applications](#cwe-919)

## CWE-699

**Software Development**

- Type: Graph
- Status: Draft
- Weakness members: 399
- Review use: Primary software-development browsing view. Use it to scope common review surfaces by development concept.

This view organizes weaknesses around concepts that are frequently used or encountered in software development. This includes all aspects of the software development lifecycle including both architecture and implementation. Accordingly, this view can align closely with the perspectives of architects, developers, educators, and assessment vendors. It provides a variety of categories that are intended to simplify navigation, browsing, and mapping.

Direct members:

- CWE-1228 API / Function Errors [Category]
- CWE-1210 Audit / Logging Errors [Category]
- CWE-1211 Authentication Errors [Category]
- CWE-1212 Authorization Errors [Category]
- CWE-1006 Bad Coding Practices [Category]
- CWE-438 Behavioral Problems [Category]
- CWE-840 Business Logic Errors [Category]
- CWE-417 Communication Channel Errors [Category]
- CWE-1226 Complexity Issues [Category]
- CWE-557 Concurrency Issues [Category]
- CWE-255 Credentials Management Errors [Category]
- CWE-310 Cryptographic Issues [Category]
- CWE-320 Key Management Errors [Category]
- CWE-1214 Data Integrity Issues [Category]
- CWE-19 Data Processing Errors [Category]
- CWE-137 Data Neutralization Issues [Category]
- CWE-1225 Documentation Issues [Category]
- CWE-1219 File Handling Issues [Category]
- CWE-1227 Encapsulation Issues [Category]
- CWE-389 Error Conditions, Return Values, Status Codes [Category]
- CWE-569 Expression Issues [Category]
- CWE-429 Handler Errors [Category]
- CWE-199 Information Management Errors [Category]
- CWE-452 Initialization and Cleanup Errors [Category]
- CWE-1215 Data Validation Issues [Category]
- CWE-1216 Lockout Mechanism Errors [Category]
- CWE-1218 Memory Buffer Errors [Category]
- CWE-189 Numeric Errors [Category]
- CWE-275 Permission Issues [Category]
- CWE-465 Pointer Issues [Category]
- CWE-265 Privilege Issues [Category]
- CWE-1213 Random Number Issues [Category]
- CWE-411 Resource Locking Problems [Category]
- CWE-399 Resource Management Errors [Category]
- CWE-387 Signal Errors [Category]
- CWE-371 State Issues [Category]
- CWE-133 String Errors [Category]
- CWE-136 Type Errors [Category]
- CWE-355 User Interface Security Issues [Category]
- CWE-1217 User Session Errors [Category]

Sample weakness members (20 of 399):

- CWE-15 External Control of System or Configuration Setting
- CWE-22 Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
- CWE-41 Improper Resolution of Path Equivalence
- CWE-59 Improper Link Resolution Before File Access ('Link Following')
- CWE-66 Improper Handling of File Names that Identify Virtual Resources
- CWE-73 External Control of File Name or Path
- CWE-76 Improper Neutralization of Equivalent Special Elements
- CWE-78 Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')
- CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
- CWE-88 Improper Neutralization of Argument Delimiters in a Command ('Argument Injection')
- CWE-89 Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
- CWE-90 Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection')
- CWE-91 XML Injection (aka Blind XPath Injection)
- CWE-93 Improper Neutralization of CRLF Sequences ('CRLF Injection')
- CWE-94 Improper Control of Generation of Code ('Code Injection')
- CWE-112 Missing XML Validation
- CWE-115 Misinterpretation of Input
- CWE-117 Improper Output Neutralization for Logs
- CWE-120 Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')
- CWE-124 Buffer Underwrite ('Buffer Underflow')

## CWE-1000

**Research Concepts**

- Type: Graph
- Status: Draft
- Weakness members: 944
- Review use: Research graph. Use it to move between broad parents and precise child weaknesses while tracing root cause.

This view is intended to facilitate research into weaknesses, including their inter-dependencies, and can be leveraged to systematically identify theoretical gaps within CWE. It is mainly organized according to abstractions of behaviors instead of how they can be detected, where they appear in code, or when they are introduced in the development life cycle. By design, this view is expected to include every weakness within CWE.

Direct members:

- CWE-284 Improper Access Control [Weakness]
- CWE-435 Improper Interaction Between Multiple Correctly-Behaving Entities [Weakness]
- CWE-664 Improper Control of a Resource Through its Lifetime [Weakness]
- CWE-682 Incorrect Calculation [Weakness]
- CWE-691 Insufficient Control Flow Management [Weakness]
- CWE-693 Protection Mechanism Failure [Weakness]
- CWE-697 Incorrect Comparison [Weakness]
- CWE-703 Improper Check or Handling of Exceptional Conditions [Weakness]
- CWE-707 Improper Neutralization [Weakness]
- CWE-710 Improper Adherence to Coding Standards [Weakness]

Sample weakness members (20 of 944):

- CWE-5 J2EE Misconfiguration: Data Transmission Without Encryption
- CWE-6 J2EE Misconfiguration: Insufficient Session-ID Length
- CWE-7 J2EE Misconfiguration: Missing Custom Error Page
- CWE-8 J2EE Misconfiguration: Entity Bean Declared Remote
- CWE-9 J2EE Misconfiguration: Weak Access Permissions for EJB Methods
- CWE-11 ASP.NET Misconfiguration: Creating Debug Binary
- CWE-12 ASP.NET Misconfiguration: Missing Custom Error Page
- CWE-13 ASP.NET Misconfiguration: Password in Configuration File
- CWE-14 Compiler Removal of Code to Clear Buffers
- CWE-15 External Control of System or Configuration Setting
- CWE-20 Improper Input Validation
- CWE-22 Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
- CWE-23 Relative Path Traversal
- CWE-24 Path Traversal: '../filedir'
- CWE-25 Path Traversal: '/../filedir'
- CWE-26 Path Traversal: '/dir/../filename'
- CWE-27 Path Traversal: 'dir/../../filename'
- CWE-28 Path Traversal: '..\filedir'
- CWE-29 Path Traversal: '\..\filename'
- CWE-30 Path Traversal: '\dir\..\filename'

## CWE-1003

**Weaknesses for Simplified Mapping of Published Vulnerabilities**

- Type: Graph
- Status: Incomplete
- Weakness members: 130
- Review use: Simplified vulnerability-mapping graph. Use it when a finding needs a practical mapping candidate before refining it.

CWE entries in this view (graph) may be used to categorize potential weaknesses within sources that handle public, third-party vulnerability information, such as the National Vulnerability Database (NVD). By design, this view is incomplete. It is limited to a small number of the most commonly-seen weaknesses, so that it is easier for humans to use. This view uses a shallow hierarchy of two levels in order to simplify the complex navigation of the entire CWE corpus.

Direct members:

- CWE-20 Improper Input Validation [Weakness]
- CWE-74 Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') [Weakness]
- CWE-116 Improper Encoding or Escaping of Output [Weakness]
- CWE-119 Improper Restriction of Operations within the Bounds of a Memory Buffer [Weakness]
- CWE-200 Exposure of Sensitive Information to an Unauthorized Actor [Weakness]
- CWE-269 Improper Privilege Management [Weakness]
- CWE-287 Improper Authentication [Weakness]
- CWE-311 Missing Encryption of Sensitive Data [Weakness]
- CWE-326 Inadequate Encryption Strength [Weakness]
- CWE-327 Use of a Broken or Risky Cryptographic Algorithm [Weakness]
- CWE-330 Use of Insufficiently Random Values [Weakness]
- CWE-345 Insufficient Verification of Data Authenticity [Weakness]
- CWE-362 Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') [Weakness]
- CWE-400 Uncontrolled Resource Consumption [Weakness]
- CWE-404 Improper Resource Shutdown or Release [Weakness]
- CWE-407 Inefficient Algorithmic Complexity [Weakness]
- CWE-436 Interpretation Conflict [Weakness]
- CWE-610 Externally Controlled Reference to a Resource in Another Sphere [Weakness]
- CWE-662 Improper Synchronization [Weakness]
- CWE-665 Improper Initialization [Weakness]
- CWE-668 Exposure of Resource to Wrong Sphere [Weakness]
- CWE-669 Incorrect Resource Transfer Between Spheres [Weakness]
- CWE-670 Always-Incorrect Control Flow Implementation [Weakness]
- CWE-672 Operation on a Resource after Expiration or Release [Weakness]
- CWE-674 Uncontrolled Recursion [Weakness]
- CWE-682 Incorrect Calculation [Weakness]
- CWE-697 Incorrect Comparison [Weakness]
- CWE-704 Incorrect Type Conversion or Cast [Weakness]
- CWE-706 Use of Incorrectly-Resolved Name or Reference [Weakness]
- CWE-732 Incorrect Permission Assignment for Critical Resource [Weakness]
- CWE-754 Improper Check for Unusual or Exceptional Conditions [Weakness]
- CWE-755 Improper Handling of Exceptional Conditions [Weakness]
- CWE-834 Excessive Iteration [Weakness]
- CWE-862 Missing Authorization [Weakness]
- CWE-863 Incorrect Authorization [Weakness]
- CWE-913 Improper Control of Dynamically-Managed Code Resources [Weakness]
- CWE-922 Insecure Storage of Sensitive Information [Weakness]

Weakness members:

- CWE-20 Improper Input Validation (Class; mapping Discouraged)
- CWE-22 Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') (Base; mapping Allowed-with-Review)
- CWE-59 Improper Link Resolution Before File Access ('Link Following') (Base; mapping Allowed)
- CWE-74 Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') (Class; mapping Discouraged)
- CWE-77 Improper Neutralization of Special Elements used in a Command ('Command Injection') (Class; mapping Allowed-with-Review)
- CWE-78 Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') (Base; mapping Allowed)
- CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') (Base; mapping Allowed)
- CWE-88 Improper Neutralization of Argument Delimiters in a Command ('Argument Injection') (Base; mapping Allowed)
- CWE-89 Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') (Base; mapping Allowed)
- CWE-91 XML Injection (aka Blind XPath Injection) (Base; mapping Allowed-with-Review)
- CWE-94 Improper Control of Generation of Code ('Code Injection') (Base; mapping Allowed-with-Review)
- CWE-116 Improper Encoding or Escaping of Output (Class; mapping Allowed-with-Review)
- CWE-119 Improper Restriction of Operations within the Bounds of a Memory Buffer (Class; mapping Discouraged)
- CWE-120 Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') (Base; mapping Allowed-with-Review)
- CWE-125 Out-of-bounds Read (Base; mapping Allowed)
- CWE-129 Improper Validation of Array Index (Variant; mapping Allowed)
- CWE-131 Incorrect Calculation of Buffer Size (Base; mapping Allowed)
- CWE-134 Use of Externally-Controlled Format String (Base; mapping Allowed)
- CWE-178 Improper Handling of Case Sensitivity (Base; mapping Allowed)
- CWE-190 Integer Overflow or Wraparound (Base; mapping Allowed)
- CWE-191 Integer Underflow (Wrap or Wraparound) (Base; mapping Allowed)
- CWE-193 Off-by-one Error (Base; mapping Allowed)
- CWE-200 Exposure of Sensitive Information to an Unauthorized Actor (Class; mapping Discouraged)
- CWE-203 Observable Discrepancy (Base; mapping Allowed)
- CWE-209 Generation of Error Message Containing Sensitive Information (Base; mapping Allowed)
- CWE-212 Improper Removal of Sensitive Information Before Storage or Transfer (Base; mapping Allowed)
- CWE-252 Unchecked Return Value (Base; mapping Allowed)
- CWE-269 Improper Privilege Management (Class; mapping Discouraged)
- CWE-273 Improper Check for Dropped Privileges (Base; mapping Allowed)
- CWE-276 Incorrect Default Permissions (Base; mapping Allowed)
- CWE-281 Improper Preservation of Permissions (Base; mapping Allowed)
- CWE-287 Improper Authentication (Class; mapping Discouraged)
- CWE-290 Authentication Bypass by Spoofing (Base; mapping Allowed)
- CWE-294 Authentication Bypass by Capture-replay (Base; mapping Allowed)
- CWE-295 Improper Certificate Validation (Base; mapping Allowed)
- CWE-306 Missing Authentication for Critical Function (Base; mapping Allowed)
- CWE-307 Improper Restriction of Excessive Authentication Attempts (Base; mapping Allowed)
- CWE-311 Missing Encryption of Sensitive Data (Class; mapping Discouraged)
- CWE-312 Cleartext Storage of Sensitive Information (Base; mapping Allowed)
- CWE-319 Cleartext Transmission of Sensitive Information (Base; mapping Allowed)
- CWE-326 Inadequate Encryption Strength (Class; mapping Allowed-with-Review)
- CWE-327 Use of a Broken or Risky Cryptographic Algorithm (Class; mapping Allowed-with-Review)
- CWE-330 Use of Insufficiently Random Values (Class; mapping Discouraged)
- CWE-331 Insufficient Entropy (Base; mapping Allowed)
- CWE-335 Incorrect Usage of Seeds in Pseudo-Random Number Generator (PRNG) (Base; mapping Allowed)
- CWE-338 Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG) (Base; mapping Allowed)
- CWE-345 Insufficient Verification of Data Authenticity (Class; mapping Discouraged)
- CWE-346 Origin Validation Error (Class; mapping Allowed-with-Review)
- CWE-347 Improper Verification of Cryptographic Signature (Base; mapping Allowed)
- CWE-352 Cross-Site Request Forgery (CSRF) (Compound; mapping Allowed)
- CWE-354 Improper Validation of Integrity Check Value (Base; mapping Allowed)
- CWE-362 Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') (Class; mapping Allowed-with-Review)
- CWE-367 Time-of-check Time-of-use (TOCTOU) Race Condition (Base; mapping Allowed)
- CWE-369 Divide By Zero (Base; mapping Allowed)
- CWE-384 Session Fixation (Compound; mapping Allowed)
- CWE-400 Uncontrolled Resource Consumption (Class; mapping Discouraged)
- CWE-401 Missing Release of Memory after Effective Lifetime (Variant; mapping Allowed)
- CWE-404 Improper Resource Shutdown or Release (Class; mapping Allowed-with-Review)
- CWE-407 Inefficient Algorithmic Complexity (Class; mapping Allowed-with-Review)
- CWE-415 Double Free (Variant; mapping Allowed)
- CWE-416 Use After Free (Variant; mapping Allowed)
- CWE-425 Direct Request ('Forced Browsing') (Base; mapping Allowed)
- CWE-426 Untrusted Search Path (Base; mapping Allowed-with-Review)
- CWE-427 Uncontrolled Search Path Element (Base; mapping Allowed-with-Review)
- CWE-428 Unquoted Search Path or Element (Base; mapping Allowed)
- CWE-434 Unrestricted Upload of File with Dangerous Type (Base; mapping Allowed)
- CWE-436 Interpretation Conflict (Class; mapping Allowed-with-Review)
- CWE-444 Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling') (Base; mapping Allowed)
- CWE-459 Incomplete Cleanup (Base; mapping Allowed)
- CWE-470 Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection') (Base; mapping Allowed)
- CWE-476 NULL Pointer Dereference (Base; mapping Allowed)
- CWE-494 Download of Code Without Integrity Check (Base; mapping Allowed)
- CWE-502 Deserialization of Untrusted Data (Base; mapping Allowed)
- CWE-521 Weak Password Requirements (Base; mapping Allowed)
- CWE-522 Insufficiently Protected Credentials (Class; mapping Allowed-with-Review)
- CWE-532 Insertion of Sensitive Information into Log File (Base; mapping Allowed)
- CWE-552 Files or Directories Accessible to External Parties (Base; mapping Allowed)
- CWE-565 Reliance on Cookies without Validation and Integrity Checking (Base; mapping Allowed)
- CWE-601 URL Redirection to Untrusted Site ('Open Redirect') (Base; mapping Allowed)
- CWE-610 Externally Controlled Reference to a Resource in Another Sphere (Class; mapping Discouraged)
- CWE-611 Improper Restriction of XML External Entity Reference (Base; mapping Allowed)
- CWE-613 Insufficient Session Expiration (Base; mapping Allowed-with-Review)
- CWE-617 Reachable Assertion (Base; mapping Allowed)
- CWE-639 Authorization Bypass Through User-Controlled Key (Base; mapping Allowed)
- CWE-640 Weak Password Recovery Mechanism for Forgotten Password (Base; mapping Allowed-with-Review)
- CWE-662 Improper Synchronization (Class; mapping Discouraged)
- CWE-665 Improper Initialization (Class; mapping Discouraged)
- CWE-667 Improper Locking (Class; mapping Allowed-with-Review)
- CWE-668 Exposure of Resource to Wrong Sphere (Class; mapping Discouraged)
- CWE-669 Incorrect Resource Transfer Between Spheres (Class; mapping Allowed-with-Review)
- CWE-670 Always-Incorrect Control Flow Implementation (Class; mapping Allowed-with-Review)
- CWE-672 Operation on a Resource after Expiration or Release (Class; mapping Allowed-with-Review)
- CWE-674 Uncontrolled Recursion (Class; mapping Allowed-with-Review)
- CWE-681 Incorrect Conversion between Numeric Types (Base; mapping Allowed)
- CWE-682 Incorrect Calculation (Pillar; mapping Discouraged)
- CWE-697 Incorrect Comparison (Pillar; mapping Discouraged)
- CWE-704 Incorrect Type Conversion or Cast (Class; mapping Allowed-with-Review)
- CWE-706 Use of Incorrectly-Resolved Name or Reference (Class; mapping Allowed-with-Review)
- CWE-732 Incorrect Permission Assignment for Critical Resource (Class; mapping Allowed-with-Review)
- CWE-754 Improper Check for Unusual or Exceptional Conditions (Class; mapping Allowed-with-Review)
- CWE-755 Improper Handling of Exceptional Conditions (Class; mapping Discouraged)
- CWE-763 Release of Invalid Pointer or Reference (Base; mapping Allowed)
- CWE-770 Allocation of Resources Without Limits or Throttling (Base; mapping Allowed)
- CWE-772 Missing Release of Resource after Effective Lifetime (Base; mapping Allowed)
- CWE-776 Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion') (Base; mapping Allowed)
- CWE-787 Out-of-bounds Write (Base; mapping Allowed-with-Review)
- CWE-798 Use of Hard-coded Credentials (Base; mapping Allowed-with-Review)
- CWE-824 Access of Uninitialized Pointer (Base; mapping Allowed)
- CWE-829 Inclusion of Functionality from Untrusted Control Sphere (Base; mapping Allowed)
- CWE-834 Excessive Iteration (Class; mapping Discouraged)
- CWE-835 Loop with Unreachable Exit Condition ('Infinite Loop') (Base; mapping Allowed)
- CWE-838 Inappropriate Encoding for Output Context (Base; mapping Allowed)
- CWE-843 Access of Resource Using Incompatible Type ('Type Confusion') (Base; mapping Allowed)
- CWE-862 Missing Authorization (Class; mapping Allowed-with-Review)
- CWE-863 Incorrect Authorization (Class; mapping Allowed-with-Review)
- CWE-908 Use of Uninitialized Resource (Base; mapping Allowed)
- CWE-909 Missing Initialization of Resource (Class; mapping Allowed-with-Review)
- CWE-913 Improper Control of Dynamically-Managed Code Resources (Class; mapping Allowed-with-Review)
- CWE-916 Use of Password Hash With Insufficient Computational Effort (Base; mapping Allowed)
- CWE-917 Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') (Base; mapping Allowed)
- CWE-918 Server-Side Request Forgery (SSRF) (Base; mapping Allowed)
- CWE-920 Improper Restriction of Power Consumption (Base; mapping Allowed)
- CWE-922 Insecure Storage of Sensitive Information (Class; mapping Allowed-with-Review)
- CWE-924 Improper Enforcement of Message Integrity During Transmission in a Communication Channel (Base; mapping Allowed)
- CWE-1021 Improper Restriction of Rendered UI Layers or Frames (Base; mapping Allowed)
- CWE-1188 Initialization of a Resource with an Insecure Default (Base; mapping Allowed)
- CWE-1236 Improper Neutralization of Formula Elements in a CSV File (Base; mapping Allowed)
- CWE-1284 Improper Validation of Specified Quantity in Input (Base; mapping Allowed)
- CWE-1321 Improperly Controlled Modification of Object Prototype Attributes ('Prototype Pollution') (Variant; mapping Allowed)
- CWE-1333 Inefficient Regular Expression Complexity (Base; mapping Allowed)

## CWE-1435

**Weaknesses in the 2025 CWE Top 25 Most Dangerous Software Weaknesses**

- Type: Graph
- Status: Draft
- Weakness members: 25
- Review use: 2025 CWE Top 25 view from this catalog release. Use it as prioritization context, never as proof of severity.

CWE entries in this view are listed in the 2025 CWE Top 25 Most Dangerous Software Weaknesses.

Ordered direct members:

1. CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') [Weakness]
2. CWE-89 Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') [Weakness]
3. CWE-352 Cross-Site Request Forgery (CSRF) [Weakness]
4. CWE-862 Missing Authorization [Weakness]
5. CWE-787 Out-of-bounds Write [Weakness]
6. CWE-22 Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') [Weakness]
7. CWE-416 Use After Free [Weakness]
8. CWE-125 Out-of-bounds Read [Weakness]
9. CWE-78 Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') [Weakness]
10. CWE-94 Improper Control of Generation of Code ('Code Injection') [Weakness]
11. CWE-120 Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') [Weakness]
12. CWE-434 Unrestricted Upload of File with Dangerous Type [Weakness]
13. CWE-476 NULL Pointer Dereference [Weakness]
14. CWE-121 Stack-based Buffer Overflow [Weakness]
15. CWE-502 Deserialization of Untrusted Data [Weakness]
16. CWE-122 Heap-based Buffer Overflow [Weakness]
17. CWE-863 Incorrect Authorization [Weakness]
18. CWE-20 Improper Input Validation [Weakness]
19. CWE-284 Improper Access Control [Weakness]
20. CWE-200 Exposure of Sensitive Information to an Unauthorized Actor [Weakness]
21. CWE-306 Missing Authentication for Critical Function [Weakness]
22. CWE-918 Server-Side Request Forgery (SSRF) [Weakness]
23. CWE-77 Improper Neutralization of Special Elements used in a Command ('Command Injection') [Weakness]
24. CWE-639 Authorization Bypass Through User-Controlled Key [Weakness]
25. CWE-770 Allocation of Resources Without Limits or Throttling [Weakness]

Sample weakness members (20 of 25):

- CWE-20 Improper Input Validation
- CWE-22 Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
- CWE-77 Improper Neutralization of Special Elements used in a Command ('Command Injection')
- CWE-78 Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')
- CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
- CWE-89 Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
- CWE-94 Improper Control of Generation of Code ('Code Injection')
- CWE-120 Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')
- CWE-121 Stack-based Buffer Overflow
- CWE-122 Heap-based Buffer Overflow
- CWE-125 Out-of-bounds Read
- CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
- CWE-284 Improper Access Control
- CWE-306 Missing Authentication for Critical Function
- CWE-352 Cross-Site Request Forgery (CSRF)
- CWE-416 Use After Free
- CWE-434 Unrestricted Upload of File with Dangerous Type
- CWE-476 NULL Pointer Dereference
- CWE-502 Deserialization of Untrusted Data
- CWE-639 Authorization Bypass Through User-Controlled Key

## CWE-1344

**Weaknesses in OWASP Top Ten (2021)**

- Type: Graph
- Status: Incomplete
- Weakness members: 182
- Review use: OWASP Top Ten 2021 view. Use it when a review or report must align findings with the OWASP 2021 grouping.

CWE entries in this view (graph) are associated with the OWASP Top Ten, as released in 2021.

Direct members:

- CWE-1345 OWASP Top Ten 2021 Category A01:2021 - Broken Access Control [Category]
- CWE-1346 OWASP Top Ten 2021 Category A02:2021 - Cryptographic Failures [Category]
- CWE-1347 OWASP Top Ten 2021 Category A03:2021 - Injection [Category]
- CWE-1348 OWASP Top Ten 2021 Category A04:2021 - Insecure Design [Category]
- CWE-1349 OWASP Top Ten 2021 Category A05:2021 - Security Misconfiguration [Category]
- CWE-1352 OWASP Top Ten 2021 Category A06:2021 - Vulnerable and Outdated Components [Category]
- CWE-1353 OWASP Top Ten 2021 Category A07:2021 - Identification and Authentication Failures [Category]
- CWE-1354 OWASP Top Ten 2021 Category A08:2021 - Software and Data Integrity Failures [Category]
- CWE-1355 OWASP Top Ten 2021 Category A09:2021 - Security Logging and Monitoring Failures [Category]
- CWE-1356 OWASP Top Ten 2021 Category A10:2021 - Server-Side Request Forgery (SSRF) [Category]

Sample weakness members (20 of 182):

- CWE-11 ASP.NET Misconfiguration: Creating Debug Binary
- CWE-13 ASP.NET Misconfiguration: Password in Configuration File
- CWE-15 External Control of System or Configuration Setting
- CWE-20 Improper Input Validation
- CWE-22 Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
- CWE-23 Relative Path Traversal
- CWE-35 Path Traversal: '.../...//'
- CWE-59 Improper Link Resolution Before File Access ('Link Following')
- CWE-73 External Control of File Name or Path
- CWE-74 Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')
- CWE-75 Failure to Sanitize Special Elements into a Different Plane (Special Element Injection)
- CWE-77 Improper Neutralization of Special Elements used in a Command ('Command Injection')
- CWE-78 Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')
- CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
- CWE-80 Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS)
- CWE-83 Improper Neutralization of Script in Attributes in a Web Page
- CWE-87 Improper Neutralization of Alternate XSS Syntax
- CWE-88 Improper Neutralization of Argument Delimiters in a Command ('Argument Injection')
- CWE-89 Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
- CWE-90 Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection')

## CWE-1450

**Weaknesses in OWASP Top Ten RC1 (2025)**

- Type: Graph
- Status: Incomplete
- Weakness members: 246
- Review use: OWASP Top Ten 2025 RC1 view. Use it only when the RC1 taxonomy is specifically relevant.

CWE entries in this view (graph) are associated with the first release candidate (RC1) of the OWASP Top Ten, as released in 2025.

Direct members:

- CWE-1436 OWASP Top Ten 2025 Category A01:2025 - Broken Access Control [Category]
- CWE-1437 OWASP Top Ten 2025 Category A02:2025 - Security Misconfiguration [Category]
- CWE-1438 OWASP Top Ten 2025 Category A03:2025 - Software Supply Chain Failures [Category]
- CWE-1439 OWASP Top Ten 2025 Category A04:2025 - Cryptographic Failures [Category]
- CWE-1440 OWASP Top Ten 2025 Category A05:2025 - Injection [Category]
- CWE-1441 OWASP Top Ten 2025 Category A06:2025 - Insecure Design [Category]
- CWE-1442 OWASP Top Ten 2025 Category A07:2025 - Authentication Failures [Category]
- CWE-1443 OWASP Top Ten 2025 Category A08:2025 - Software or Data Integrity Failures [Category]
- CWE-1444 OWASP Top Ten 2025 Category A09:2025 - Logging & Alerting Failures [Category]
- CWE-1445 OWASP Top Ten 2025 Category A10:2025 - Mishandling of Exceptional Conditions [Category]

Sample weakness members (20 of 246):

- CWE-5 J2EE Misconfiguration: Data Transmission Without Encryption
- CWE-11 ASP.NET Misconfiguration: Creating Debug Binary
- CWE-13 ASP.NET Misconfiguration: Password in Configuration File
- CWE-15 External Control of System or Configuration Setting
- CWE-20 Improper Input Validation
- CWE-22 Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
- CWE-23 Relative Path Traversal
- CWE-36 Absolute Path Traversal
- CWE-59 Improper Link Resolution Before File Access ('Link Following')
- CWE-61 UNIX Symbolic Link (Symlink) Following
- CWE-65 Windows Hard Link
- CWE-73 External Control of File Name or Path
- CWE-74 Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')
- CWE-76 Improper Neutralization of Equivalent Special Elements
- CWE-77 Improper Neutralization of Special Elements used in a Command ('Command Injection')
- CWE-78 Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')
- CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
- CWE-80 Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS)
- CWE-83 Improper Neutralization of Script in Attributes in a Web Page
- CWE-86 Improper Neutralization of Invalid Characters in Identifiers in Web Pages

## CWE-1448

**Weaknesses Related to AI/ML Products**

- Type: Graph
- Status: Incomplete
- Weakness members: 17
- Review use: AI/ML product view. Use it when model inputs, training, inference, or agentic behavior are in scope.

CWE entries in this view (graph) are unique to AI/ML products, or are commonly encountered in products that use or support AI/ML.

Direct members:

- CWE-1446 Weaknesses That are Specific to AI/ML Technology [Category]
- CWE-1447 General Software Weaknesses that Appear in Products that Use or Support AI/ML Technology [Category]

Weakness members:

- CWE-22 Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') (Base; mapping Allowed-with-Review)
- CWE-77 Improper Neutralization of Special Elements used in a Command ('Command Injection') (Class; mapping Allowed-with-Review)
- CWE-78 Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') (Base; mapping Allowed)
- CWE-79 Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') (Base; mapping Allowed)
- CWE-94 Improper Control of Generation of Code ('Code Injection') (Base; mapping Allowed-with-Review)
- CWE-95 Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') (Variant; mapping Allowed)
- CWE-116 Improper Encoding or Escaping of Output (Class; mapping Allowed-with-Review)
- CWE-250 Execution with Unnecessary Privileges (Base; mapping Allowed)
- CWE-434 Unrestricted Upload of File with Dangerous Type (Base; mapping Allowed)
- CWE-502 Deserialization of Untrusted Data (Base; mapping Allowed)
- CWE-862 Missing Authorization (Class; mapping Allowed-with-Review)
- CWE-918 Server-Side Request Forgery (SSRF) (Base; mapping Allowed)
- CWE-1039 Inadequate Detection or Handling of Adversarial Input Perturbations in Automated Recognition Mechanism (Class; mapping Allowed-with-Review)
- CWE-1336 Improper Neutralization of Special Elements Used in a Template Engine (Base; mapping Allowed)
- CWE-1426 Improper Validation of Generative AI Output (Base; mapping Discouraged)
- CWE-1427 Improper Neutralization of Input Used for LLM Prompting (Base; mapping Allowed)
- CWE-1434 Insecure Setting of Generative AI/ML Model Inference Parameters (Base; mapping Allowed)

## CWE-658

**Weaknesses in Software Written in C**

- Type: Implicit
- Status: Draft
- Weakness members: 103
- Review use: Implicit C-language view.

This view (slice) covers issues that are found in C programs that are not common to all languages.

Filter: `/Weakness_Catalog/Weaknesses/Weakness[./Applicable_Platforms/Language/@Name='C']`

Sample weakness members (20 of 103):

- CWE-14 Compiler Removal of Code to Clear Buffers
- CWE-119 Improper Restriction of Operations within the Bounds of a Memory Buffer
- CWE-120 Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')
- CWE-121 Stack-based Buffer Overflow
- CWE-122 Heap-based Buffer Overflow
- CWE-123 Write-what-where Condition
- CWE-124 Buffer Underwrite ('Buffer Underflow')
- CWE-125 Out-of-bounds Read
- CWE-126 Buffer Over-read
- CWE-127 Buffer Under-read
- CWE-128 Wrap-around Error
- CWE-129 Improper Validation of Array Index
- CWE-130 Improper Handling of Length Parameter Inconsistency
- CWE-131 Incorrect Calculation of Buffer Size
- CWE-134 Use of Externally-Controlled Format String
- CWE-135 Incorrect Calculation of Multi-Byte String Length
- CWE-158 Improper Neutralization of Null Byte or NUL Character
- CWE-170 Improper Null Termination
- CWE-188 Reliance on Data/Memory Layout
- CWE-190 Integer Overflow or Wraparound

## CWE-659

**Weaknesses in Software Written in C++**

- Type: Implicit
- Status: Draft
- Weakness members: 97
- Review use: Implicit C++-language view.

This view (slice) covers issues that are found in C++ programs that are not common to all languages.

Filter: `/Weakness_Catalog/Weaknesses/Weakness[./Applicable_Platforms/Language/@Name='C++']`

Sample weakness members (20 of 97):

- CWE-14 Compiler Removal of Code to Clear Buffers
- CWE-119 Improper Restriction of Operations within the Bounds of a Memory Buffer
- CWE-120 Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')
- CWE-121 Stack-based Buffer Overflow
- CWE-122 Heap-based Buffer Overflow
- CWE-123 Write-what-where Condition
- CWE-124 Buffer Underwrite ('Buffer Underflow')
- CWE-125 Out-of-bounds Read
- CWE-126 Buffer Over-read
- CWE-127 Buffer Under-read
- CWE-128 Wrap-around Error
- CWE-129 Improper Validation of Array Index
- CWE-130 Improper Handling of Length Parameter Inconsistency
- CWE-131 Incorrect Calculation of Buffer Size
- CWE-134 Use of Externally-Controlled Format String
- CWE-135 Incorrect Calculation of Multi-Byte String Length
- CWE-158 Improper Neutralization of Null Byte or NUL Character
- CWE-170 Improper Null Termination
- CWE-188 Reliance on Data/Memory Layout
- CWE-191 Integer Underflow (Wrap or Wraparound)

## CWE-660

**Weaknesses in Software Written in Java**

- Type: Implicit
- Status: Draft
- Weakness members: 84
- Review use: Implicit Java-language view.

This view (slice) covers issues that are found in Java programs that are not common to all languages.

Filter: `/Weakness_Catalog/Weaknesses/Weakness[./Applicable_Platforms/Language/@Name='Java']`

Sample weakness members (20 of 84):

- CWE-5 J2EE Misconfiguration: Data Transmission Without Encryption
- CWE-6 J2EE Misconfiguration: Insufficient Session-ID Length
- CWE-7 J2EE Misconfiguration: Missing Custom Error Page
- CWE-8 J2EE Misconfiguration: Entity Bean Declared Remote
- CWE-9 J2EE Misconfiguration: Weak Access Permissions for EJB Methods
- CWE-95 Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')
- CWE-102 Struts: Duplicate Validation Forms
- CWE-103 Struts: Incomplete validate() Method Definition
- CWE-104 Struts: Form Bean Does Not Extend Validation Class
- CWE-105 Struts: Form Field Without Validator
- CWE-106 Struts: Plug-in Framework not in Use
- CWE-107 Struts: Unused Validation Form
- CWE-108 Struts: Unvalidated Action Form
- CWE-109 Struts: Validator Turned Off
- CWE-110 Struts: Validator Without Form Field
- CWE-111 Direct Use of Unsafe JNI
- CWE-191 Integer Underflow (Wrap or Wraparound)
- CWE-192 Integer Coercion Error
- CWE-197 Numeric Truncation Error
- CWE-209 Generation of Error Message Containing Sensitive Information

## CWE-661

**Weaknesses in Software Written in PHP**

- Type: Implicit
- Status: Draft
- Weakness members: 26
- Review use: Implicit PHP-language view.

This view (slice) covers issues that are found in PHP programs that are not common to all languages.

Filter: `/Weakness_Catalog/Weaknesses/Weakness[./Applicable_Platforms/Language/@Name='PHP']`

Sample weakness members (20 of 26):

- CWE-88 Improper Neutralization of Argument Delimiters in a Command ('Argument Injection')
- CWE-95 Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')
- CWE-96 Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection')
- CWE-98 Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion')
- CWE-209 Generation of Error Message Containing Sensitive Information
- CWE-211 Externally-Generated Error Message Containing Sensitive Information
- CWE-434 Unrestricted Upload of File with Dangerous Type
- CWE-453 Insecure Default Variable Initialization
- CWE-454 External Initialization of Trusted Variables or Data Stores
- CWE-457 Use of Uninitialized Variable
- CWE-470 Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection')
- CWE-473 PHP External Variable Modification
- CWE-474 Use of Function with Inconsistent Implementations
- CWE-484 Omitted Break Statement in Switch
- CWE-502 Deserialization of Untrusted Data
- CWE-595 Comparison of Object References Instead of Object Contents
- CWE-597 Use of Wrong Operator in String Comparison
- CWE-616 Incomplete Identification of Uploaded File Variables (PHP)
- CWE-621 Variable Extraction Error
- CWE-624 Executable Regular Expression Error

## CWE-701

**Weaknesses Introduced During Design**

- Type: Implicit
- Status: Incomplete
- Weakness members: 297
- Review use: Implicit design-introduction view.

This view (slice) lists weaknesses that can be introduced during design.

Filter: `/Weakness_Catalog/Weaknesses/Weakness[(@Abstraction='Base') or (@Abstraction='Class')][./Modes_Of_Introduction/Introduction/Phase='Architecture and Design']`

Sample weakness members (20 of 297):

- CWE-20 Improper Input Validation
- CWE-73 External Control of File Name or Path
- CWE-99 Improper Control of Resource Identifiers ('Resource Injection')
- CWE-115 Misinterpretation of Input
- CWE-184 Incomplete List of Disallowed Inputs
- CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
- CWE-201 Insertion of Sensitive Information Into Sent Data
- CWE-202 Exposure of Sensitive Information Through Data Queries
- CWE-203 Observable Discrepancy
- CWE-204 Observable Response Discrepancy
- CWE-205 Observable Behavioral Discrepancy
- CWE-208 Observable Timing Discrepancy
- CWE-209 Generation of Error Message Containing Sensitive Information
- CWE-210 Self-generated Error Message Containing Sensitive Information
- CWE-211 Externally-Generated Error Message Containing Sensitive Information
- CWE-212 Improper Removal of Sensitive Information Before Storage or Transfer
- CWE-213 Exposure of Sensitive Information Due to Incompatible Policies
- CWE-214 Invocation of Process Using Visible Sensitive Information
- CWE-221 Information Loss or Omission
- CWE-223 Omission of Security-relevant Information

## CWE-702

**Weaknesses Introduced During Implementation**

- Type: Implicit
- Status: Incomplete
- Weakness members: 835
- Review use: Implicit implementation-introduction view.

This view (slice) lists weaknesses that can be introduced during implementation.

Filter: `/Weakness_Catalog/Weaknesses/Weakness[./Modes_Of_Introduction/Introduction/Phase='Implementation']`

Sample weakness members (20 of 835):

- CWE-5 J2EE Misconfiguration: Data Transmission Without Encryption
- CWE-6 J2EE Misconfiguration: Insufficient Session-ID Length
- CWE-7 J2EE Misconfiguration: Missing Custom Error Page
- CWE-8 J2EE Misconfiguration: Entity Bean Declared Remote
- CWE-9 J2EE Misconfiguration: Weak Access Permissions for EJB Methods
- CWE-11 ASP.NET Misconfiguration: Creating Debug Binary
- CWE-12 ASP.NET Misconfiguration: Missing Custom Error Page
- CWE-13 ASP.NET Misconfiguration: Password in Configuration File
- CWE-14 Compiler Removal of Code to Clear Buffers
- CWE-15 External Control of System or Configuration Setting
- CWE-20 Improper Input Validation
- CWE-22 Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
- CWE-23 Relative Path Traversal
- CWE-24 Path Traversal: '../filedir'
- CWE-25 Path Traversal: '/../filedir'
- CWE-26 Path Traversal: '/dir/../filename'
- CWE-27 Path Traversal: 'dir/../../filename'
- CWE-28 Path Traversal: '..\filedir'
- CWE-29 Path Traversal: '\..\filename'
- CWE-30 Path Traversal: '\dir\..\filename'

## CWE-919

**Weaknesses in Mobile Applications**

- Type: Implicit
- Status: Incomplete
- Weakness members: 21
- Review use: Implicit mobile-application view.

CWE entries in this view (slice) are often seen in mobile applications.

Filter: `/Weakness_Catalog/Weaknesses/Weakness[./Applicable_Platforms/Technology/@Class='Mobile']`

Sample weakness members (20 of 21):

- CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
- CWE-250 Execution with Unnecessary Privileges
- CWE-295 Improper Certificate Validation
- CWE-297 Improper Validation of Certificate with Host Mismatch
- CWE-312 Cleartext Storage of Sensitive Information
- CWE-319 Cleartext Transmission of Sensitive Information
- CWE-359 Exposure of Private Personal Information to an Unauthorized Actor
- CWE-362 Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')
- CWE-511 Logic/Time Bomb
- CWE-602 Client-Side Enforcement of Server-Side Security
- CWE-672 Operation on a Resource after Expiration or Release
- CWE-772 Missing Release of Resource after Effective Lifetime
- CWE-798 Use of Hard-coded Credentials
- CWE-920 Improper Restriction of Power Consumption
- CWE-921 Storage of Sensitive Data in a Mechanism without Access Control
- CWE-925 Improper Verification of Intent by Broadcast Receiver
- CWE-926 Improper Export of Android Application Components
- CWE-927 Use of Implicit Intent for Sensitive Communication
- CWE-939 Improper Authorization in Handler for Custom URL Scheme
- CWE-940 Improper Verification of Source of a Communication Channel
