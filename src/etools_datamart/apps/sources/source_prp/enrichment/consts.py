from model_utils import Choices

REPORTING_TYPES = Choices(
    ('QPR', 'Quarterly Progress Report'),
    ('HR', 'Humanitarian Report'),
    ('SR', 'Special Report'),
)

PROGRESS_REPORT_STATUS = Choices(
    ('Due', 'due', 'Due'),
    ('Ove', 'overdue', 'Overdue'),
    ('Sub', 'submitted', 'Submitted'),
    ('Sen', 'sent_back', 'Sent back'),
    ('Acc', 'accepted', 'Accepted'),
)
