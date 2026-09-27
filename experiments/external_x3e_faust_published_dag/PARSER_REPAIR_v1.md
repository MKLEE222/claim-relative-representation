# X3E DOT Parser Repair v1

Date: 2026-09-27
Status: IMPLEMENTATION REPAIR AFTER PARSE FAILURE

The first X3E run successfully fetched the one frozen official object:

- URL: https://www.faustedition.net/macrogenesis/dag-graph.dot
- bytes: 443462
- SHA-256: a76c25331da9408560682c835de8cf5f02ee2773a6f3595fa086aee1fa2c849b

No DAG outcome was observed because the local DOT edge regex returned zero directed edges.

## Parser bug

The v1 regex ended the second node token with a regex word boundary:

`... (?P<v>QUOTED|UNQUOTED)\b`

For a quoted Graphviz identifier the token ends in `"`, which is a non-word character. When followed by whitespace, `[`, or `;`, no word boundary exists.

Thus quoted edge endpoints can fail even when the DOT contains valid directed edges.

## Repair

- same URL;
- same frozen object;
- same scientific metrics;
- same cycle algorithm;
- no fallback filename;
- no graph outcome-dependent choice.

Only the edge lexical recognizer changes:
- remove the inappropriate trailing word boundary;
- require a DOT-valid following delimiter by lookahead: whitespace, `[`, `;`, or line end.

The repair also reports raw counts of `->` and `--` operator substrings before parsing so syntax mismatch is explicit.

If the repaired parser still yields zero directed edges, status remains PARSE_FAILURE and no alternate object is searched.
