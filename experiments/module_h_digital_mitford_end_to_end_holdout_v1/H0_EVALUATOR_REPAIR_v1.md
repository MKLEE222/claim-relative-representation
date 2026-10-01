# Module H0 evaluator repair note v1

Date: 2026-09-28
Status: PRE-OUTCOME IMPLEMENTATION REPAIR.

Failed run:
36384484110

The run terminated before population extraction produced any scientific output.

Failure:
the frozen Digital Mitford Journal XML contains a duplicate xml:id value:

    e-1172

lxml's default parser builds an XML ID table and treats the duplicate ID as a fatal parse error.

This duplicate is a property of the frozen source snapshot. It is not repaired or rewritten.

Repair:
parse the frozen XML with:

    collect_ids=False

while retaining:
- recover=False;
- entity resolution disabled;
- network access disabled;
- exact frozen source bytes and Git blobs.

This suppresses only parser-level ID uniqueness enforcement. It does not alter element content, refs, names, source matching, population rules, exposure exclusions, checkpoints, or scientific criteria.

The failed run is preserved and is not an experimental outcome.
