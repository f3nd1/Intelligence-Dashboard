# Criterion 3 DocType Inventory

## Primary inventory

| DocType | Module | Criterion use | Key relationships | Confidence |
|---|---|---|---|---|
| Agent | Educ Sg | Master record for application, selection, approval, monitoring, renewal, risk and exit | Student via `custom_agent`; Agent Contract; NDA; Provider Rating; Provider; multiple child tables | Confirmed |
| External Onboarding | Educ Sg | Onboarding execution for Agent, Provider or Teacher | `agent_id` → Agent; `onboarding_template`; `activities`; `signature_ref` | Confirmed |
| External Offboarding | Educ Sg | Separation and offboarding execution | `agent_id` → Agent; `offboarding_template`; `activities` | Confirmed |
| Provider Rating | Educ Sg | Screening, renewal review and exit evaluation | Dynamic Link using `type` + `document`; template and child assessment rows | Confirmed |
| Supplier Rating Assessment Childtable | Educ Sg | Weighted Likert criteria used by Provider Rating | `criteria` → Provider Criteria | Confirmed |
| Agent Claim Form | Educ Sg | Agent commission and additional-claim processing | `claims` and `extra` child tables | Confirmed |
| Agent Annual Performance Review | Educ Sg | Annual activity, survey, targets and internal review | `agent_name` → Agent; `year` → Academic Year | Confirmed |
| Agent Contract | Educ Sg | First appointment and renewal contract | `ac_agent_link_agent_contract` → Agent; optional NDA link | Confirmed |
| Non Disclosure Agreement | Educ Sg | NDA lifecycle and signatures | `agent_contract` → Agent Contract | Confirmed |
| Student Applicant | Existing Education/Criterion 4 mapping | Recruitment outcomes and applicant linkage | Agent link already used by existing implementation | Confirmed by user; reuse existing mapping |

## Referenced supporting DocTypes and child tables

The following are referenced by the supplied definitions but their full metadata
was not supplied:

- Agent Registration Childtable
- Agent School Childtable
- Agent Recruit Childtable
- Agent Yearly Recruitment Childtable
- Agent Submission Document Childtable
- Agent Provider Rating Childtable
- Agent Training and Review Log
- Agent Rating List Childtable
- Agents Monitoring Childtable
- Agents Evaluation Childtable
- Agent Student Onboarding Feedback
- Agent Claim Form Details Childtable
- Agent Claim Form Extra Childtable
- Agent Annual Performance Review Student Childtable
- Employee Boarding Activity
- Checklist Template
- Checklist List
- Contract Signature
- Provider Rating Template
- Provider Criteria
- Risk Identification Childtable
- Risk Justification Childtable
- Exit Interview
- User Email List
- Provider

These may be queried only after their field definitions are confirmed.
