"""Verify the round-two delivery ZIP. Integrity is not historical adjudication."""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

EXPECTED = "24ca6e2f7023dff59bd61887914fffa877ecaf1c8c170a006ecbe405c17d90c7"
PREFIX = "R3_Frame_And_Responsibility_Audit_2026-09-27/"

def verify(path: Path) -> dict:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != EXPECTED:
        raise ValueError("Unexpected delivery archive identity")
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP CRC check failed")
        manifest = json.loads(z.read(PREFIX + "delivery_manifest.json"))
        for item in manifest["files"]:
            data = z.read(PREFIX + item["path"])
            if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise ValueError("Delivery member mismatch: " + item["path"])
        source = z.read(PREFIX + "sources/pg12410.txt").decode("utf-8")
        original = json.loads(z.read(PREFIX + "reference/frozen_frame_intervals.json"))["entries"]
        for entry in original:
            text = source[entry["source_start"]:entry["source_end"]]
            actual = hashlib.sha256(" ".join(text.split()).encode("utf-8")).hexdigest()
            if actual != entry["entry_sha256"]:
                raise ValueError("Legacy source interval mismatch: " + entry["entry_id"])
        spans = json.loads(z.read(PREFIX + "exact_spans.json"))
        sources = {name: z.read(PREFIX + "sources/" + name).decode("utf-8") for name in ("pg10636.txt", "pg12410.txt")}
        for span in spans:
            text = sources[span["source_file"]][span["start"]:span["end"]]
            if text != span["raw_text"] or hashlib.sha256(text.encode()).hexdigest() != span["span_sha256_utf8"]:
                raise ValueError("Exact evidence span mismatch: " + span["span_id"])
        return {"archive_sha256": digest, "members_checked": len(manifest["files"]), "legacy_intervals_checked": len(original), "exact_spans_checked": len(spans), "historical_interpretation_independently_validated": False, "retrieval_recomputed": False}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.archive), indent=2))
