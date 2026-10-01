# Module R / VGW distribution discovery rule v1

Date: 2026-09-29
Status: PRE-FRESH METADATA-ONLY RULE.

## Purpose

The five frozen Van Gogh Worldwide dataset landing pages expose distribution existence and media
type through the public catalog, but their HTML does not contain a static distribution href.

No N-Triples distribution has been opened.

## Frozen deterministic discovery rule

For each already frozen landing URL:

    https://data.spinque.com/ld/data/vangoghworldwide/{slug}/

perform exactly one HTTP HEAD request with:

    Accept: application/n-triples

The probe may:
- follow HTTP redirects while retaining HEAD semantics;
- record status;
- final URL;
- Content-Type;
- Content-Length;
- ETag;
- Last-Modified;
- Content-Disposition;
- Location / redirect history when exposed by the client.

The probe must not:
- issue GET with application/n-triples;
- read any response body;
- try guessed suffixes such as .nt, /download or /distribution;
- enumerate artwork URIs;
- inspect any RDF statement.

If HEAD unexpectedly returns a body-capable response, the client still reads zero bytes.

## Interpretation

A HEAD response can establish a deterministic distribution endpoint/version anchor.

It cannot establish:
- record count;
- triple content;
- presence of previous_attribution;
- any scientific outcome.

If the server does not support useful HEAD content negotiation, stop and design another
metadata-only method before any data opening.
