# R3 Proposition-Binding Repair Protocol v1

Date: 2026-09-27
Status: constructive follow-up to separation run 36306380002. This is not an untouched discovery test.

## Question

Can a bounded source-derived binding repair restore each separated inquiry, while an equally shaped incorrect binding fails?

## Repair objects

### Pashai

Base projection: P_STANCE_BAG.

Correct repair adds exactly two stance-target bindings:
- CORROBORATION -> PASH-PROV-1903;
- CRITICISM -> PASH-ROUTE-1903.

Matched wrong repair adds the same two edge types with targets swapped.

### Arbre Sec

Base projection: P_ROLE_BAG.

Correct repair adds source-relative commitment roles:
- HOUTUM_SCHINDLER -> COMMITS_TO cypress proposition;
- CORDIER -> TRANSMITS cypress proposition;
- CORDIER adoption status -> NOT_ESTABLISHED_IN_INSPECTED_ENTRY.

Matched wrong repair has the same information footprint but changes the final Cordier status to ADOPTS_IN_INSPECTED_ENTRY.

### Great Desert

Base projection: P_EVIDENCE_BAG.

Correct repair adds two evidence-proposition edges:
- LOCAL_FOLKLORE_INTERPRETATION -> DES-FOLK-1920;
- PLANE_TABLE_AND_CYCLOMETER_MEASUREMENTS -> DES-DIST-1920.

Matched wrong repair swaps the two targets.

## Control

The Urumtsi text-pair inquiry is unaffected by all three repair families and must remain `found -> founded`.

## Success conditions

For each primary case:
1. correct repair reproduces the reference inquiry output exactly;
2. matched wrong repair does not reproduce the reference output;
3. repair and wrong-repair information footprints have equal cardinality/type profile;
4. Urumtsi control remains unchanged.

## Claim ceiling

A passing result demonstrates constructive repair for the named controlled projection only.

It does not show that these are globally minimal encodings or that a named real-world platform should implement this exact schema.