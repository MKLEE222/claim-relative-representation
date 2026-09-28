# Oxford MMOL Auct_B prospective transfer results v1

Date: 2026-09-28
Status: PROSPECTIVE TRANSFER SUPPORT STOP; NO REPLACEMENT UNDER V1.
GitHub Actions run: 36373900483
Artifact: oxford-mmol-auct-b-parent-transfer-v1
Artifact ID: 10950163413
Artifact ZIP SHA-256: 7eb2240d2a8b3b40a85d257b2f4847ee1cdf1607312faa8d03870f7b8bca44e8
results SHA-256: b992e7907545631ed5ceed2c2ee4ad8d516b91437a0c71dda94db257e6b23baa

## Frozen population

The selection was fixed by repository path/file metadata before Auct_B content was opened:

- MS_Auct_B_subtus_4.xml
- MS_Auct_B_subtus_5.xml
- MS_Auct_B_subtus_6.xml

All three were executed.

## Result

- native msItems: 3
- native nested msItems: 0
- aligned published items: 3 / 3
- aligned nested items: 0
- row trigger true negatives: 3 / 3
- trigger false positives: 0
- trigger false negatives: 0

Disposition:

`TRANSFER_SUPPORT_STOP_ZERO_ELIGIBLE_NESTED_ITEMS`

## Interpretation

The frozen Auct_B collection does not instantiate the registered parent-continuation task.

Therefore:
- it provides no positive or negative evidence about FILE_TABLE parent recovery;
- it does not falsify the Frankenstein/Oxford development mechanism;
- it cannot be replaced inside v1 after opening;
- the three correct row-trigger negatives are retained only as scope controls.

The v1 transfer is scientifically uninformative about parent continuation beyond confirming that the selection rule did not guarantee task support.

A new v2 may use a prospectively frozen structural-eligibility selector, provided:
- eligibility is defined from native source structure only;
- no tabular parent-recovery outcome is inspected during selection;
- the decoder and disposition rules are frozen before candidate scanning;
- all selection failures are preserved.
