# Criterion 3 Field Reference

This reference records the fields relevant to analytics and workflow mapping.
It is not an instruction to expose every field.

## Agent

### Identity and lifecycle

| Field | Type | Purpose |
|---|---|---|
| `status` | Select | For Approval, For Internal Use, Active, Inactive, Suspended, Terminated, Under Review, Prospective, Pending Verification |
| `applying_as_company` | Check | Individual/company application indicator |
| `agent_or_company_name` | Data | Display title |
| `date_of_registration` | Date | Company registration date |
| `expiry_date` | Date | Agent expiry date |
| `custom_ra_application_form_date` | Date | Recruitment-agent application date |
| `registration_no` | Data | Registration identifier |
| `place_of_registration` | Select | Registration country |
| `countries_of_recruitment` | Data | Approved or declared recruitment territories |
| `agent_search_type` | Select | Proactive or Reactive |
| `identification_types` | Select | Proactive or Reactive |
| `supplier` | Link Provider | Related provider |
| `contract` | Link Agent Contract | Current contract |
| `nda` | Link Non Disclosure Agreement | Current NDA |
| `agent_owner` | Link User | Record owner |

### Contact and organisation

- `telephone_no`
- `email`
- `full_address`
- `registered_address`
- `fax_no`
- `ceo_first_name`
- `ceo_last_name`
- `ceo_position`
- `co_first_name`
- `co_last_name`
- `co_position`
- `company_description`
- `company_experience`

### Recruitment capability and strategy

- `has_representation`
- `school_representation`
- `recruited_students_yearly`
- `has_experience`
- `school_recruit`
- `outside_sg`
- `students_ucc_yearly`
- `1st_quarter_target`
- `2nd_quarter_target`
- `3rd_quarter_target`
- `4th_quarter_target`
- `exhibition`
- `online_marketing`
- `seminar_talk`
- `school_talk`
- `one_to_one`
- `advertisement`
- `others`
- `please_specify`
- `details_service_fees`

### Application evidence

- `referee_name`
- `referee_position`
- `referee_phone`
- `referee_organization`
- `referee_email`
- `relationship_to_applicant`
- `business_registration`
- `table_vsbe`
- `company_profile`
- `additional_documents`
- `name_of_applicant`
- `date`
- `nric_passport`
- `signature`

### Approval and selection

- `employee`
- `processing_officer`
- `processing_officer_name`
- `processed_date`
- `approved_by`
- `approved_by_full_name`
- `approved_date`
- `share_values_rating`
- `legal_rating`
- `partnership_rating`
- `collaborative_rating`
- `financial_rating`
- `communication_rating`
- `cultural_rating`
- `support_rating`
- `sustainability_rating`
- `provider_rating`
- `average_identification_and_selection_score`
- `remarks`
- `rating`

### Onboarding, monitoring and renewal

- `checklist_template`
- `onboarding_checklist`
- `training_log`
- `done_consent_and_onboarding_survey`
- `onboarding_survey_date`
- `agent_rating_list`
- `agent_monitoring_childtable`
- `monitoring_summary`
- `table_tczl`
- `student_feedback`
- `text_editor_pftn`

### Exit and risk

- `resignation_letter_date`
- `relieving_date`
- `exit_interview_held_on`
- `exit_interview`
- `reason_for_leaving`
- `feedback`
- `risk_assessment`
- `risk_management`

### Financial and commission configuration

- `registration`
- `fc_commission`
- `sc_commission`
- banking fields exist but must not be exposed in analytics; see `SECURITY_AND_PRIVACY.md`

## External Onboarding

| Field | Type | Use |
|---|---|---|
| `document_type` | Select | Agent, Provider or Teacher |
| `agent_id` | Link Agent | Agent being onboarded |
| `agent_name` | Data | Fetched agent name |
| `date_of_joining` | Date | Joining date |
| `onboarding_begins_on` | Date | Workflow start |
| `onboarding_template` | Link | Employee Onboarding Template |
| `activities` | Table | Employee Boarding Activity |
| `signature_ref` | Link | Contract Signature |
| `party_signature` | Signature | Signed confirmation |
| `signed_date` | Date | Signature date |
| `signed_date_and_time` | Datetime | Signature timestamp |

