from __future__ import annotations

RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
CRM = "http://www.cidoc-crm.org/cidoc-crm/"

E22_HUMAN_MADE_OBJECT = CRM + "E22_Human-Made_Object"
E42_IDENTIFIER = CRM + "E42_Identifier"
E12_PRODUCTION = CRM + "E12_Production"
E13_ATTRIBUTE_ASSIGNMENT = CRM + "E13_Attribute_Assignment"

P1_IDENTIFIED_BY = CRM + "P1_is_identified_by"
P2_HAS_TYPE = CRM + "P2_has_type"
P14_CARRIED_OUT_BY = CRM + "P14_carried_out_by"
P108I_WAS_PRODUCED_BY = CRM + "P108i_was_produced_by"
P141_ASSIGNED = CRM + "P141_assigned"
P141I_WAS_ASSIGNED_BY = CRM + "P141i_was_assigned_by"
P190_SYMBOLIC_CONTENT = CRM + "P190_has_symbolic_content"

F_NUMBER_TYPE = "https://vangoghworldwide.org/data/concept/f_number"
PREVIOUS_ATTRIBUTION_TYPE = (
    "https://vangoghworldwide.org/data/concept/previous_attribution"
)

VAN_GOGH_IDS = frozenset({
    "http://vocab.getty.edu/ulan/500115588",
    "https://data.rkd.nl/artists/32439",
})

BASELINE_SLUG = "de_la_faille_1970"
POST1970_SLUG = "works_after_1970"
CURRENT_PROVIDER_SLUGS = (
    "van_gogh_museum",
    "krollermuller_museum",
    "rkd_collections",
)

TARGET_PROPERTY = "van-gogh-creator-attribution-status"
VALUE_VAN_GOGH = "VINCENT_VAN_GOGH"
STATUS_ATTRIBUTED = "ATTRIBUTED"
STATUS_PREVIOUS = "PREVIOUSLY_ATTRIBUTED"

STUDY_REPOSITORY = "VAN_GOGH_WORLDWIDE_COMPOSITE"
SYNTHETIC_SOURCE_VERSION = "VGW_SYNTHETIC_V1"
