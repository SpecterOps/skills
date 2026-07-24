# CWE Schema Guide

Generated from the local CWE XSD. Use this file when interpreting field meaning, relationship semantics, or allowed vocabulary.

## Contents

- [Schema Metadata](#schema-metadata)
- [Core Complex Types](#core-complex-types)
- [Enumerations](#enumerations)

## Schema Metadata

- Name: Core Definition
- Version: 7.3
- Date: December 11, 2025

## Core Complex Types

### WeaknessType

A weakness is a mistake or condition that, if left unaddressed, could under the proper conditions contribute to a cyber-enabled capability being vulnerable to attack, allowing an adversary to make items function in unintended ways. This complexType is used to describe a specific type of weakness and provide a variety of information related to it. The required Description should be short and limited to the key points that define this weakness. The optional Extended_Description element provides a place for additional details important to this weakness, but that are not necessary to convey the fundamental concept behind the weakness. A number of other optional elements are available, each of which is described in more detail within the corresponding complexType that it references. The required ID attribute provides a unique identifier for the entry. It is considered static for the lifeti...

| Element | Type | Cardinality |
| --- | --- | --- |
| Description | xs:string | 1..1 |
| Extended_Description | cwe:StructuredTextType | 0..1 |
| Related_Weaknesses | cwe:RelatedWeaknessesType | 0..1 |
| Weakness_Ordinalities | cwe:WeaknessOrdinalitiesType | 0..1 |
| Applicable_Platforms | cwe:ApplicablePlatformsType | 0..1 |
| Background_Details | cwe:BackgroundDetailsType | 0..1 |
| Alternate_Terms | cwe:AlternateTermsType | 0..1 |
| Modes_Of_Introduction | cwe:ModesOfIntroductionType | 0..1 |
| Exploitation_Factors | cwe:ExploitationFactorsType | 0..1 |
| Likelihood_Of_Exploit | cwe:LikelihoodEnumeration | 0..1 |
| Common_Consequences | cwe:CommonConsequencesType | 0..1 |
| Detection_Methods | cwe:DetectionMethodsType | 0..1 |
| Potential_Mitigations | cwe:PotentialMitigationsType | 0..1 |
| Demonstrative_Examples | cwe:DemonstrativeExamplesType | 0..1 |
| Observed_Examples | cwe:ObservedExampleType | 0..1 |
| Functional_Areas | cwe:FunctionalAreasType | 0..1 |
| Affected_Resources | cwe:AffectedResourcesType | 0..1 |
| Taxonomy_Mappings | cwe:TaxonomyMappingsType | 0..1 |
| Related_Attack_Patterns | cwe:RelatedAttackPatternsType | 0..1 |
| References | cwe:ReferencesType | 0..1 |
| Mapping_Notes | cwe:MappingNotesType | 1..1 |
| Notes | cwe:NotesType | 0..1 |
| Content_History | cwe:ContentHistoryType | 1..1 |

| Attribute | Type | Use |
| --- | --- | --- |
| ID | xs:integer | required |
| Name | xs:string | required |
| Abstraction | cwe:AbstractionEnumeration | required |
| Structure | cwe:StructureEnumeration | required |
| Status | cwe:StatusEnumeration | required |
| Diagram | xs:string | optional |

### MappingNotesType

The MappingNotesType complex type provides guidance for when (and whether) to map an issue to this CWE entry or to suggest alternatives. The Usage element describes whether the CWE should be used for mapping vulnerabilities to their underlying weaknesses as part of root cause analysis. The Rationale element provides context for the Usage. The Comments element provides further clarification to the reader. The Reasons element uses a limited vocabulary to summarize the Usage. The Suggestions element includes suggestions for additional CWEs that might be more appropriate for the mapping task.

| Element | Type | Cardinality |
| --- | --- | --- |
| Usage | cwe:UsageEnumeration | 1..1 |
| Rationale | cwe:StructuredTextType | 1..1 |
| Comments | cwe:StructuredTextType | 1..1 |
| Reasons | cwe:ReasonsType | 1..1 |
| Suggestions | cwe:SuggestionsType | 0..1 |

### RelatedWeaknessesType

The RelatedWeaknessesType complex type is used to refer to other weaknesses that differ only in their level of abstraction. It contains one or more Related_Weakness elements, each of which is used to link to the CWE identifier of the other Weakness. The nature of the relation is captured by the Nature attribute. Please see the RelatedNatureEnumeration simple type definition for details about the valid value and meanings. The optional Chain_ID attribute specifies the unique ID of a named chain that a CanFollow or CanPrecede relationship pertains to. The optional Ordinal attribute is used to determine if this relationship is the primary ChildOf relationship for this weakness for a given View_ID. This attribute can only have the value "Primary" and should only be included for the primary parent/child relationship. For each unique triple of <Nature, CWE_ID, View_ID>, there should be only...

| Element | Type | Cardinality |
| --- | --- | --- |
| Related_Weakness | inline type | 1..unbounded |

### RelationshipsType

The RelationshipsType complex type provides elements to show the associated relationships with a given view or category. The Member_Of element is used to denote the individual categories that are included as part of the target view. The Has_Member element is used to define the weaknesses or other categories that are grouped together by a category. In both cases, the required MemberType's CWE_ID attribute specifies the unique CWE ID that is the target entry of the relationship, while the View_ID specifies which view the given relationship is relevant to.

### ModesOfIntroductionType

The ModeOfIntroductionType complex type is used to provide information about how and when a given weakness may be introduced. If there are multiple possible introduction points, then a separate Introduction element should be included for each. The required Phase element identifies the point in the product life cycle at which the weakness may be introduced. The optional Note element identifies the typical scenarios under which the weakness may be introduced during the given phase.

| Element | Type | Cardinality |
| --- | --- | --- |
| Introduction | inline type | 1..unbounded |

### ApplicablePlatformsType

The ApplicablePlatformsType complex type specifies the languages, operating systems, architectures, and technologies in which a given weakness could appear. A technology represents a generally accepted feature of a system and often refers to a high-level functional component within a system. The required Prevalence attribute identifies the regularity with which the weakness is applicable to that platform. When providing an operating system name, an optional Common Platform Enumeration (CPE) identifier can be used to a identify a specific OS.

| Element | Type | Cardinality |
| --- | --- | --- |
| Language | inline type | 0..unbounded |
| Operating_System | inline type | 0..unbounded |
| Architecture | inline type | 0..unbounded |
| Technology | inline type | 0..unbounded |

### FunctionalAreasType

The FunctionalAreasType complex type contains one or more functional_area elements, each of which identifies the functional area in which the weakness is most likely to occur. For example, CWE-23: Relative Path Traversal may occur in functional areas of software related to file processing. Each applicable functional area should have a new Functional_Area element, and standard title capitalization should be applied to each area.

| Element | Type | Cardinality |
| --- | --- | --- |
| Functional_Area | cwe:FunctionalAreaEnumeration | 1..unbounded |

### CommonConsequencesType

The CommonConsequencesType complex type is used to specify individual consequences associated with a weakness. The required Scope element identifies the security property that is violated. The optional Impact element describes the technical impact that arises if an adversary succeeds in exploiting this weakness. The optional Likelihood element identifies how likely the specific consequence is expected to be seen relative to the other consequences. For example, there may be high likelihood that a weakness will be exploited to achieve a certain impact, but a low likelihood that it will be exploited to achieve a different impact. The optional Note element provides additional commentary about a consequence. The optional Consequence_ID attribute is used by the internal CWE team to uniquely identify examples that are repeated across any number of individual weaknesses. To help make sure tha...

| Element | Type | Cardinality |
| --- | --- | --- |
| Consequence | inline type | 1..unbounded |

### DetectionMethodsType

The DetectionMethodsType complex type is used to identify methods that may be employed to detect this weakness, including their strengths and limitations. The required Method element identifies the particular detection method being described. The required Description element is intended to provide some context of how this method can be applied to a specific weakness. The optional Effectiveness element says how effective the detection method may be in detecting the associated weakness. This assumes the use of best-of-breed tools, analysts, and methods. There is limited consideration for financial costs, labor, or time. The optional Effectiveness_Notes element provides additional discussion of the strengths and shortcomings of this detection method. The optional Detection_Method_ID attribute is used by the internal CWE team to uniquely identify methods that are repeated across any numbe...

| Element | Type | Cardinality |
| --- | --- | --- |
| Detection_Method | inline type | 1..unbounded |

### PotentialMitigationsType

The PotentialMitigationsType complex type is used to describe potential mitigations associated with a weakness. It contains one or more Mitigation elements, which each represent individual mitigations for the weakness. The Phase element indicates the development life cycle phase during which this particular mitigation may be applied. The Strategy element describes a general strategy for protecting a system to which this mitigation contributes. The Effectiveness element summarizes how effective the mitigation may be in preventing the weakness. The Description element contains a description of this individual mitigation including any strengths and shortcomings of this mitigation for the weakness. The optional Mitigation_ID attribute is used by the internal CWE team to uniquely identify mitigations that are repeated across any number of individual weaknesses. To help make sure that the d...

| Element | Type | Cardinality |
| --- | --- | --- |
| Mitigation | inline type | 1..unbounded |

### ObservedExampleType

The ObservedExampleType complex type specifies references to a specific observed instance of a weakness in real-world products. Typically this will be a CVE reference. Each Observed_Example element represents a single example. The required Reference element should contain the identifier for the example being cited. For example, if a CVE is being cited, it should be of the standard CVE identifier format, such as CVE-2005-1951 or CVE-1999-0046. The required Description element should contain a brief description of the weakness being cited, without including irrelevant details such as the product name or attack vectors. The description should present an unambiguous correlation between the example being described and the weakness(es) that it is meant to exemplify. It should also be short and easy to understand. The Link element should provide a valid URL where more information regarding t...

| Element | Type | Cardinality |
| --- | --- | --- |
| Observed_Example | inline type | 1..unbounded |

## Enumerations

### AbstractionEnumeration

The AbstractionEnumeration simple type defines the different abstraction levels that apply to a weakness. A "Pillar" is the most abstract type of weakness and represents a theme for all class/base/variant weaknesses related to it. A Pillar is different from a Category as a Pillar is still technically a type of weakness that describes a mistake, while a Category represents a common characteristic used to group related things. A "Class" is a weakness also described in a very abstract fashion, t...

| Value | Notes |
| --- | --- |
| Pillar |  |
| Class |  |
| Base |  |
| Variant |  |
| Compound |  |

### ArchitectureClassEnumeration

The ArchitectureClassEnumeration simple type contains a list of values corresponding to known classes of architectures. The value "Not Architecture-Specific" is used to indicate that the entry is not limited to a small set of architectures, i.e., it can appear in many different architectures.

| Value | Notes |
| --- | --- |
| Embedded |  |
| Microcomputer |  |
| Workstation |  |
| Not Architecture-Specific | Used to indicate that the entry is not limited to a small set of architectures, i.e., it can appear in many different architectures |

### ArchitectureNameEnumeration

The ArchitectureNameEnumeration simple type contains a list of values corresponding to known architectures.

| Value | Notes |
| --- | --- |
| Alpha |  |
| ARM |  |
| Itanium |  |
| Power Architecture |  |
| SPARC |  |
| x86 |  |
| Other |  |

### DetectionEffectivenessEnumeration

The DetectionEffectivenessEnumeration simple type defines the different levels of effectiveness that a detection method may have in detecting an associated weakness. The value "High" is used to describe a method that succeeds frequently and does not result in many false reports. The value "Moderate" is used to describe a method that is applicable to multiple circumstances, but it may not have complete coverage of the weakness, or it may result in a number of incorrect reports. The "SOAR Parti...

| Value | Notes |
| --- | --- |
| High |  |
| Moderate |  |
| SOAR Partial | Used to indicate that according to the IATAC State Of the Art Report (SOAR), the detection method is partially effective. |
| Opportunistic |  |
| Limited |  |
| None |  |

### DetectionMethodEnumeration

The DetectionMethodEnumeration simple type defines the different methods used to detect a weakness.

| Value | Notes |
| --- | --- |
| Automated Analysis |  |
| Automated Dynamic Analysis |  |
| Automated Static Analysis |  |
| Automated Static Analysis - Source Code |  |
| Automated Static Analysis - Binary or Bytecode |  |
| Fuzzing |  |
| Manual Analysis |  |
| Manual Dynamic Analysis |  |
| Manual Static Analysis |  |
| Manual Static Analysis - Source Code |  |
| Manual Static Analysis - Binary or Bytecode |  |
| White Box |  |
| Black Box |  |
| Architecture or Design Review |  |
| Dynamic Analysis with Manual Results Interpretation |  |
| Dynamic Analysis with Automated Results Interpretation |  |
| Formal Verification |  |
| Simulation / Emulation |  |
| Other |  |

### EffectivenessEnumeration

The EffectivenessEnumeration simple type defines the different values related to how effective a mitigation may be in preventing the weakness. A value of "High" means the mitigation is frequently successful in eliminating the weakness entirely. A value of "Moderate" means the mitigation will prevent the weakness in multiple forms, but it does not have complete coverage of the weakness. A value of "Limited" means the mitigation may be useful in limited circumstances, or it is only applicable t...

| Value | Notes |
| --- | --- |
| High |  |
| Moderate |  |
| Limited |  |
| Incidental |  |
| Discouraged Common Practice |  |
| Defense in Depth |  |
| None |  |

### FunctionalAreaEnumeration

The FunctionalAreaEnumeration simple type defines the different functional areas in which the weakness may appear. The value "Functional-Area-Independent" is used to indicate that the entry is not limited to a small set of functional areas, i.e., it can appear in many different functional areas

| Value | Notes |
| --- | --- |
| Authentication |  |
| Authorization |  |
| Code Libraries |  |
| Counters |  |
| Cryptography |  |
| Error Handling |  |
| Interprocess Communication |  |
| File Processing |  |
| Logging |  |
| Memory Management |  |
| Networking |  |
| Number Processing |  |
| Program Invocation |  |
| Protection Mechanism |  |
| Session Management |  |
| Signals |  |
| String Processing |  |
| Not Functional-Area-Specific | Used to indicate that the entry is not limited to a small set of functional areas, i.e., it can appear in many different functional areas |
| Power |  |
| Clock |  |

### ImportanceEnumeration

The ImportanceEnumeration simple type lists different values for importance.

| Value | Notes |
| --- | --- |
| Normal |  |
| Critical |  |

### LanguageClassEnumeration

The LanguageClassEnumeration simple type contains a list of values corresponding to different classes of source code languages. The same language could belong to multiple language classes, such as 'Object-Oriented' and 'Memory-Unsafe'. The value "Not Language-Specific" is used to indicate that the entry is not limited to a small set of languages.

| Value | Notes |
| --- | --- |
| Assembly |  |
| Compiled |  |
| Hardware Description Language |  |
| Interpreted |  |
| Object-Oriented |  |
| Memory-Unsafe |  |
| Not Language-Specific | Used to indicate that the entry is not limited to a small set of language classes, i.e., it can appear in many different language classes. |

### LanguageNameEnumeration

The LanguageNameEnumeration simple type contains a list of values corresponding to different source code languages or data formats.

| Value | Notes |
| --- | --- |
| Ada |  |
| ARM Assembly |  |
| ASP |  |
| ASP.NET |  |
| Basic |  |
| C |  |
| C++ |  |
| C# |  |
| COBOL |  |
| Fortran |  |
| F# |  |
| Go |  |
| HTML |  |
| Java |  |
| JavaScript |  |
| JSON |  |
| JSP |  |
| Objective-C |  |
| Pascal |  |
| Perl |  |
| PHP |  |
| Pseudocode |  |
| Python |  |
| Ruby |  |
| Rust |  |
| Shell |  |
| SQL |  |
| Swift |  |
| VB.NET |  |
| Verilog |  |
| VHDL |  |
| XML |  |
| x86 Assembly |  |
| Other |  |

### LikelihoodEnumeration

The LikelihoodEnumeration simple type contains a list of values corresponding to different likelihoods. The value "Unknown" should be used when the actual likelihood of something occurring is not known.

| Value | Notes |
| --- | --- |
| High |  |
| Medium |  |
| Low |  |
| Unknown |  |

### MitigationStrategyEnumeration

The MitigationStrategyEnumeration simple type lists general strategies for protecting a system to which a mitigation contributes.

| Value | Notes |
| --- | --- |
| Attack Surface Reduction |  |
| Compilation or Build Hardening |  |
| Enforcement by Conversion |  |
| Environment Hardening |  |
| Firewall |  |
| Input Validation |  |
| Language Selection |  |
| Libraries or Frameworks |  |
| Resource Limitation |  |
| Output Encoding |  |
| Parameterization |  |
| Refactoring |  |
| Sandbox or Jail |  |
| Separation of Privilege |  |

### NoteTypeEnumeration

The NoteTypeEnumeration simple type defines the different types of notes that can be associated with a weakness. An "Applicable Platform" note provides additional information about the list of applicable platforms for a given weakness. A "Maintenance" note contains significant maintenance tasks within this entry that still need to be addressed, such as clarifying the concepts involved or improving relationships. A "Relationship" note provides clarifying details regarding the relationships bet...

| Value | Notes |
| --- | --- |
| Applicable Platform |  |
| Maintenance |  |
| Relationship |  |
| Research Gap |  |
| Terminology |  |
| Theoretical |  |
| Other |  |

### OperatingSystemClassEnumeration

The OperatingSystemClassEnumeration simple type contains a list of values corresponding to different classes of operating systems. The value "Not OS-Specific" is used to indicate that the entry is not limited to a small set of operating system classes, i.e., it can appear in many different operating system classes.

| Value | Notes |
| --- | --- |
| Linux |  |
| macOS |  |
| Unix |  |
| Windows |  |
| Not OS-Specific | Used to indicate that the entry is not limited to a small set of operating system classes, i.e., it can appear in many different operating system classes. |

### OperatingSystemNameEnumeration

The OperatingSystemNameEnumeration simple type contains a list of values corresponding to different operating systems.

| Value | Notes |
| --- | --- |
| AIX |  |
| Android |  |
| BlackBerry OS |  |
| Chrome OS |  |
| Darwin |  |
| FreeBSD |  |
| iOS |  |
| macOS |  |
| NetBSD |  |
| OpenBSD |  |
| Red Hat |  |
| Solaris |  |
| SUSE |  |
| tvOS |  |
| Ubuntu |  |
| watchOS |  |
| Windows 9x |  |
| Windows Embedded |  |
| Windows NT |  |

### OrdinalEnumeration

The OrdinalEnumeration simple type contains a list of values used to determine if a relationship is the primary relationship for a given weakness entry within a given view. Currently, this attribute can only have the value "Primary".

| Value | Notes |
| --- | --- |
| Primary |  |

### OrdinalityEnumeration

The OrdinalityEnumeration simple type contains a list of values used to indicates potential ordering relationships with other weaknesses. A primary relationship means the weakness exists independent of other weaknesses, while a resultant relationship is when a weakness exists only in the presence of some other weaknesses. An indirect relationship means the weakness does not directly lead to security-relevant weaknesses but is a quality issue that might indirectly make it easier to introduce s...

| Value | Notes |
| --- | --- |
| Indirect |  |
| Primary |  |
| Resultant |  |

### PhaseEnumeration

The PhaseEnumeration simple type lists different phases in the product life cycle.

| Value | Notes |
| --- | --- |
| Policy |  |
| Requirements |  |
| Architecture and Design |  |
| Implementation |  |
| Build and Compilation |  |
| Testing |  |
| Documentation |  |
| Bundling |  |
| Distribution |  |
| Installation |  |
| System Configuration |  |
| Operation |  |
| Patching and Maintenance |  |
| Porting |  |
| Integration |  |
| Manufacturing |  |
| Decommissioning and End-of-Life |  |

### PrevalenceEnumeration

The PrevalenceEnumeration simple type defines the different regularities that guide the applicability of platforms.

| Value | Notes |
| --- | --- |
| Often |  |
| Sometimes |  |
| Rarely |  |
| Undetermined |  |

### ReasonEnumeration

The ReasonEnumeration simple type holds all the different types of reasons to why a CWE might not be considered for mapping.

| Value | Notes |
| --- | --- |
| Abstraction |  |
| Category |  |
| View |  |
| Deprecated |  |
| Potential Deprecation |  |
| Frequent Misuse |  |
| Frequent Misinterpretation |  |
| Multiple Use |  |
| CWE Overlap |  |
| Acceptable-Use |  |
| Potential Major Changes |  |
| Other |  |

### RelatedNatureEnumeration

The RelatedNatureEnumeration simple type defines the different values that can be used to define the nature of a related weakness. A ChildOf nature denotes a related weakness at a higher level of abstraction. A ParentOf nature denotes a related weakness at a lower level of abstraction. The StartsWith, CanPrecede, and CanFollow relationships are used to denote weaknesses that are part of a chaining structure. The RequiredBy and Requires relationships are used to denote a weakness that is part...

| Value | Notes |
| --- | --- |
| ChildOf |  |
| ParentOf |  |
| StartsWith |  |
| CanFollow |  |
| CanPrecede |  |
| RequiredBy |  |
| Requires |  |
| CanAlsoBe |  |
| PeerOf |  |

### ResourceEnumeration

The ResourceEnumeration simple type defines different resources of a system.

| Value | Notes |
| --- | --- |
| CPU |  |
| File or Directory |  |
| Memory |  |
| System Process |  |
| Other |  |

### ScopeEnumeration

The ScopeEnumeration simple type defines the different areas of security that can be affected by exploiting a weakness.

| Value | Notes |
| --- | --- |
| Confidentiality |  |
| Integrity |  |
| Availability |  |
| Access Control |  |
| Accountability |  |
| Authentication |  |
| Authorization |  |
| Non-Repudiation |  |
| Other |  |

### StakeholderEnumeration

The StakeholderEnumeration simple type defines the different types of users within the CWE community.

| Value | Notes |
| --- | --- |
| Academic Researchers |  |
| Applied Researchers |  |
| Assessment Teams |  |
| Assessment Tool Vendors |  |
| CWE Team |  |
| Educators |  |
| Hardware Designers |  |
| Information Providers |  |
| Product Customers |  |
| Product Vendors |  |
| Software Developers |  |
| Vulnerability Analysts |  |
| Other |  |

### StatusEnumeration

The StatusEnumeration simple type defines the different status values that an entity (view, category, weakness) can have. A value of Deprecated refers to an entity that has been removed from CWE, likely because it was a duplicate or was created in error. A value of Obsolete is used when an entity is still valid but no longer is relevant, likely because it has been superseded by a more recent entity. A value of Incomplete means that the entity does not have all important elements filled, and t...

| Value | Notes |
| --- | --- |
| Deprecated |  |
| Draft |  |
| Incomplete |  |
| Obsolete |  |
| Stable |  |
| Usable |  |

### StructureEnumeration

The StructureEnumeration simple type lists the different structural natures of a weakness. A Simple structure represents a single weakness whose exploitation is not dependent on the presence of another weakness. A Composite is a set of weaknesses that must all be present simultaneously in order to produce an exploitable vulnerability, while a Chain is a set of weaknesses that must be reachable consecutively in order to produce an exploitable vulnerability.

| Value | Notes |
| --- | --- |
| Chain |  |
| Composite |  |
| Simple |  |

### StructuredCodeNatureEnumeration

The StructuredCodeNatureEnumeration sinple type defines the different values that state what type of code is being shown in an eample.

| Value | Notes |
| --- | --- |
| Attack |  |
| Bad |  |
| Good |  |
| Informative |  |
| Mitigation |  |
| Result |  |

### TaxonomyMappingFitEnumeration

The TaxonomyMappingFitEnumeration simple type defines the different values used to describe how close a certain mapping to CWE is.

| Value | Notes |
| --- | --- |
| Exact |  |
| CWE More Abstract |  |
| CWE More Specific |  |
| Imprecise |  |
| Perspective |  |

### TaxonomyNameEnumeration

The TaxonomyNameEnumeration simple type lists the different known taxomomies that can be mapped to CWE.

| Value | Notes |
| --- | --- |
| 7 Pernicious Kingdoms |  |
| 19 Deadly Sins |  |
| Aslam |  |
| Bishop |  |
| CERT C Secure Coding |  |
| CERT C++ Secure Coding |  |
| The CERT Oracle Secure Coding Standard for Java (2011) |  |
| CLASP |  |
| ISA/IEC 62443 |  |
| Landwehr |  |
| OMG ASCSM |  |
| OMG ASCRM |  |
| OMG ASCMM |  |
| OMG ASCPEM |  |
| OWASP Top Ten 2004 |  |
| OWASP Top Ten 2007 |  |
| OWASP Top Ten |  |
| PLOVER |  |
| Protection Analysis |  |
| RISOS |  |
| SEI CERT C Coding Standard |  |
| SEI CERT C++ Coding Standard |  |
| SEI CERT Oracle Coding Standard for Java |  |
| SEI CERT Perl Coding Standard |  |
| Software Fault Patterns |  |
| Weber, Karger, Paradkar |  |
| WASC |  |

### TechnicalImpactEnumeration

The TechnicalImpactEnumeration simple type describes the technical impacts that can arise if an adversary successfully exploits a weakness.

| Value | Notes |
| --- | --- |
| Modify Memory |  |
| Read Memory |  |
| Modify Files or Directories |  |
| Read Files or Directories |  |
| Modify Application Data |  |
| Read Application Data |  |
| DoS: Crash, Exit, or Restart |  |
| DoS: Amplification |  |
| DoS: Instability |  |
| DoS: Resource Consumption (CPU) |  |
| DoS: Resource Consumption (Memory) |  |
| DoS: Resource Consumption (Other) |  |
| Execute Unauthorized Code or Commands |  |
| Gain Privileges or Assume Identity |  |
| Bypass Protection Mechanism |  |
| Hide Activities |  |
| Alter Execution Logic |  |
| Quality Degradation |  |
| Unexpected State |  |
| Varies by Context |  |
| Increase Analytical Complexity | It is more difficult for humans or tools to analyze the product's code, documentation, and other artifacts understand how the product works or is intended to work, which can make it more difficult to find and fix vulnerabilities. |
| Reduce Maintainability |  |
| Reduce Performance |  |
| Reduce Reliability |  |
| Other |  |

### TechnologyClassEnumeration

The TechnologyClassEnumeration simple type contains a list of values corresponding to different classes of technologies. The value "Not Technology-Specific" is used to indicate that the entry is not limited to a small set of technologies, i.e., it can appear in many different technologies.

| Value | Notes |
| --- | --- |
| Client Server | Represents technology involving a distributed application but for the purposes of CWE does not leverage a web browser. |
| Cloud Computing | Represents technology that involves data storage and computing power being made available to multiple users via the internet instead of using local systems, without the need for users to perform all system management themselves. |
| ICS/OT | Represents technology related to Industrial Control Systems (ICS) and Operational Techology (OT), which are often considered to be distinct from Information Technology (IT) systems. |
| Mainframe |  |
| Mobile |  |
| N-Tier |  |
| SOA | Represents technology related to Service-oriented architecture (SOA). |
| System on Chip | Represents technology that integrates all components of a computer within a single integrated circuit, to include FPGA and ASIC. |
| Web Based | Represents technology that involves applications or single-page sites that leverage a web browser to support client interactions. |
| Not Technology-Specific | Used to indicate that the entry is not limited to a small set of technologies, i.e., it can appear in many different technologies. |

### TechnologyNameEnumeration

The TechnologyNameEnumeration simple type contains a list of values corresponding to different technologies. A technology represents a generally accepted feature of a system and often refers to a high-level functional component within a system. Within this context, "IP" stands for "Intellectual Property" and is the term used to distinguish unique blocks within a System on Chip, with each block potentially coming from a different source.

| Value | Notes |
| --- | --- |
| AI/ML | Represents technology related to Artificial Intelligence (AI) and Machine Learning (ML) systems. Note: terminology in this space is inconsistently used, but the AI WG agreed on this usage for CWE 4.15. |
| Web Server |  |
| Database Server |  |
| Accelerator Hardware | hardware Intellectual Property (IP) dedicated to offload a specific workload to enhance performance: DSP, packet processing, mathematical, compression, etc. |
| Analog and Mixed Signal Hardware | hardware Intellectual Property (IP) that controls/senses the electricals for communication which receives/transmits signals conditioned outside of a system’s digital domain. |
| Audio/Video Hardware | hardware Intellectual Property (IP) designed to manipulate audio/video data: coders/decoders, speech recognition, format converters, etc. |
| Bus/Interface Hardware | hardware Intellectual Property (IP) implementing an interconnect among elements in a computing system: I2C, PCIe, DDR, MMC, USB, GPIO, NoC, etc. |
| Clock/Counter Hardware | hardware Intellectual Property (IP) reflecting the passage of time in oscillations or human units: Real Time Clock, Watchdog, Monotonic Counter, etc. |
| Communication Hardware | hardware Intellectual Property (IP) designed to transmit/receive information: Modulator/Demodulator, GPS, 802.11, Bluetooth, CDMA/DSM, etc. |
| Controller Hardware | hardware Intellectual Property (IP) circuit hard-wired (e.g., an FSM) to react in a closed-loop control system or other limited context, to control another entity: Arbiter, APIC, USB, Peripheral, Memory, Storage, etc. |
| Memory Hardware | hardware Intellectual Property (IP) implementing volatile (transient) data storage: DRAM, SRAM, etc. |
| Microcontroller Hardware | hardware Intellectual Property (IP) implementing a specialized processor acting as a programmable controller. |
| Network on Chip Hardware |  |
| Power Management Hardware | hardware Intellectual Property (IP) that controls and/or monitors the power state of a system: voltage regulators, power controllers, power monitors, etc. |
| Processor Hardware | hardware Intellectual Property (IP) implementing a general-purpose computing engine: CPU, GPU, RISC, CISC, etc. |
| Security Hardware | hardware Intellectual Property (IP), including hardware security modules (HSM), designed to protect assets: cryptography, auth, tamper detection, etc. |
| Sensor Hardware |  |
| Storage Hardware |  |
| Test/Debug Hardware | hardware Intellectual Property (IP) designed to verify functionality and identify root cause of defects: JTAG, BIST, boundary scan, pattern generator, etc. |
| Other |  |

### UsageEnumeration

The UsageEnumeration simple type is used for whether this CWE entry is supported for mapping.

| Value | Notes |
| --- | --- |
| Discouraged | this CWE ID should not be used to map to real-world vulnerabilities |
| Prohibited | this CWE ID must not be used to map to real-world vulnerabilities |
| Allowed | this CWE ID may be used to map to real-world vulnerabilities |
| Allowed-with-Review | this CWE ID could be used to map to real-world vulnerabilities in limited situations requiring careful review |

### ViewTypeEnumeration

The ViewTypeEnumeration simple type defines the different types of views that can be found within CWE. A graph is a hierarchical representation of weaknesses based on a specific vantage point that a user may take. The hierarchy often starts with a category, followed by a class/base weakness, and ends with a variant weakness. In addition to graphs, a view can be a slice, which is a flat list of entries that does not specify any relationships between those entries. An explicit slice is a subset...

| Value | Notes |
| --- | --- |
| Implicit |  |
| Explicit |  |
| Graph |  |
