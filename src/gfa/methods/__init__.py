"""
Nabhani Methods - Governing Method Hierarchy

This package implements the Nabhani method hierarchy:
- RationalMethod: The root governing method (الطريقة العقلية)
- NeutralBinding: Neutral element (العنصر المحايد)
- StyleSpec: Domain specializations (أساليب التفكير)
- LafziMadlul: Linguistic signification domain
- DalMadlulBinding: Signifier/Signified binding (PR-L4)
- (future) ScientificMethod: Experimental branch (الطريقة العلمية)
- (future) LogicalStyle: Formal grounded style (الطريقة المنطقية)
- (future) MeansAlgebra: Non-certifying instruments (وسائل التفكير)

Core Principle:
    RationalMethod is the root.
    All other methods are branches or specializations.
    No branch may claim to be root.

Module Exports:
    - rational: RationalMethod, NeutralBinding, PriorInformation
    - styles: StyleSpec, ThinkingDomain
    - lafzi_trace: LafziTrace
    - lafzi_registration: LafziMadlul registration
    - lafzi_dal: DālCandidate
    - lafzi_madlul: MadlulLafziCandidate
    - lafzi_binding: DalMadlulBinding (PR-L4)
"""

__version__ = "0.1.0"
