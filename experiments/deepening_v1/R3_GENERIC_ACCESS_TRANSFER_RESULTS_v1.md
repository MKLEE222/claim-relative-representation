# R3 Generic-Access Carrier-Exposure Development Results v1

Date: 2026-09-27
Status: PRESERVED DEVELOPMENT / SENSITIVITY RUN. **NOT AUTHORITATIVE FOR AW1 ENTRY-DISCOVERABILITY CLAIMS.**

## Why this file is demoted

This run was created while independently extending R3 into carrier-component evaluation.

It used the same generic access algorithm family as the 2026-09-24 policy, but it instantiated its own seed/task formulations and therefore is not numerically interchangeable with the already-existing authoritative R3-AW1 workflow transfer.

The authoritative ecological entry-discoverability result is:

`R3_AW1_GENERIC_ACCESS_RESULTS_v1.md`

The authoritative retrospective decomposition of the Great Desert AW1 ranking into proposition-specific carrier components is:

`R3_AW1_GREAT_DESERT_COMPONENT_AUDIT_RESULTS_v1.md`

No result in this file overrides either.

## Preserved run provenance

### Five-inquiry development transfer

GitHub Actions run: 36313158548  
Head commit: 023009ef2aabebd2b82f709a450903508e4c2d38  
Artifact: deepening-r3-generic-access-transfer-v1  
Artifact id: 10929697089  
Artifact ZIP SHA-256: 3d868abd6846ea95392c6a0fe64c3c42d63d81b4e7ce4465f3cae6f0bf6140ee

The run remains useful as a development demonstration that carrier-component ranks can differ from one another and that one 180-word chunk need not contain every carrier required by a multi-proposition inquiry.

Its ranks are task-formulation-specific and must not replace AW1.

## Great Desert local-context sensitivity run

GitHub Actions run: 36313295632  
Artifact: deepening-r3-great-desert-exact-start-v1  
Artifact id: 10930175337  
Artifact ZIP SHA-256: 74ea04366f593b4328d4a00e9519f5e5f988a96aa6dc3ba8a8a0d81f44f1656a

The seed **anchor** correctly targeted the opening of 1903 I p.202 Note 2:

`The waste and desert places of the Earth`

However, post-run audit found that the seed-span extractor fell back to a bounded local-context window rather than isolating the exact p.202 note/paragraph. This is visible in the generated query, which contains adjacent p.201 terms such as `Urumtsi` and `Charkalyk`.

Therefore:

[
STRICT_EXACT_START_IMPLEMENTATION = 0.
]

The run is retained only as a local-context sensitivity result. It is not evidence that the exact frozen p.202 start yields the reported component ranks.

## Authoritative replacement for Great Desert component exposure

The later retrospective audit replays the **exact authoritative AW1 ranking** without changing its seed, query, windows, ranker, or target entry.

R3-AW1 Great Desert:

- full-object target entry rank = 6;
- later-layer target entry rank = 1.

Within those same ranked lists:

### Full object
- folklore carrier rank = 6;
- measurement carrier rank = 341;
- both not complete within top 50.

### Native later layer
- folklore carrier rank = 1;
- measurement carrier rank = 35;
- both complete only within top 50.

This yields the licensed distinction:

[
entry discoverability 
eq proposition	ext{-}carrier completeness.
]

## Preserved useful lesson from this development branch

The development work correctly identified that a scholarly inquiry may require multiple textual carriers and that retrieval evaluation should not stop at one target-entry rank.

That methodological insight is now carried by the AW1 component audit rather than by the non-authoritative ranks in this file.

## Claim rule

Do not cite this file for:
- primary AW1 entry ranks;
- strict p.202 exact-start effects;
- natural proposition-binding deletion.

Use it only for provenance of the development path and sensitivity diagnostics.
