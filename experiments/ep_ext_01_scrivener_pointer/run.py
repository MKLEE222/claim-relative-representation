from __future__ import annotations

import hashlib
import re
import urllib.request
from html.parser import HTMLParser

URL="https://www.gutenberg.org/cache/epub/36548/pg36548-images.html"
OLD="Synaxaria"
NEW="Menologies"
TARGET_PAGE=87

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts=[]
    def handle_data(self,data):
        if data:
            self.parts.append(data)

def fetch():
    req=urllib.request.Request(URL,headers={"User-Agent":"claim-relative-representation/1.0"})
    with urllib.request.urlopen(req,timeout=45) as r:
        return r.read()

def normalize(s):
    return re.sub(r"\s+"," "," ".join(s.split())).strip()

raw=fetch()
html=raw.decode("utf-8",errors="replace")
p=VisibleText()
p.feed(html)
visible="\n".join(p.parts)

# Find addenda/body boundary so pointer-free search does not count the correction entry itself.
body_match=re.search(r"\[pg\s*0*01\]",visible,flags=re.I)
if not body_match:
    print("EP_EXT_01_SCRIVENER_POINTER")
    print("STATUS=BLOCKED_SOURCE")
    print("REASON=body page 001 marker unavailable")
    raise SystemExit(0)
body=visible[body_match.start():]

page_pat=rf"\[pg\s*0*{TARGET_PAGE}\]"
next_pat=rf"\[pg\s*0*{TARGET_PAGE+1}\]"
pm=re.search(page_pat,body,flags=re.I)
nm=re.search(next_pat,body[pm.end():] if pm else "",flags=re.I) if pm else None

print("EP_EXT_01_SCRIVENER_POINTER")
print("source_sha256="+hashlib.sha256(raw).hexdigest())
print("selection_entry=P.87,l.19,for_Synaxaria_read_Menologies")

if not pm or not nm:
    print("STATUS=BLOCKED_SOURCE")
    print("REASON=target page boundary unavailable")
    raise SystemExit(0)

page_start=pm.start()
page_end=pm.end()+nm.start()
page87=body[page_start:page_end]

page_hits=[m.start() for m in re.finditer(r"\bSynaxaria\b",page87,flags=re.I)]
all_hits=[m.start() for m in re.finditer(r"\bSynaxaria\b",body,flags=re.I)]

if not page_hits:
    print("STATUS=BLOCKED_SOURCE")
    print("REASON=old reading absent from page 87")
    raise SystemExit(0)

# Target = first page-87 occurrence, as defined by native correction pointer.
target_abs=page_start+page_hits[0]
ordinal=1+sum(1 for x in all_hits if x<target_abs)

print("page87_old_reading_count="+str(len(page_hits)))
print("body_old_reading_count="+str(len(all_hits)))
print("pointer_free_target_ordinal="+str(ordinal))

print("RESULT,SCR_FULL_POINTER,state=EXACT_LOCALIZATION,candidates=1")
if len(page_hits)==1:
    print("RESULT,SCR_PAGE_ONLY,state=EXACT_LOCALIZATION,candidates=1")
else:
    print(f"RESULT,SCR_PAGE_ONLY,state=MULTIPLE_CANDIDATES,candidates={len(page_hits)}")

if len(all_hits)==1:
    print("RESULT,SCR_POINTER_FREE,state=EXACT_LOCALIZATION,candidates=1,target_ordinal=1")
else:
    print(f"RESULT,SCR_POINTER_FREE,state=MULTIPLE_CANDIDATES,candidates={len(all_hits)},target_ordinal={ordinal}")

if len(page_hits)==1:
    print("MINIMAL_POINTER_RESULT=line_coordinate_not_required_given_page_plus_old_reading")
else:
    print("MINIMAL_POINTER_RESULT=line_coordinate_may_be_required_within_page")

print("TEXTUAL_CRITICAL_TRUTH_ADJUDICATED=0")