## External Offboarding

| Field | Type | Use |
|---|---|---|
| `document_type` | Select | Agent, Provider or Teacher |
| `agent_id` | Link Agent | Agent being offboarded |
| `agent_name` | Data | Fetched agent name |
| `separation_begins_on` | Date | Offboarding start |
| `offboarding_template` | Link | Employee Separation Template |
| `activities` | Table | Employee Boarding Activity |
| `party_signature` | Signature | Signed confirmation |
| `signed_date` | Date | Signature date |

## Provider Rating

### Core fields

- `posting_date`
- `year`
- `status`
- `type`
- `document`
- `supplier`
- `evaluation_stage`
- `rating`
- `rating_likert`
- `assessment_template`
- `assessment`
- `note`

### Status values supplied

- Approved
- Approved for Continuation
- On Hold
- On Hold (Future Consideration)
- Pending
- Terminated

### Evaluation-stage values

- Identification and Screening
- Renewal and Regular Review
- Exit / Termination

## Supplier Rating Assessment Childtable

- `criteria` → Provider Criteria
- `maximum_score`
- `rating` — Likert 1–5
- `score` — percentage
- `note`

## Agent Claim Form

- `year`
- `month`
- `agent`
- `full_name`
- `email`
- `claims`
- `teaching_total`
- `extra`
- `extra_total`
- `grand_total`
- `docstatus` is available because the DocType is submittable

## Agent Annual Performance Review

### Recruitment and planning

- `no_of_students`
- `recruitment_activities`
- `challenges_and_reccomendations` — legacy
- `challenges_2025`
- `reccomendations_2025`
- `1st_quarter`
- `2nd_quarter`
- `3rd_quarter`
- `4th_quarter`
- `next_year_student_recruitment_target`
- `planned_strategies`

### Survey ratings

- `survey_training`
- `survey_comm`
- `survey_marketing`
- `survey_stakeholder`
- `survey_pdpa`
- `survey_isms`
- `survey_overall`
- `survey_satisfaction`

### Internal review

- `agent_name` → Agent
- `agent_full_name`
- `year` → Academic Year
- `date_of_review`
- `reviewed_by`
- `user_name`
- `feedback`
- `rating_recognition`
- `rating_pro_development`
- `rating_agent_recommend`
- `rating_policies_clarity`
- `rating_support_resources`
- `rating_communication`

## Agent Contract

### Contract lifecycle

- `party_name`
- `personal_id`
- `posting_date`
- `email`
- `preview_link`
- `start_date`
- `valid_for_days`
- `expires_on`
- `end_date`
- `contract_type` — First-time Agreement or Renewal
- `agreement_duratio_mou`
- `docstatus`

### NDA and signatures

- `requires_nda`
- `nda_purpose_nda`
- `non_disclosure_agreement`
- `nda_acknowledged`
- `nda_signed_date`
- `party_signature`
- `signed_date`
- `name_of_representative`
- `party_designation`
- `ucc_signed_name`
- `ucc_signed_title`
- `ucc_signature`
- `ucc_signed_date`

### Agent relationship and commercial configuration

- `ac_agent_link_agent_contract` → Agent
- `ac_name_of_agent`
- `ac_company_registration`
- `ac_territory_country`
- `ac_agreement_duration`
- `ac_minimum_target_survey`
- `ac_number_intake`
- `ac_commission_maximum`
- `ac_agent_commision`

## Non Disclosure Agreement

- `status`
- `party_name`
- `personal_id`
- `email`
- `posting_date`
- `preview_link`
- `agent_contract`
- `nda_purpose_nda`
- `nda_party_information`
- `start_date`
- `valid_for_days`
- `expires_on`
- `end_date`
- `agreement_duratio_mou`
- `party_signature`
- `signed_date`
- `ucc_signed_name`
- `ucc_signed_title`
- `ucc_signature`
- `ucc_signed_date`
- `docstatus`
