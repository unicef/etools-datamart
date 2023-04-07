import logging

logger = logging.getLogger(__name__)

ACL_ACCESS_OPEN = 0
ACL_ACCESS_LOGIN = 2
ACL_ACCESS_RESTRICTED = 4
ACL_ACCESS_RESERVED = 8

ACL_LABELS = {
    ACL_ACCESS_OPEN: "Open",
    ACL_ACCESS_LOGIN: "Login required",
    ACL_ACCESS_RESTRICTED: "Access Restricted",
    ACL_ACCESS_RESERVED: "Business authorization needed",
}

CLASS_STRICTLY = 1
CLASS_CONFIDENTIAL = 2
CLASS_INTERNAL = 3
CLASS_INTERNAL_UN = 4
CLASS_PUBLIC = 5
CONFIDENTIALITY_CHOICES = (
    (CLASS_STRICTLY, "Strictly Confidential"),
    (CLASS_CONFIDENTIAL, "Confidential"),
    (CLASS_INTERNAL, "Internal"),
    (CLASS_INTERNAL_UN, "Internal UN"),
    (CLASS_PUBLIC, "Public"),
)
