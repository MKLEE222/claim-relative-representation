# Module R / VGW catalog JSON-LD metadata rule v1

Date: 2026-09-29
Status: PRE-FRESH METADATA-ONLY RULE.

## Preconditions

HEAD-only run 36527870153 established that every frozen VGW landing URL returns:

    Content-Type: application/ld+json
    Content-Length: between 1428 and 1596 bytes

with zero response-body bytes read.

These responses are catalog-record sized and share Last-Modified times with the already frozen
HTML landing records.

No provider RDF distribution has been opened.

## Authorized metadata GET

For each of the five already frozen landing URLs only:

    GET {landing_url}
    Accept: application/ld+json

The client must first verify the frozen HEAD anchor for that slug.

Hard metadata boundary:

    Content-Type contains application/ld+json
    Content-Length <= 10000 bytes

The client may read at most:

    10000 bytes

If Content-Length is absent, exceeds 10000, or the returned body exceeds 10000 bytes:

    STOP / METADATA_BOUNDARY_INVALID

Do not truncate and interpret a larger response.

## Allowed inspection

The JSON-LD catalog record may be parsed only to recover dataset/distribution metadata such as:
- dataset identifier/title;
- modified timestamp;
- publisher/provider;
- distribution media type;
- distribution access/download URL;
- byte size or format where supplied.

Do not follow any recovered distribution URL.

Do not inspect artwork identifiers, production activities, creator assertions or attribution
assignments at this stage.

## Freshness interpretation

Reading this bounded catalog metadata does not consume the provider data distribution.

Strict fresh status is retained unless:
- a response violates the metadata-size/type boundary;
- provider RDF content is returned inside the bounded record unexpectedly;
- a distribution URL is followed.

Any such incident must be recorded before further work.
