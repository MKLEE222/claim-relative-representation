# Module R / VGW authoritative fresh attempt result v1

Date: 2026-09-29
Status: INVALID AUTHORITATIVE FRESH ATTEMPT.

## 1. Authority

Fresh trigger commit:

    6f92907abee21d0d5d3edef6ca4c9ac91e6815c6

Authoritative workflow:

    module-r-vgw-fresh-confirmatory-v1
    run 36553853190

PRE_DATA job:

    SUCCESS

DATA_OPEN event:

    2026-09-29T10:10:41.478059+00:00

At DATA_OPEN, the five VGW provider distributions became exposed forever for this project.

## 2. Source acquisition

All five frozen distributions were downloaded completely.

Frozen/observed byte sizes matched exactly.

Distribution SHA-256:

    de_la_faille_1970
    88ae395103d86b5b40afb40465d7d093d88412f16841c936bfa22e68502548e3

    works_after_1970
    eed8cd78f3ec811b5302555abb5cad14cc86679ebc23e9132f46943803dac810

    van_gogh_museum
    8985296d791366910ae01a954d0ade65f196f461cd78328ce21602e2ed279e43

    krollermuller_museum
    78c48e3f7cb1699548e3d7f2e604ce363a663deca1b3747343fb22c013c788b2

    rkd_collections
    85ec7afd25c3cd4cf99924d65a7b9954c50254715467231a0a1f56fe1e5d7f03

Composite source-manifest SHA-256:

    94520fe008f1d2c96fdfa74412ce2801bb13ec0672344b680874312e91e0415d

Thus the failure is not incomplete source acquisition.

## 3. Failure

The RDFLib oracle accepted the real N-Triples population.

The independent lexical runtime failed while parsing the De la Faille distribution:

    ValueError: missing terminal dot at line 31932

Therefore no oracle/runtime population comparison or scientific candidate result was completed.

Frozen disposition:

    INVALID

Reason:

    RUNTIME_NTRIPLES_LEXER_FAILURE_AFTER_DATA_OPEN

This is not:
- NULL_APPLICABILITY;
- NULL_REASSESSMENT;
- evidence against the Module-R mechanism.

## 4. Post-exposure diagnostic

Diagnostic workflow:

    36554246988

The exact failing source line, verified against the frozen source SHA, has the form:

    <IRI> <IRI> _:blank-node-label.

The blank-node object is immediately followed by the legal N-Triples statement terminator dot.

The runtime parser's blank-node reader consumed characters until whitespace, so it incorrectly
included the terminal dot in the blank-node token.

It then reached end-of-line and reported that the terminal dot was missing.

This is a lexical parser implementation gap.

It does not change:
- object identity rules;
- F-number join;
- attribution-status vocabulary;
- event semantics;
- transition class;
- Module-R capabilities;
- comparator budgets.

## 5. Freshness disposition

The authoritative fresh attempt remains INVALID.

Because DATA_OPEN occurred, no later correction may be relabeled as the first fresh confirmatory
run.

A minimal parser correction may be run only as:

    CORRECTED_REPRODUCTION_AFTER_FRESH_INVALID

and may establish whether the frozen scientific analysis is executable/stable after fixing the
lexer.

## 6. Preserved artifact

Workflow artifact:

    ID 11026975223
    module-r-vgw-fresh-confirmatory-v1

Artifact digest:

    sha256:fe0bc95c067aa6cdc3d98ad03b4e4862ed5acf36b15ba5e9816b53303b64925b

It contains:
- DATA_OPEN_EVENT_v1.json;
- distribution_manifest_v1.json.
