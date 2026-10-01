# Module H implementation freeze v1

Date: 2026-09-28
Status: FROZEN BEFORE PAUL D'ESTOURNELLES DE CONSTANT HOLDOUT BODY INSPECTION.

## Frozen scientific protocol

Original prospective protocol:
- path: experiments/module_h_dahn_end_to_end_holdout_v1/PROTOCOL.md
- protocol commit: b725d12ca9029b195dbfa2febe01501d74f25b68

Development-driven design repair, still before any Paul holdout body inspection:
- experiments/module_h_dahn_end_to_end_holdout_v1/DEVELOPMENT_DESIGN_REPAIR_v1.md
- repair commits: ac011d27e9a9e3849eb4a62480c0753a45384589 and 4770c48649779d52fec843d6d1158db6780f2710

The repair separates:
- t0 root carriers: docDate / sent / dateline
from:
- later OPEN_ORIGIN evidence: primary current-document origDate.

Evidence effect is evaluated as:
    W_root != W_post_origin

not merely Q0 != W_post_origin.

## Frozen evaluator

Path:
experiments/module_h_dahn_end_to_end_holdout_v1/run.py

Git blob SHA-1:
3cfb747de03df433692415457f22293e0adefc49

Code commit:
c0148f36fa5446057a6a382bb58f10429d5b96ff

The holdout workflow must refuse execution if this blob identity changes.

## Final Berlin development verification

Authoritative development-only run:
36393954208

Artifact:
module-h-dahn-development-verification-v1

Artifact ID:
10957945232

Artifact ZIP SHA-256:
c587bbed29c5ffc8173ad1a41b17a7d5fb0977b042e5ca1442c283db6d5d7a43

Population:
- 190 parsed XML documents
- 0 parse errors
- 42 primary discovery episodes
- 39 full trajectories

I_NATIVE:
- 39/39 end-to-end

I_RSTAR:
- 39/39 end-to-end

I_NO_ALTERNATIVES:
- 6/39 end-to-end

I_NO_BINDING:
- 0/39 end-to-end

I_NO_HISTORY:
- 39/39 delayed warrant state exact
- 0/39 transition history exact
- 0/39 end-to-end under the declared audit task

All pre-holdout development checks are satisfied.

## Prospective holdout

Frozen prefix:
Correspondence/Paul_d_Estournelles_de_Constant/Corpus/

Frozen upstream:
FloChiff/DAHNProject
commit e7d4a81d42ea10a3d672e5c0869f033a8c2c8149

Pre-holdout exposure:
- repository tree/path count only
- 1,515 XML file paths observed
- filenames observed
- NO Paul holdout XML body opened before this freeze

The holdout will be processed once using the exact frozen evaluator.

No holdout-specific parser, representation, eligibility, warrant, or ablation repair is authorized after scientific outcomes are produced.
