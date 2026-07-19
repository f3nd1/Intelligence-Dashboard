# Criterion 3 Security and Privacy

Criterion 3 contains personal, contractual, financial and credential-related
fields. Analytics must apply data minimisation.

## Never expose in dashboards, exports, diagnostics or Ask UCC answers

### Credentials

- Agent.`username`
- Agent.`password`

The field names exist in the supplied DocType. Their values must never be read,
logged, exported or returned by an API.

### Banking information

- `agent_bank_branch`
- `agent_account_number`
- `agent_bank_address`
- `agent_swift_code`
- `agent_account_name`
- intermediary bank fields

### Personal identifiers

- Agent.`nric_passport`
- Agent Contract.`personal_id`
- NDA.`personal_id`
- Agent Claim Form.`nric`

### Signatures and attachments

- signatures;
- company stamps;
- UCC signature images;
- business-registration attachments;
- company-profile attachments;
- additional documents;
- contract and preview URLs.

### Contact details

Email, phone and addresses should appear only where operationally necessary and
where the current user has permission.

## Safe default analytics fields

Prefer:

- record name;
- status;
- dates;
- counts;
- completion flags;
- rating values;
- source availability;
- anonymised or aggregated outcomes.

## API rules

- `Allow Guest` must be disabled.
- Use Frappe permission checks for every DocType.
- Use an allow-list for fields and drill-down columns.
- Do not return arbitrary requested fields.
- Do not log document payloads.
- Limit record pages and exports.
