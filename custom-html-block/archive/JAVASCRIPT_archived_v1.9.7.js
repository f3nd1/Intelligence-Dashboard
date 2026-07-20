/*
 * UCC Intelligence Platform - ARCHIVED VISUAL DEFINITIONS (v1.9.7)
 *
 * These are the 415 visual definitions that were disabled in the Step #4 audit
 * reduction and then PHYSICALLY REMOVED from the live custom-html-block/JAVASCRIPT.js
 * to shrink the deployed file. This file is NOT loaded by the Custom HTML Block.
 * The human-readable list of what was cut and why is in
 * documentation/archived-visuals.md.
 *
 * TO RESTORE A VISUAL:
 *  - Criteria 1/2/3/6/7: copy its entry object (it keeps its original "i" index)
 *    from LIVE_ARCHIVED[criterion][section] below back into the
 *    LIVE_VISUAL_EXPANSION[criterion][section] array in
 *    src/js/30-live-foundation-runtime.js. The "i" field preserves its original
 *    metric-window index so it renders exactly as before.
 *  - Criterion 4: copy its entry from C4_ARCHIVED[section] back into
 *    C4_VISUAL_EXPANSION[section] in src/js/10-platform-runtime.js.
 *  - Criterion 5: it is a static HTML card (still present in HTML.html, hidden via
 *    C5_DISABLED_VISUALS). Remove its id from the C5_DISABLED_VISUALS set in
 *    src/js/10-platform-runtime.js and copy its description from C5_ARCHIVED_DESCRIPTIONS
 *    below back into C5_VISUAL_DESCRIPTIONS.
 *  - Then bump the affected criterion's count in tools/validate_package.py
 *    (EXPECTED_VISUALS) and VERSION.json (diagram_counts, visual_targets), rebuild.
 */

const LIVE_ARCHIVED = {
 "criterion_1": {
  "overview": [
   {
    "id": "v190-c1-overview-03",
    "title": "Leadership System Health",
    "type": "funnel",
    "description": "Tracks how leadership records move from raised to fully resolved across the system.",
    "i": 2
   },
   {
    "id": "v190-c1-overview-04",
    "title": "Governance-to-Improvement Lifecycle",
    "type": "lifecycle",
    "description": "Maps the stages a governance issue passes through on its way to improvement.",
    "i": 3
   },
   {
    "id": "v190-c1-overview-05",
    "title": "Governance Exception Funnel",
    "type": "radar",
    "description": "Highlights where governance exceptions are concentrated across different control areas.",
    "i": 4
   },
   {
    "id": "v190-c1-overview-07",
    "title": "Board and Committee Activity",
    "type": "gauge",
    "description": "Gauges how active board and committee meetings have been against expectations.",
    "i": 6
   },
   {
    "id": "v190-c1-overview-09",
    "title": "Decision Closure Performance",
    "type": "bar",
    "description": "Compares how quickly leadership decisions are being closed out across periods.",
    "i": 8
   },
   {
    "id": "v190-c1-overview-10",
    "title": "Policy Ownership Coverage",
    "type": "donut",
    "description": "Shows the share of governance policies that have a clearly named owner.",
    "i": 9
   },
   {
    "id": "v190-c1-overview-11",
    "title": "Policy Review Timeliness",
    "type": "funnel",
    "description": "Tracks policies moving from due for review through to actually reviewed on time.",
    "i": 10
   },
   {
    "id": "v190-c1-overview-12",
    "title": "Strategic Objective Portfolio",
    "type": "lifecycle",
    "description": "Follows strategic objectives through their lifecycle from set to achieved.",
    "i": 11
   },
   {
    "id": "v190-c1-overview-13",
    "title": "Strategic Initiative Progress",
    "type": "radar",
    "description": "Compares progress across the different strategic initiatives currently underway.",
    "i": 12
   },
   {
    "id": "v190-c1-overview-14",
    "title": "Department Contribution Profile",
    "type": "matrix",
    "description": "Grids each department's contribution to governance and strategic objectives.",
    "i": 13
   },
   {
    "id": "v190-c1-overview-15",
    "title": "Stakeholder Engagement Coverage",
    "type": "gauge",
    "description": "Gauges how many stakeholder groups have been engaged in governance and planning.",
    "i": 14
   },
   {
    "id": "v190-c1-overview-16",
    "title": "Management Review Follow-up",
    "type": "trend",
    "description": "Tracks how consistently management review actions are followed up over time.",
    "i": 15
   },
   {
    "id": "v190-c1-overview-18",
    "title": "Strategic Risk Exposure",
    "type": "donut",
    "description": "Shows the share of strategic risks that remain open versus mitigated.",
    "i": 17
   },
   {
    "id": "v190-c1-overview-19",
    "title": "Action Ownership Readiness",
    "type": "funnel",
    "description": "Tracks governance and strategy actions from raised through to a named owner.",
    "i": 18
   },
   {
    "id": "v190-c1-overview-21",
    "title": "Annual Governance Trend",
    "type": "radar",
    "description": "Compares governance performance across recent years on several dimensions at once.",
    "i": 20
   },
   {
    "id": "v190-c1-overview-22",
    "title": "Annual Strategy Trend",
    "type": "matrix",
    "description": "Grids strategic planning performance by year against each measured dimension.",
    "i": 21
   },
   {
    "id": "v190-c1-overview-23",
    "title": "Leadership Control Maturity",
    "type": "gauge",
    "description": "Gauges how mature leadership controls are against the expected standard.",
    "i": 22
   },
   {
    "id": "v190-c1-overview-24",
    "title": "Strategy Execution Maturity",
    "type": "trend",
    "description": "Tracks how strategy execution maturity has changed over recent reporting periods.",
    "i": 23
   },
   {
    "id": "v190-c1-overview-25",
    "title": "Open Governance Actions",
    "type": "bar",
    "description": "Compares how many governance actions remain open across different owners or areas.",
    "i": 24
   },
   {
    "id": "v190-c1-overview-26",
    "title": "Open Strategic Actions",
    "type": "donut",
    "description": "Shows the share of strategic actions that are still open versus closed.",
    "i": 25
   }
  ],
  "1.1.1": [
   {
    "id": "v190-c1-111-07",
    "title": "Leadership Structure Coverage",
    "type": "gauge",
    "description": "Gauges how complete the documented leadership and reporting structure currently is.",
    "i": 6
   },
   {
    "id": "v190-c1-111-08",
    "title": "Role Description Completeness",
    "type": "trend",
    "description": "Tracks over time how many leadership roles have a complete role description.",
    "i": 7
   },
   {
    "id": "v190-c1-111-09",
    "title": "Delegation and Authority Coverage",
    "type": "bar",
    "description": "Compares how many roles have documented delegation of authority in place.",
    "i": 8
   },
   {
    "id": "v190-c1-111-10",
    "title": "Committee Meeting Cadence",
    "type": "donut",
    "description": "Shows how committee meetings are distributed across their scheduled cadence.",
    "i": 9
   },
   {
    "id": "v190-c1-111-11",
    "title": "Meeting Attendance Profile",
    "type": "funnel",
    "description": "Tracks committee members from invited through to actually attending meetings.",
    "i": 10
   },
   {
    "id": "v190-c1-111-12",
    "title": "Decision Register Status",
    "type": "lifecycle",
    "description": "Follows governance decisions from logged through to formally closed out.",
    "i": 11
   },
   {
    "id": "v190-c1-111-13",
    "title": "Decision Closure Ageing",
    "type": "radar",
    "description": "Compares how long open governance decisions have been waiting for closure.",
    "i": 12
   },
   {
    "id": "v190-c1-111-14",
    "title": "Governance Action Funnel",
    "type": "matrix",
    "description": "Grids governance actions by status against the area they belong to.",
    "i": 13
   },
   {
    "id": "v190-c1-111-16",
    "title": "Policy Review Calendar",
    "type": "trend",
    "description": "Tracks upcoming and overdue governance policy reviews across the year.",
    "i": 15
   },
   {
    "id": "v190-c1-111-17",
    "title": "Policy Owner Distribution",
    "type": "bar",
    "description": "Compares how governance policies are distributed across their named owners.",
    "i": 16
   },
   {
    "id": "v190-c1-111-18",
    "title": "Governance Risk Matrix",
    "type": "donut",
    "description": "Shows the mix of governance risks by severity or category.",
    "i": 17
   },
   {
    "id": "v190-c1-111-20",
    "title": "Stakeholder Accountability",
    "type": "lifecycle",
    "description": "Follows how stakeholder accountability commitments move from made to fulfilled.",
    "i": 19
   },
   {
    "id": "v190-c1-111-21",
    "title": "Communication of Governance Decisions",
    "type": "radar",
    "description": "Compares how well governance decisions have been communicated across stakeholder groups.",
    "i": 20
   },
   {
    "id": "v190-c1-111-23",
    "title": "Management Review Escalations",
    "type": "gauge",
    "description": "Gauges how many issues raised in management review still need escalation.",
    "i": 22
   },
   {
    "id": "v190-c1-111-24",
    "title": "Leadership Exception Profile",
    "type": "trend",
    "description": "Tracks how leadership and governance exceptions have trended over recent periods.",
    "i": 23
   },
   {
    "id": "v190-c1-111-25",
    "title": "Governance Trend by Period",
    "type": "bar",
    "description": "Compares overall governance performance across each recent reporting period.",
    "i": 24
   },
   {
    "id": "v190-c1-111-26",
    "title": "Action Effectiveness",
    "type": "donut",
    "description": "Shows what share of governance actions were assessed as effective once closed.",
    "i": 25
   }
  ],
  "1.2.1": [
   {
    "id": "v190-c1-121-05",
    "title": "Strategic Gap Funnel",
    "type": "radar",
    "description": "Compares the size of strategic gaps identified across different planning areas.",
    "i": 4
   },
   {
    "id": "v190-c1-121-07",
    "title": "Objective Portfolio by Status",
    "type": "gauge",
    "description": "Gauges how the portfolio of strategic objectives is distributed by current status.",
    "i": 6
   },
   {
    "id": "v190-c1-121-08",
    "title": "Initiative Portfolio by Status",
    "type": "trend",
    "description": "Tracks how the status of strategic initiatives has shifted over recent periods.",
    "i": 7
   },
   {
    "id": "v190-c1-121-11",
    "title": "Milestone Delay Ageing",
    "type": "funnel",
    "description": "Tracks delayed milestones from just overdue through to significantly behind schedule.",
    "i": 10
   },
   {
    "id": "v190-c1-121-12",
    "title": "Department Alignment",
    "type": "lifecycle",
    "description": "Follows how each department's plans move from set through to aligned with strategy.",
    "i": 11
   },
   {
    "id": "v190-c1-121-13",
    "title": "Resource Alignment",
    "type": "radar",
    "description": "Compares how well resources are aligned to each strategic objective.",
    "i": 12
   },
   {
    "id": "v190-c1-121-14",
    "title": "Risk-to-Objective Matrix",
    "type": "matrix",
    "description": "Grids identified risks against the strategic objectives they could affect.",
    "i": 13
   },
   {
    "id": "v190-c1-121-15",
    "title": "Stakeholder Input Coverage",
    "type": "gauge",
    "description": "Gauges how much stakeholder input has been captured during strategic planning.",
    "i": 14
   },
   {
    "id": "v190-c1-121-17",
    "title": "Annual Planning Cycle",
    "type": "bar",
    "description": "Compares strategic planning activity across the stages of the annual planning cycle.",
    "i": 16
   },
   {
    "id": "v190-c1-121-18",
    "title": "Quarterly Review Cadence",
    "type": "donut",
    "description": "Shows how quarterly strategy reviews are distributed across the reporting year.",
    "i": 17
   },
   {
    "id": "v190-c1-121-19",
    "title": "Management Review Inputs",
    "type": "funnel",
    "description": "Tracks strategic planning inputs from submitted through to accepted into management review.",
    "i": 18
   },
   {
    "id": "v190-c1-121-20",
    "title": "Management Review Outputs",
    "type": "lifecycle",
    "description": "Follows management review outputs from raised through to implemented in the plan.",
    "i": 19
   },
   {
    "id": "v190-c1-121-21",
    "title": "Improvement Action Linkage",
    "type": "radar",
    "description": "Compares how well improvement actions are linked back to strategic objectives.",
    "i": 20
   },
   {
    "id": "v190-c1-121-23",
    "title": "Strategic Measure Availability",
    "type": "gauge",
    "description": "Gauges how many strategic objectives have a measurable indicator defined.",
    "i": 22
   },
   {
    "id": "v190-c1-121-24",
    "title": "Strategic Exception Profile",
    "type": "trend",
    "description": "Tracks how strategic planning exceptions have trended across recent reporting periods.",
    "i": 23
   },
   {
    "id": "v190-c1-121-25",
    "title": "Objective Achievement Trend",
    "type": "bar",
    "description": "Compares strategic objective achievement rates across recent reporting periods.",
    "i": 24
   },
   {
    "id": "v190-c1-121-26",
    "title": "Initiative Completion Trend",
    "type": "donut",
    "description": "Shows how the completion rate of strategic initiatives has changed recently.",
    "i": 25
   }
  ]
 },
 "criterion_2": {
  "overview": [
   {
    "id": "v190-c2-overview-07",
    "title": "Workforce Control Profile",
    "type": "gauge",
    "description": "Gauges how well workforce controls are in place across staff selection and management.",
    "i": 6
   },
   {
    "id": "v190-c2-overview-08",
    "title": "Training Control Profile",
    "type": "trend",
    "description": "Gauges how well training controls are covering staff development needs.",
    "i": 7
   },
   {
    "id": "v190-c2-overview-09",
    "title": "Communication Control Profile",
    "type": "bar",
    "description": "Compares how well communication controls are in place across internal and external channels.",
    "i": 8
   },
   {
    "id": "v190-c2-overview-10",
    "title": "Information Control Profile",
    "type": "donut",
    "description": "Shows how well information and data controls are covering this criterion.",
    "i": 9
   },
   {
    "id": "v190-c2-overview-11",
    "title": "Knowledge Control Profile",
    "type": "funnel",
    "description": "Tracks knowledge management controls from missing through to fully in place.",
    "i": 10
   }
  ],
  "2.1.1": [
   {
    "id": "v190-c2-211-03",
    "title": "Recruitment and Onboarding Funnel",
    "type": "funnel",
    "description": "Tracks candidates from application through recruitment to onboarding completion.",
    "i": 2
   },
   {
    "id": "v190-c2-211-05",
    "title": "Hiring Exception Profile",
    "type": "radar",
    "description": "Compares where hiring exceptions are concentrated across recruitment stages.",
    "i": 4
   },
   {
    "id": "v190-c2-211-06",
    "title": "Employment Lifecycle Trend",
    "type": "matrix",
    "description": "Grids employment lifecycle events by month to show hiring activity over time.",
    "i": 5
   },
   {
    "id": "v190-c2-211-07",
    "title": "Manpower Plan Coverage",
    "type": "gauge",
    "description": "Gauges how much of the approved manpower plan has been filled.",
    "i": 6
   },
   {
    "id": "v190-c2-211-08",
    "title": "Requisition Approval Readiness",
    "type": "trend",
    "description": "Tracks manpower requisitions from submitted through to fully approved.",
    "i": 7
   },
   {
    "id": "v190-c2-211-09",
    "title": "Candidate Screening Status",
    "type": "bar",
    "description": "Compares how candidates are distributed across each stage of screening.",
    "i": 8
   },
   {
    "id": "v190-c2-211-10",
    "title": "Interview Assessment Coverage",
    "type": "donut",
    "description": "Shows what share of candidates have completed a documented interview assessment.",
    "i": 9
   },
   {
    "id": "v190-c2-211-11",
    "title": "Appointment and Onboarding Status",
    "type": "funnel",
    "description": "Tracks new hires from offer accepted through to onboarding completion.",
    "i": 10
   }
  ],
  "2.1.2": [
   {
    "id": "v190-c2-212-03",
    "title": "Training Needs Funnel",
    "type": "funnel",
    "description": "Tracks identified training needs from raised through to a scheduled course.",
    "i": 2
   },
   {
    "id": "v190-c2-212-04",
    "title": "Competency Readiness",
    "type": "lifecycle",
    "description": "Follows staff competency records from assessed through to confirmed as ready.",
    "i": 3
   },
   {
    "id": "v190-c2-212-05",
    "title": "Training Exception Profile",
    "type": "radar",
    "description": "Compares where training exceptions are concentrated across roles or departments.",
    "i": 4
   },
   {
    "id": "v190-c2-212-06",
    "title": "Training Completion Trend",
    "type": "matrix",
    "description": "Grids training completion rates by month to show trends over the year.",
    "i": 5
   },
   {
    "id": "v190-c2-212-07",
    "title": "Training Plan Coverage",
    "type": "gauge",
    "description": "Gauges how much of the approved training plan has been delivered.",
    "i": 6
   },
   {
    "id": "v190-c2-212-08",
    "title": "Mandatory Training Status",
    "type": "trend",
    "description": "Tracks mandatory training from assigned through to confirmed complete.",
    "i": 7
   },
   {
    "id": "v190-c2-212-09",
    "title": "Role-Specific Training Coverage",
    "type": "bar",
    "description": "Compares training coverage for role-specific courses across staff groups.",
    "i": 8
   },
   {
    "id": "v190-c2-212-10",
    "title": "Training Effectiveness",
    "type": "donut",
    "description": "Shows what share of completed training was assessed as effective.",
    "i": 9
   }
  ],
  "2.2.1": [
   {
    "id": "v190-c2-221-03",
    "title": "Communication Approval Funnel",
    "type": "funnel",
    "description": "Tracks communications from drafted through to formal approval.",
    "i": 2
   },
   {
    "id": "v190-c2-221-04",
    "title": "Channel Readiness",
    "type": "lifecycle",
    "description": "Follows each communication channel from unverified through to confirmed ready for use.",
    "i": 3
   },
   {
    "id": "v190-c2-221-05",
    "title": "Communication Exception Profile",
    "type": "radar",
    "description": "Compares where communication exceptions are concentrated across channels.",
    "i": 4
   },
   {
    "id": "v190-c2-221-06",
    "title": "Communication Trend",
    "type": "matrix",
    "description": "Grids communication activity by month to show trends over the reporting period.",
    "i": 5
   },
   {
    "id": "v190-c2-221-07",
    "title": "Internal Communication Activity",
    "type": "gauge",
    "description": "Gauges how active internal communication has been against expectations.",
    "i": 6
   },
   {
    "id": "v190-c2-221-08",
    "title": "External Communication Activity",
    "type": "trend",
    "description": "Tracks external communication activity over recent reporting periods.",
    "i": 7
   },
   {
    "id": "v190-c2-221-09",
    "title": "Stakeholder Channel Coverage",
    "type": "bar",
    "description": "Compares stakeholder channel coverage across the communication types offered.",
    "i": 8
   },
   {
    "id": "v190-c2-221-10",
    "title": "Approval-Level Distribution",
    "type": "donut",
    "description": "Shows how communications are distributed across each required approval level.",
    "i": 9
   }
  ],
  "2.3.1": [
   {
    "id": "v190-c2-231-03",
    "title": "Data Collection Lifecycle",
    "type": "funnel",
    "description": "Tracks data records from collected through to properly filed and controlled.",
    "i": 2
   },
   {
    "id": "v190-c2-231-05",
    "title": "Data Exception Profile",
    "type": "radar",
    "description": "Compares where data exceptions are concentrated across data management areas.",
    "i": 4
   },
   {
    "id": "v190-c2-231-06",
    "title": "Data Quality Trend",
    "type": "matrix",
    "description": "Grids data quality trend results by month to show progress over time.",
    "i": 5
   },
   {
    "id": "v190-c2-231-07",
    "title": "Consent Coverage",
    "type": "gauge",
    "description": "Gauges what share of records have the required consent captured.",
    "i": 6
   },
   {
    "id": "v190-c2-231-08",
    "title": "Access Control Coverage",
    "type": "trend",
    "description": "Tracks how access control coverage has changed across recent periods.",
    "i": 7
   },
   {
    "id": "v190-c2-231-09",
    "title": "Data Classification Coverage",
    "type": "bar",
    "description": "Compares how data records are distributed across classification levels.",
    "i": 8
   },
   {
    "id": "v190-c2-231-10",
    "title": "Retention and Disposal Status",
    "type": "donut",
    "description": "Shows the status mix of records against retention and disposal requirements.",
    "i": 9
   },
   {
    "id": "v190-c2-231-11",
    "title": "Data Source Integration Readiness",
    "type": "funnel",
    "description": "Tracks data source integration from unread through to fully connected.",
    "i": 10
   }
  ],
  "2.3.2": [
   {
    "id": "v190-c2-232-03",
    "title": "Document Lifecycle",
    "type": "funnel",
    "description": "Tracks documents from drafted through review to formal publication.",
    "i": 2
   },
   {
    "id": "v190-c2-232-05",
    "title": "Knowledge Exception Profile",
    "type": "radar",
    "description": "Compares where knowledge management exceptions are concentrated across document types.",
    "i": 4
   },
   {
    "id": "v190-c2-232-06",
    "title": "Document Review Trend",
    "type": "matrix",
    "description": "Grids document review activity by month to show trends over time.",
    "i": 5
   },
   {
    "id": "v190-c2-232-07",
    "title": "Controlled Document Coverage",
    "type": "gauge",
    "description": "Gauges what share of controlled documents are correctly version-controlled.",
    "i": 6
   },
   {
    "id": "v190-c2-232-08",
    "title": "Document Version Currency",
    "type": "trend",
    "description": "Tracks how up to date controlled documents are against their review cycle.",
    "i": 7
   },
   {
    "id": "v190-c2-232-09",
    "title": "Document Owner Coverage",
    "type": "bar",
    "description": "Compares document ownership coverage across the knowledge repository.",
    "i": 8
   },
   {
    "id": "v190-c2-232-10",
    "title": "Obsolete Document Removal",
    "type": "donut",
    "description": "Shows what share of obsolete documents have been properly removed.",
    "i": 9
   },
   {
    "id": "v190-c2-232-11",
    "title": "Knowledge Access Readiness",
    "type": "funnel",
    "description": "Tracks knowledge access readiness from restricted through to confirmed available.",
    "i": 10
   }
  ],
  "2.4.1": [
   {
    "id": "v190-c2-241-03",
    "title": "Feedback Handling Funnel",
    "type": "funnel",
    "description": "Tracks feedback from received through to fully handled and closed.",
    "i": 2
   },
   {
    "id": "v190-c2-241-04",
    "title": "Feedback Readiness",
    "type": "lifecycle",
    "description": "Follows feedback readiness checks from incomplete through to confirmed ready.",
    "i": 3
   },
   {
    "id": "v190-c2-241-05",
    "title": "Feedback Exception Profile",
    "type": "radar",
    "description": "Compares where feedback handling exceptions are concentrated across channels.",
    "i": 4
   },
   {
    "id": "v190-c2-241-06",
    "title": "Feedback Closure Trend",
    "type": "matrix",
    "description": "Grids feedback closure activity by month to show trends over time.",
    "i": 5
   },
   {
    "id": "v190-c2-241-07",
    "title": "Feedback Channel Distribution",
    "type": "gauge",
    "description": "Shows how feedback is distributed across the channels it was received through.",
    "i": 6
   },
   {
    "id": "v190-c2-241-08",
    "title": "Feedback Priority Matrix",
    "type": "trend",
    "description": "Tracks feedback priority levels against how quickly each is being closed.",
    "i": 7
   },
   {
    "id": "v190-c2-241-09",
    "title": "Acknowledgement Timeliness",
    "type": "bar",
    "description": "Compares how quickly feedback is being formally acknowledged.",
    "i": 8
   },
   {
    "id": "v190-c2-241-10",
    "title": "Resolution Timeliness",
    "type": "donut",
    "description": "Shows what share of feedback was resolved within the expected timeframe.",
    "i": 9
   }
  ],
  "2.4.2": [
   {
    "id": "v190-c2-242-03",
    "title": "Survey Participation Funnel",
    "type": "funnel",
    "description": "Tracks students from invited through to actually completing a survey.",
    "i": 2
   },
   {
    "id": "v190-c2-242-05",
    "title": "Student Survey Exception Profile",
    "type": "radar",
    "description": "Compares where student survey exceptions are concentrated across survey types.",
    "i": 4
   },
   {
    "id": "v190-c2-242-06",
    "title": "Student Satisfaction Trend",
    "type": "matrix",
    "description": "Grids student satisfaction trend results by month to show progress over time.",
    "i": 5
   },
   {
    "id": "v190-c2-242-07",
    "title": "Survey Type Distribution",
    "type": "gauge",
    "description": "Shows how student surveys are distributed across the types offered.",
    "i": 6
   },
   {
    "id": "v190-c2-242-08",
    "title": "Question Response Coverage",
    "type": "trend",
    "description": "Tracks how much of each survey's questions received a response.",
    "i": 7
   },
   {
    "id": "v190-c2-242-09",
    "title": "Student Support Satisfaction",
    "type": "bar",
    "description": "Compares student satisfaction with the support services they received.",
    "i": 8
   },
   {
    "id": "v190-c2-242-10",
    "title": "Teaching and Learning Satisfaction",
    "type": "donut",
    "description": "Shows student satisfaction with the teaching and learning experience.",
    "i": 9
   },
   {
    "id": "v190-c2-242-11",
    "title": "Survey Improvement Actions",
    "type": "funnel",
    "description": "Tracks improvement actions raised from student surveys through to implementation.",
    "i": 10
   }
  ],
  "2.4.3": [
   {
    "id": "v190-c2-243-03",
    "title": "Survey Participation Funnel",
    "type": "funnel",
    "description": "Tracks staff from invited through to actually completing a survey.",
    "i": 2
   },
   {
    "id": "v190-c2-243-05",
    "title": "Staff Survey Exception Profile",
    "type": "radar",
    "description": "Compares where staff survey exceptions are concentrated across survey types.",
    "i": 4
   },
   {
    "id": "v190-c2-243-06",
    "title": "Staff Satisfaction Trend",
    "type": "matrix",
    "description": "Grids staff satisfaction trend results by month to show progress over time.",
    "i": 5
   },
   {
    "id": "v190-c2-243-07",
    "title": "Survey Type Distribution",
    "type": "gauge",
    "description": "Shows how staff surveys are distributed across the types offered.",
    "i": 6
   },
   {
    "id": "v190-c2-243-08",
    "title": "Engagement Dimension Profile",
    "type": "trend",
    "description": "Compares staff engagement across the different dimensions measured in the survey.",
    "i": 7
   },
   {
    "id": "v190-c2-243-09",
    "title": "Workplace Satisfaction",
    "type": "bar",
    "description": "Shows staff satisfaction with the overall workplace experience.",
    "i": 8
   },
   {
    "id": "v190-c2-243-10",
    "title": "Communication Satisfaction",
    "type": "donut",
    "description": "Compares staff satisfaction with internal communication specifically.",
    "i": 9
   },
   {
    "id": "v190-c2-243-11",
    "title": "Staff Improvement Actions",
    "type": "funnel",
    "description": "Tracks improvement actions raised from staff surveys through to implementation.",
    "i": 10
   }
  ]
 },
 "criterion_3": {
  "overview": [
   {
    "id": "v190-c3-overview-03",
    "title": "Agent Control Health",
    "type": "funnel",
    "description": "Tracks agent control issues from raised through to fully resolved.",
    "i": 2
   },
   {
    "id": "v190-c3-overview-04",
    "title": "Renewal and Evaluation Trend",
    "type": "lifecycle",
    "description": "Tracks renewal and evaluation activity across recent reporting periods.",
    "i": 3
   },
   {
    "id": "v190-c3-overview-08",
    "title": "Agent Territory Distribution",
    "type": "trend",
    "description": "Tracks how agents are distributed across their operating territories.",
    "i": 7
   },
   {
    "id": "v190-c3-overview-09",
    "title": "Agent Contract Coverage",
    "type": "bar",
    "description": "Compares how many agents have a fully documented contract on file.",
    "i": 8
   },
   {
    "id": "v190-c3-overview-11",
    "title": "Agent Onboarding Coverage",
    "type": "funnel",
    "description": "Tracks agents from selected through to fully onboarded.",
    "i": 10
   },
   {
    "id": "v190-c3-overview-12",
    "title": "Agent Review Coverage",
    "type": "lifecycle",
    "description": "Follows agent review coverage from scheduled through to completed.",
    "i": 11
   },
   {
    "id": "v190-c3-overview-13",
    "title": "Recruitment Contribution",
    "type": "radar",
    "description": "Compares how much each agent has contributed to recruitment overall.",
    "i": 12
   },
   {
    "id": "v190-c3-overview-14",
    "title": "Applicant Conversion Profile",
    "type": "matrix",
    "description": "Grids applicant conversion rates against each contributing agent.",
    "i": 13
   },
   {
    "id": "v190-c3-overview-15",
    "title": "Commission Activity",
    "type": "gauge",
    "description": "Gauges how much commission activity has occurred across agents.",
    "i": 14
   },
   {
    "id": "v190-c3-overview-16",
    "title": "Renewal Readiness",
    "type": "trend",
    "description": "Tracks how ready agent contracts are for their upcoming renewal.",
    "i": 15
   },
   {
    "id": "v190-c3-overview-17",
    "title": "Suspension and Termination Profile",
    "type": "bar",
    "description": "Compares suspension and termination activity across agents over time.",
    "i": 16
   },
   {
    "id": "v190-c3-overview-18",
    "title": "Offboarding Readiness",
    "type": "donut",
    "description": "Shows how ready offboarding records are for agents exiting the programme.",
    "i": 17
   },
   {
    "id": "v190-c3-overview-19",
    "title": "Agent Risk Profile",
    "type": "funnel",
    "description": "Tracks agent risk levels from identified through to mitigated.",
    "i": 18
   },
   {
    "id": "v190-c3-overview-21",
    "title": "Annual Agent Trend",
    "type": "radar",
    "description": "Compares agent performance across recent years on several dimensions at once.",
    "i": 20
   },
   {
    "id": "v190-c3-overview-22",
    "title": "Contract Expiry Trend",
    "type": "matrix",
    "description": "Grids agent contract expiry dates against each contract on file.",
    "i": 21
   },
   {
    "id": "v190-c3-overview-23",
    "title": "Review Outcome Trend",
    "type": "gauge",
    "description": "Gauges how agent reviews have trended toward positive or negative outcomes.",
    "i": 22
   },
   {
    "id": "v190-c3-overview-24",
    "title": "Claim Amount Trend",
    "type": "trend",
    "description": "Tracks agent claim amounts across recent reporting periods.",
    "i": 23
   },
   {
    "id": "v190-c3-overview-25",
    "title": "Agent Performance Radar",
    "type": "bar",
    "description": "Compares agent performance across several measured dimensions at once.",
    "i": 24
   },
   {
    "id": "v190-c3-overview-26",
    "title": "Agent Lifecycle Funnel",
    "type": "donut",
    "description": "Shows agents by lifecycle stage, from identified through to active.",
    "i": 25
   },
   {
    "id": "v190-c3-overview-27",
    "title": "Agent Control Matrix",
    "type": "funnel",
    "description": "Grids agent control status against each management area.",
    "i": 26
   },
   {
    "id": "v190-c3-overview-29",
    "title": "Agent Source Readiness",
    "type": "radar",
    "description": "Compares how readable the underlying agent data sources currently are.",
    "i": 28
   },
   {
    "id": "v190-c3-overview-30",
    "title": "Agent Metric Readiness",
    "type": "matrix",
    "description": "Follows agent metrics from unavailable through to fully calculated and ready.",
    "i": 29
   }
  ],
  "3.1.1": [
   {
    "id": "v190-c3-311-03",
    "title": "Selection Criteria Weighting",
    "type": "funnel",
    "description": "Grids the weighting applied to each selection criterion used for agents.",
    "i": 2
   },
   {
    "id": "v190-c3-311-04",
    "title": "Selection Score Distribution",
    "type": "lifecycle",
    "description": "Shows how selection scores are distributed across candidate agents.",
    "i": 3
   },
   {
    "id": "v190-c3-311-08",
    "title": "Application Volume",
    "type": "trend",
    "description": "Tracks agent application volume across recent reporting periods.",
    "i": 7
   },
   {
    "id": "v190-c3-311-09",
    "title": "Application Completeness",
    "type": "bar",
    "description": "Compares how complete each agent application is against requirements.",
    "i": 8
   },
   {
    "id": "v190-c3-311-10",
    "title": "Application Processing Time",
    "type": "donut",
    "description": "Shows how long agent applications take to move through processing.",
    "i": 9
   },
   {
    "id": "v190-c3-311-11",
    "title": "Approval Processing Time",
    "type": "funnel",
    "description": "Tracks how long agent approvals take once submitted for review.",
    "i": 10
   },
   {
    "id": "v190-c3-311-13",
    "title": "Referee Evidence",
    "type": "radar",
    "description": "Compares how complete referee evidence is across candidate agents.",
    "i": 12
   },
   {
    "id": "v190-c3-311-14",
    "title": "Company Evidence",
    "type": "matrix",
    "description": "Grids company evidence completeness against each candidate agent.",
    "i": 13
   },
   {
    "id": "v190-c3-311-16",
    "title": "Selection Rating Profile",
    "type": "trend",
    "description": "Shows how selection ratings are distributed across candidate agents.",
    "i": 15
   },
   {
    "id": "v190-c3-311-17",
    "title": "Risk Assessment Coverage",
    "type": "bar",
    "description": "Compares how many candidate agents have a completed risk assessment.",
    "i": 16
   },
   {
    "id": "v190-c3-311-18",
    "title": "Risk Mitigation Coverage",
    "type": "donut",
    "description": "Shows what share of identified agent risks have a mitigation plan.",
    "i": 17
   },
   {
    "id": "v190-c3-311-19",
    "title": "First-Time Contract Status",
    "type": "funnel",
    "description": "Tracks first-time agent contracts from drafted through to signed.",
    "i": 18
   },
   {
    "id": "v190-c3-311-21",
    "title": "NDA Requirement Distribution",
    "type": "radar",
    "description": "Shows how NDA requirements are distributed across agent types.",
    "i": 20
   },
   {
    "id": "v190-c3-311-23",
    "title": "Onboarding Initiation",
    "type": "gauge",
    "description": "Gauges how many newly appointed agents have started onboarding.",
    "i": 22
   },
   {
    "id": "v190-c3-311-24",
    "title": "Onboarding Activity Completion",
    "type": "trend",
    "description": "Tracks how much of the onboarding activity checklist has been completed.",
    "i": 23
   },
   {
    "id": "v190-c3-311-25",
    "title": "Agent Territory Readiness",
    "type": "bar",
    "description": "Compares how ready agent territory assignments are across candidates.",
    "i": 24
   },
   {
    "id": "v190-c3-311-26",
    "title": "Appointment Exception Profile",
    "type": "donut",
    "description": "Shows the share of appointments with an outstanding exception.",
    "i": 25
   },
   {
    "id": "v190-c3-311-29",
    "title": "Appointment Trend",
    "type": "radar",
    "description": "Compares agent appointment activity across recent reporting periods.",
    "i": 28
   },
   {
    "id": "v190-c3-311-30",
    "title": "Approval Outcome Trend",
    "type": "matrix",
    "description": "Grids approval outcomes by month to show trends over time.",
    "i": 29
   }
  ],
  "3.2.1": [
   {
    "id": "v190-c3-321-05",
    "title": "Renewal Checkpoint Flow",
    "type": "radar",
    "description": "Follows agents through each stage of their renewal checkpoint process.",
    "i": 4
   },
   {
    "id": "v190-c3-321-07",
    "title": "Offboarding and Exit Security",
    "type": "gauge",
    "description": "Gauges how securely agent offboarding and exit is being managed.",
    "i": 6
   },
   {
    "id": "v190-c3-321-08",
    "title": "Active Agent Portfolio",
    "type": "trend",
    "description": "Tracks how the active agent portfolio has changed over recent periods.",
    "i": 7
   },
   {
    "id": "v190-c3-321-09",
    "title": "Annual Review Coverage",
    "type": "bar",
    "description": "Compares how many agents have completed their annual review.",
    "i": 8
   },
   {
    "id": "v190-c3-321-10",
    "title": "Annual Survey Profile",
    "type": "donut",
    "description": "Shows the results profile of annual agent surveys.",
    "i": 9
   },
   {
    "id": "v190-c3-321-11",
    "title": "Recruitment Target Profile",
    "type": "funnel",
    "description": "Tracks agent recruitment activity against their assigned target.",
    "i": 10
   },
   {
    "id": "v190-c3-321-12",
    "title": "Target versus Actual Recruitment",
    "type": "lifecycle",
    "description": "Compares planned recruitment targets against actual results by agent.",
    "i": 11
   },
   {
    "id": "v190-c3-321-13",
    "title": "Applicant Contribution by Agent",
    "type": "radar",
    "description": "Compares how much each agent has contributed to total applicants.",
    "i": 12
   },
   {
    "id": "v190-c3-321-14",
    "title": "Applicant Conversion by Agent",
    "type": "matrix",
    "description": "Grids applicant conversion rates against each individual agent.",
    "i": 13
   },
   {
    "id": "v190-c3-321-16",
    "title": "Contract Expiry Ageing",
    "type": "trend",
    "description": "Tracks how close agent contracts are to their expiry date.",
    "i": 15
   },
   {
    "id": "v190-c3-321-18",
    "title": "Continuation and Hold Outcomes",
    "type": "donut",
    "description": "Shows the split between agents continued, put on hold, or ended.",
    "i": 17
   },
   {
    "id": "v190-c3-321-19",
    "title": "Claim Submission Activity",
    "type": "funnel",
    "description": "Tracks claims submitted against agents across recent reporting periods.",
    "i": 18
   },
   {
    "id": "v190-c3-321-20",
    "title": "Claim Amount Profile",
    "type": "lifecycle",
    "description": "Follows claim amounts against agents from filed through to resolved.",
    "i": 19
   },
   {
    "id": "v190-c3-321-21",
    "title": "Training Log Coverage",
    "type": "radar",
    "description": "Compares how much training log evidence exists for each agent.",
    "i": 20
   },
   {
    "id": "v190-c3-321-23",
    "title": "Student Feedback Coverage",
    "type": "gauge",
    "description": "Gauges how much student feedback has been captured for agents.",
    "i": 22
   },
   {
    "id": "v190-c3-321-24",
    "title": "Consent Survey Completion",
    "type": "trend",
    "description": "Tracks consent surveys from sent through to completed by students.",
    "i": 23
   },
   {
    "id": "v190-c3-321-25",
    "title": "Suspension and Termination",
    "type": "bar",
    "description": "Compares suspension and termination activity across agents.",
    "i": 24
   },
   {
    "id": "v190-c3-321-29",
    "title": "Performance Trend",
    "type": "radar",
    "description": "Compares agent performance trends across recent reporting periods.",
    "i": 28
   },
   {
    "id": "v190-c3-321-30",
    "title": "Renewal Outcome Trend",
    "type": "matrix",
    "description": "Grids renewal outcomes by month to show trends over time.",
    "i": 29
   }
  ]
 },
 "criterion_6": {
  "overview": [
   {
    "id": "v190-c6-overview-01",
    "title": "Quality Management Cycle",
    "type": "bar",
    "description": "Maps the stages a quality issue passes through the management cycle.",
    "i": 0
   },
   {
    "id": "v190-c6-overview-03",
    "title": "Quality System Health",
    "type": "funnel",
    "description": "Tracks quality system issues from raised through to fully resolved.",
    "i": 2
   },
   {
    "id": "v190-c6-overview-05",
    "title": "Action Status",
    "type": "radar",
    "description": "Compares the status of quality actions across audits, review and innovation.",
    "i": 4
   },
   {
    "id": "v190-c6-overview-07",
    "title": "Audit Portfolio Status",
    "type": "gauge",
    "description": "Gauges how the current audit portfolio is distributed by status.",
    "i": 6
   },
   {
    "id": "v190-c6-overview-08",
    "title": "Management Review Portfolio",
    "type": "trend",
    "description": "Tracks the management review portfolio across recent reporting periods.",
    "i": 7
   },
   {
    "id": "v190-c6-overview-09",
    "title": "Innovation Portfolio",
    "type": "bar",
    "description": "Compares how many innovation initiatives are in progress across categories.",
    "i": 8
   },
   {
    "id": "v190-c6-overview-10",
    "title": "Provider Evaluation Portfolio",
    "type": "donut",
    "description": "Shows the current status mix of provider evaluations, from due to complete.",
    "i": 9
   },
   {
    "id": "v190-c6-overview-11",
    "title": "Risk Portfolio",
    "type": "funnel",
    "description": "Tracks risk records from identified through to fully treated.",
    "i": 10
   },
   {
    "id": "v190-c6-overview-12",
    "title": "Corrective Action Portfolio",
    "type": "lifecycle",
    "description": "Follows corrective actions from raised through to verified closure.",
    "i": 11
   },
   {
    "id": "v190-c6-overview-13",
    "title": "Quality Exception Profile",
    "type": "radar",
    "description": "Highlights where quality exceptions are concentrated across this criterion.",
    "i": 12
   },
   {
    "id": "v190-c6-overview-15",
    "title": "Quality Trend",
    "type": "gauge",
    "description": "Gauges how quality performance has trended across recent periods.",
    "i": 14
   }
  ],
  "6.1.1": [
   {
    "id": "v190-c6-611-03",
    "title": "Audit Lifecycle",
    "type": "funnel",
    "description": "Maps an audit from planned through fieldwork to its closed report.",
    "i": 2
   },
   {
    "id": "v190-c6-611-04",
    "title": "Auditor Qualification and Independence",
    "type": "lifecycle",
    "description": "Follows auditor qualification and independence checks from unverified through to confirmed.",
    "i": 3
   },
   {
    "id": "v190-c6-611-07",
    "title": "Audit Plan Completion",
    "type": "gauge",
    "description": "Gauges how much of the approved audit plan has been completed.",
    "i": 6
   },
   {
    "id": "v190-c6-611-08",
    "title": "Audit Schedule Status",
    "type": "trend",
    "description": "Tracks audits against their scheduled status across the year.",
    "i": 7
   },
   {
    "id": "v190-c6-611-09",
    "title": "Audit Evidence Completeness",
    "type": "bar",
    "description": "Compares how complete audit evidence is across recent audits.",
    "i": 8
   },
   {
    "id": "v190-c6-611-10",
    "title": "Finding Type Distribution",
    "type": "donut",
    "description": "Shows how audit findings are distributed across each finding type.",
    "i": 9
   },
   {
    "id": "v190-c6-611-11",
    "title": "Finding Owner Distribution",
    "type": "funnel",
    "description": "Shows how audit findings are distributed across their assigned owners.",
    "i": 10
   },
   {
    "id": "v190-c6-611-12",
    "title": "Finding Ageing",
    "type": "lifecycle",
    "description": "Tracks how long open audit findings have been waiting for closure.",
    "i": 11
   },
   {
    "id": "v190-c6-611-13",
    "title": "Resolution Status",
    "type": "radar",
    "description": "Compares the resolution status of audit findings across recent audits.",
    "i": 12
   },
   {
    "id": "v190-c6-611-14",
    "title": "Overdue Resolution Profile",
    "type": "matrix",
    "description": "Grids overdue findings against each area they were raised against.",
    "i": 13
   },
   {
    "id": "v190-c6-611-15",
    "title": "Closure Verification",
    "type": "gauge",
    "description": "Gauges what share of closed findings have completed verification.",
    "i": 14
   }
  ],
  "6.2.1": [
   {
    "id": "v190-c6-621-02",
    "title": "Management Review Preparation",
    "type": "donut",
    "description": "Tracks management review meetings from scheduled through to prepared.",
    "i": 1
   },
   {
    "id": "v190-c6-621-05",
    "title": "Action Ageing",
    "type": "radar",
    "description": "Compares how long open management review actions have been outstanding.",
    "i": 4
   },
   {
    "id": "v190-c6-621-06",
    "title": "Action Effectiveness",
    "type": "matrix",
    "description": "Shows what share of management review actions were assessed as effective once closed.",
    "i": 5
   },
   {
    "id": "v190-c6-621-08",
    "title": "Review Cadence",
    "type": "trend",
    "description": "Tracks how management review meetings are distributed across their scheduled cadence.",
    "i": 7
   },
   {
    "id": "v190-c6-621-09",
    "title": "Chairperson Coverage",
    "type": "bar",
    "description": "Compares chairperson coverage across scheduled management review meetings.",
    "i": 8
   },
   {
    "id": "v190-c6-621-10",
    "title": "Minutes Completion",
    "type": "donut",
    "description": "Gauges what share of management review meetings have completed minutes.",
    "i": 9
   },
   {
    "id": "v190-c6-621-11",
    "title": "Next Review Readiness",
    "type": "funnel",
    "description": "Gauges how ready the next scheduled management review is.",
    "i": 10
   },
   {
    "id": "v190-c6-621-12",
    "title": "Audit Input Coverage",
    "type": "lifecycle",
    "description": "Compares how much audit-related input has fed into management review.",
    "i": 11
   },
   {
    "id": "v190-c6-621-13",
    "title": "Provider Input Coverage",
    "type": "radar",
    "description": "Compares how much provider-related input has fed into management review.",
    "i": 12
   },
   {
    "id": "v190-c6-621-14",
    "title": "Risk Input Coverage",
    "type": "matrix",
    "description": "Grids how much risk-related input has fed into management review.",
    "i": 13
   },
   {
    "id": "v190-c6-621-15",
    "title": "Quality Action Follow-up",
    "type": "gauge",
    "description": "Gauges how many quality actions from management review still need follow-up.",
    "i": 14
   }
  ],
  "6.3.1": [
   {
    "id": "v190-c6-631-03",
    "title": "Innovation Performance Categories",
    "type": "funnel",
    "description": "Compares innovation performance across the categories being tracked.",
    "i": 2
   },
   {
    "id": "v190-c6-631-04",
    "title": "QIPI Outcome Trend",
    "type": "lifecycle",
    "description": "Tracks QIPI outcomes across recent reporting periods.",
    "i": 3
   },
   {
    "id": "v190-c6-631-05",
    "title": "Before and After Impact",
    "type": "radar",
    "description": "Compares before-and-after impact for completed improvement initiatives.",
    "i": 4
   },
   {
    "id": "v190-c6-631-07",
    "title": "Innovation Category Mix",
    "type": "gauge",
    "description": "Gauges how innovation activity is distributed across each category.",
    "i": 6
   },
   {
    "id": "v190-c6-631-09",
    "title": "TACEI Profile",
    "type": "bar",
    "description": "Compares TACEI scores across recent innovation initiatives.",
    "i": 8
   },
   {
    "id": "v190-c6-631-10",
    "title": "CEI Profile",
    "type": "donut",
    "description": "Shows the CEI profile across recent innovation initiatives.",
    "i": 9
   },
   {
    "id": "v190-c6-631-11",
    "title": "People Saving",
    "type": "funnel",
    "description": "Tracks people-related savings achieved from innovation initiatives.",
    "i": 10
   },
   {
    "id": "v190-c6-631-12",
    "title": "Technology Saving",
    "type": "lifecycle",
    "description": "Follows technology-related savings from identified through to realised.",
    "i": 11
   },
   {
    "id": "v190-c6-631-13",
    "title": "Physical Saving",
    "type": "radar",
    "description": "Compares physical or facility-related savings across initiatives.",
    "i": 12
   },
   {
    "id": "v190-c6-631-14",
    "title": "Gross and Net Saving",
    "type": "matrix",
    "description": "Grids gross and net savings against each innovation initiative.",
    "i": 13
   },
   {
    "id": "v190-c6-631-15",
    "title": "Benchmark Variance",
    "type": "gauge",
    "description": "Gauges how actual innovation savings compare against the set benchmark.",
    "i": 14
   }
  ],
  "6.4.1": [
   {
    "id": "v190-c6-641-03",
    "title": "Compliance Package",
    "type": "funnel",
    "description": "Gauges how complete each provider's compliance documentation package is.",
    "i": 2
   },
   {
    "id": "v190-c6-641-04",
    "title": "Service Delivery and Purchase Controls",
    "type": "lifecycle",
    "description": "Follows service delivery and purchase controls from unverified through to confirmed.",
    "i": 3
   },
   {
    "id": "v190-c6-641-05",
    "title": "Provider Rating Weighting",
    "type": "radar",
    "description": "Grids the weighting applied to each provider rating criterion.",
    "i": 4
   },
   {
    "id": "v190-c6-641-07",
    "title": "Provider Portfolio Status",
    "type": "gauge",
    "description": "Gauges how the current provider portfolio is distributed by status.",
    "i": 6
   },
   {
    "id": "v190-c6-641-08",
    "title": "Identification and Screening",
    "type": "trend",
    "description": "Tracks providers through identification and initial screening stages.",
    "i": 7
   },
   {
    "id": "v190-c6-641-09",
    "title": "Regular Review Coverage",
    "type": "bar",
    "description": "Compares how many providers have completed a regular scheduled review.",
    "i": 8
   },
   {
    "id": "v190-c6-641-10",
    "title": "Exit Evaluation Coverage",
    "type": "donut",
    "description": "Shows what share of exiting providers completed a formal exit evaluation.",
    "i": 9
   },
   {
    "id": "v190-c6-641-12",
    "title": "Rating Likert Profile",
    "type": "lifecycle",
    "description": "Shows how provider ratings are distributed across the Likert scale used.",
    "i": 11
   },
   {
    "id": "v190-c6-641-13",
    "title": "Continuation Outcomes",
    "type": "radar",
    "description": "Shows what share of provider evaluations resulted in continuation.",
    "i": 12
   },
   {
    "id": "v190-c6-641-14",
    "title": "Hold Outcomes",
    "type": "matrix",
    "description": "Shows what share of provider evaluations resulted in a hold status.",
    "i": 13
   },
   {
    "id": "v190-c6-641-15",
    "title": "Termination Outcomes",
    "type": "gauge",
    "description": "Shows what share of provider evaluations resulted in termination.",
    "i": 14
   }
  ],
  "6.5.3": [
   {
    "id": "v190-c6-653-04",
    "title": "Risk Treatment Lifecycle",
    "type": "lifecycle",
    "description": "Follows a risk from identified through treatment to closure.",
    "i": 3
   },
   {
    "id": "v190-c6-653-05",
    "title": "Residual Risk Trend",
    "type": "radar",
    "description": "Compares residual risk levels across recent reporting periods.",
    "i": 4
   },
   {
    "id": "v190-c6-653-06",
    "title": "Business Continuity Readiness",
    "type": "matrix",
    "description": "Gauges how ready business continuity plans are against expectations.",
    "i": 5
   },
   {
    "id": "v190-c6-653-08",
    "title": "Mitigation Plan Coverage",
    "type": "trend",
    "description": "Gauges what share of identified risks have a mitigation plan in place.",
    "i": 7
   },
   {
    "id": "v190-c6-653-09",
    "title": "Risk Owner Coverage",
    "type": "bar",
    "description": "Compares risk ownership coverage across identified risks.",
    "i": 8
   },
   {
    "id": "v190-c6-653-10",
    "title": "Risk Due-Date Readiness",
    "type": "donut",
    "description": "Gauges how many risk treatment actions are on track for their due date.",
    "i": 9
   },
   {
    "id": "v190-c6-653-11",
    "title": "High-Priority Risk Profile",
    "type": "funnel",
    "description": "Grids high-priority risks against the area they were identified in.",
    "i": 10
   },
   {
    "id": "v190-c6-653-12",
    "title": "Initial Risk Profile",
    "type": "lifecycle",
    "description": "Compares initial risk ratings before any treatment was applied.",
    "i": 11
   },
   {
    "id": "v190-c6-653-13",
    "title": "Residual Risk Profile",
    "type": "radar",
    "description": "Compares residual risk ratings after treatment has been applied.",
    "i": 12
   },
   {
    "id": "v190-c6-653-14",
    "title": "Control Effectiveness",
    "type": "matrix",
    "description": "Grids control effectiveness against each identified risk.",
    "i": 13
   },
   {
    "id": "v190-c6-653-15",
    "title": "Risk Exception Profile",
    "type": "gauge",
    "description": "Highlights where risk assessment exceptions are concentrated.",
    "i": 14
   }
  ]
 },
 "criterion_7": {
  "overview": [
   {
    "id": "v190-c7-overview-01",
    "title": "Outcome Portfolio",
    "type": "bar",
    "description": "Compares the portfolio of tracked outcomes across all measured areas.",
    "i": 0
   },
   {
    "id": "v190-c7-overview-03",
    "title": "Outcome System Health",
    "type": "funnel",
    "description": "Tracks outcome measurement issues from raised through to fully resolved.",
    "i": 2
   },
   {
    "id": "v190-c7-overview-04",
    "title": "Outcome Measurement Lifecycle",
    "type": "lifecycle",
    "description": "Maps an outcome from target set through to measured and reviewed.",
    "i": 3
   },
   {
    "id": "v190-c7-overview-05",
    "title": "Outcome Exception Funnel",
    "type": "radar",
    "description": "Highlights where outcome exceptions are concentrated across measured areas.",
    "i": 4
   },
   {
    "id": "v190-c7-overview-07",
    "title": "Indicator Portfolio",
    "type": "gauge",
    "description": "Gauges how the current indicator portfolio is distributed by status.",
    "i": 6
   },
   {
    "id": "v190-c7-overview-12",
    "title": "Outcome Category Mix",
    "type": "lifecycle",
    "description": "Follows outcomes from raw category through to fully classified.",
    "i": 11
   },
   {
    "id": "v190-c7-overview-13",
    "title": "Outcome Ownership",
    "type": "radar",
    "description": "Compares how outcome ownership is distributed across responsible owners.",
    "i": 12
   },
   {
    "id": "v190-c7-overview-15",
    "title": "Improvement Action Linkage",
    "type": "gauge",
    "description": "Gauges how many outcomes have a linked improvement action.",
    "i": 14
   },
   {
    "id": "v190-c7-overview-16",
    "title": "Outcome Trend",
    "type": "trend",
    "description": "Tracks overall outcome performance across recent reporting periods.",
    "i": 15
   },
   {
    "id": "v190-c7-overview-17",
    "title": "Benchmark Profile",
    "type": "bar",
    "description": "Compares outcome results against their set benchmark values.",
    "i": 16
   },
   {
    "id": "v190-c7-overview-18",
    "title": "Student Outcome Profile",
    "type": "donut",
    "description": "Shows the profile of outcomes specifically tied to students.",
    "i": 17
   },
   {
    "id": "v190-c7-overview-19",
    "title": "Graduate Outcome Profile",
    "type": "funnel",
    "description": "Tracks graduate outcomes from measured through to reported.",
    "i": 18
   },
   {
    "id": "v190-c7-overview-20",
    "title": "Stakeholder Outcome Profile",
    "type": "lifecycle",
    "description": "Compares outcomes across the different stakeholder groups measured.",
    "i": 19
   },
   {
    "id": "v190-c7-overview-21",
    "title": "Financial Outcome Profile",
    "type": "radar",
    "description": "Compares financial outcome results across the areas measured.",
    "i": 20
   },
   {
    "id": "v190-c7-overview-22",
    "title": "Operational Outcome Profile",
    "type": "matrix",
    "description": "Grids operational outcome results against each measured area.",
    "i": 21
   },
   {
    "id": "v190-c7-overview-23",
    "title": "People Saving Profile",
    "type": "gauge",
    "description": "Gauges how much people-related saving has been achieved.",
    "i": 22
   },
   {
    "id": "v190-c7-overview-24",
    "title": "Technology Saving Profile",
    "type": "trend",
    "description": "Tracks technology-related savings across recent reporting periods.",
    "i": 23
   },
   {
    "id": "v190-c7-overview-25",
    "title": "Physical Saving Profile",
    "type": "bar",
    "description": "Compares physical or facility-related savings across measured areas.",
    "i": 24
   },
   {
    "id": "v190-c7-overview-26",
    "title": "Gross Saving Profile",
    "type": "donut",
    "description": "Shows the profile of gross savings before adjustments.",
    "i": 25
   },
   {
    "id": "v190-c7-overview-27",
    "title": "Net Saving Profile",
    "type": "funnel",
    "description": "Tracks net savings from identified through to realised.",
    "i": 26
   },
   {
    "id": "v190-c7-overview-30",
    "title": "Outcome Maturity",
    "type": "matrix",
    "description": "Grids outcome measurement maturity against each measured area.",
    "i": 29
   },
   {
    "id": "v190-c7-overview-31",
    "title": "Department Performance",
    "type": "gauge",
    "description": "Gauges how each department is performing against its outcome targets.",
    "i": 30
   },
   {
    "id": "v190-c7-overview-32",
    "title": "Strategic Alignment",
    "type": "trend",
    "description": "Tracks how well outcomes are aligned to strategic objectives over time.",
    "i": 31
   },
   {
    "id": "v190-c7-overview-33",
    "title": "Outcome Risk Profile",
    "type": "bar",
    "description": "Compares outcome risk levels across the areas being measured.",
    "i": 32
   },
   {
    "id": "v190-c7-overview-36",
    "title": "Outcome Metric Readiness",
    "type": "lifecycle",
    "description": "Follows outcome metrics from unavailable through to fully calculated and ready.",
    "i": 35
   },
   {
    "id": "v190-c7-overview-37",
    "title": "Annual Outcome Trend",
    "type": "radar",
    "description": "Compares outcome performance across recent years on several dimensions at once.",
    "i": 36
   },
   {
    "id": "v190-c7-overview-38",
    "title": "Quarterly Outcome Trend",
    "type": "matrix",
    "description": "Grids outcome performance by quarter against each measured dimension.",
    "i": 37
   },
   {
    "id": "v190-c7-overview-39",
    "title": "Outcome Benchmark Trend",
    "type": "gauge",
    "description": "Gauges how outcome results have trended against their benchmark over time.",
    "i": 38
   }
  ],
  "7.1.1": [
   {
    "id": "v190-c7-711-07",
    "title": "Measurement Lifecycle",
    "type": "gauge",
    "description": "Maps an indicator from defined through measured to reviewed.",
    "i": 6
   },
   {
    "id": "v190-c7-711-10",
    "title": "Outcome Category Distribution",
    "type": "donut",
    "description": "Shows how outcomes are distributed across each measured category.",
    "i": 9
   },
   {
    "id": "v190-c7-711-11",
    "title": "Indicator Status Funnel",
    "type": "funnel",
    "description": "Tracks indicators from defined through to a confirmed status.",
    "i": 10
   },
   {
    "id": "v190-c7-711-13",
    "title": "Measurement Evidence Matrix",
    "type": "radar",
    "description": "Compares how complete the supporting measurement evidence is across indicators.",
    "i": 12
   },
   {
    "id": "v190-c7-711-18",
    "title": "Outcome-to-Strategy Mapping",
    "type": "donut",
    "description": "Maps outcomes to the strategic objectives they support.",
    "i": 17
   },
   {
    "id": "v190-c7-711-19",
    "title": "Student Outcome Trend",
    "type": "funnel",
    "description": "Tracks student outcome results across recent reporting periods.",
    "i": 18
   },
   {
    "id": "v190-c7-711-20",
    "title": "Graduate Outcome Trend",
    "type": "lifecycle",
    "description": "Follows graduate outcome results from measured through to reported.",
    "i": 19
   },
   {
    "id": "v190-c7-711-21",
    "title": "Stakeholder Outcome Trend",
    "type": "radar",
    "description": "Compares stakeholder outcome results across recent reporting periods.",
    "i": 20
   },
   {
    "id": "v190-c7-711-22",
    "title": "Financial Outcome Trend",
    "type": "matrix",
    "description": "Grids financial outcome results by trend against each measured area.",
    "i": 21
   },
   {
    "id": "v190-c7-711-23",
    "title": "Operational Outcome Trend",
    "type": "gauge",
    "description": "Gauges how operational outcomes have trended across recent periods.",
    "i": 22
   },
   {
    "id": "v190-c7-711-24",
    "title": "Savings Outcome Trend",
    "type": "trend",
    "description": "Tracks savings-related outcome results across recent reporting periods.",
    "i": 23
   },
   {
    "id": "v190-c7-711-25",
    "title": "Department Outcome Profile",
    "type": "bar",
    "description": "Compares outcome performance across each contributing department.",
    "i": 24
   },
   {
    "id": "v190-c7-711-26",
    "title": "Outcome Ownership Radar",
    "type": "donut",
    "description": "Compares outcome ownership coverage across several dimensions at once.",
    "i": 25
   },
   {
    "id": "v190-c7-711-27",
    "title": "Target Achievement Radar",
    "type": "funnel",
    "description": "Tracks target achievement from set through to confirmed achieved.",
    "i": 26
   },
   {
    "id": "v190-c7-711-28",
    "title": "Outcome Maturity Matrix",
    "type": "lifecycle",
    "description": "Grids outcome maturity against each measured dimension.",
    "i": 27
   },
   {
    "id": "v190-c7-711-29",
    "title": "Indicator Exception Profile",
    "type": "radar",
    "description": "Compares where indicator exceptions are concentrated across outcome areas.",
    "i": 28
   },
   {
    "id": "v190-c7-711-30",
    "title": "Outcome Risk Matrix",
    "type": "matrix",
    "description": "Grids outcome risk levels against each measured area.",
    "i": 29
   },
   {
    "id": "v190-c7-711-33",
    "title": "Annual Performance Trend",
    "type": "bar",
    "description": "Compares annual performance results across recent reporting years.",
    "i": 32
   },
   {
    "id": "v190-c7-711-34",
    "title": "Quarterly Performance Trend",
    "type": "donut",
    "description": "Shows how quarterly performance results have shifted across the year.",
    "i": 33
   },
   {
    "id": "v190-c7-711-35",
    "title": "Benchmark Comparison",
    "type": "funnel",
    "description": "Tracks outcome results against their set benchmark comparison.",
    "i": 34
   },
   {
    "id": "v190-c7-711-39",
    "title": "Outcome Reporting Readiness",
    "type": "gauge",
    "description": "Gauges how ready outcome data currently is for formal reporting.",
    "i": 38
   },
   {
    "id": "v190-c7-711-40",
    "title": "Measurement Governance",
    "type": "trend",
    "description": "Compares how well measurement governance is being applied across indicators.",
    "i": 39
   }
  ]
 }
};

const C4_ARCHIVED = {
 "c411": [
  {
   "id": "v190-c4-c411-04",
   "title": "Applicant Processing Time",
   "type": "lifecycle",
   "description": "Tracks how long applicants take to move through the admission process.",
   "i": 3
  },
  {
   "id": "v190-c4-c411-05",
   "title": "Selection Decision Profile",
   "type": "radar",
   "description": "Compares selection decisions across the different outcomes reached.",
   "i": 4
  },
  {
   "id": "v190-c4-c411-06",
   "title": "Late Admission Exceptions",
   "type": "matrix",
   "description": "Highlights admissions processed later than the expected timeframe.",
   "i": 5
  },
  {
   "id": "v190-c4-c411-08",
   "title": "Admission Evidence Matrix",
   "type": "trend",
   "description": "Grids admission evidence completeness against each stage of the process.",
   "i": 7
  },
  {
   "id": "v190-c4-c411-09",
   "title": "Applicant Trend",
   "type": "bar",
   "description": "Tracks applicant volume across recent reporting periods.",
   "i": 8
  },
  {
   "id": "v190-c4-c411-11",
   "title": "Admission Metric Readiness",
   "type": "funnel",
   "description": "Follows admission metrics from unavailable through to fully calculated and ready.",
   "i": 10
  },
  {
   "id": "v190-c4-c411-12",
   "title": "Admission Exception Profile",
   "type": "lifecycle",
   "description": "Shows the share of admissions with an outstanding exception.",
   "i": 11
  }
 ],
 "c421": [
  {
   "id": "v190-c4-c421-03",
   "title": "Contract Approval Status",
   "type": "funnel",
   "description": "Compares how student contracts are distributed across approval status.",
   "i": 2
  },
  {
   "id": "v190-c4-c421-04",
   "title": "Unsigned Contract Ageing",
   "type": "lifecycle",
   "description": "Tracks how long unsigned student contracts have been outstanding.",
   "i": 3
  },
  {
   "id": "v190-c4-c421-06",
   "title": "Contract Exception Funnel",
   "type": "matrix",
   "description": "Highlights where contract exceptions are concentrated across students.",
   "i": 5
  },
  {
   "id": "v190-c4-c421-07",
   "title": "Contract Date Readiness",
   "type": "gauge",
   "description": "Gauges what share of student contracts have key dates recorded.",
   "i": 6
  },
  {
   "id": "v190-c4-c421-08",
   "title": "Student Contract Status",
   "type": "trend",
   "description": "Shows the current status mix of student contracts across the cohort.",
   "i": 7
  },
  {
   "id": "v190-c4-c421-09",
   "title": "Contract Trend",
   "type": "bar",
   "description": "Tracks student contract activity across recent reporting periods.",
   "i": 8
  },
  {
   "id": "v190-c4-c421-11",
   "title": "Contract Metric Readiness",
   "type": "funnel",
   "description": "Follows contract metrics from unavailable through to fully calculated and ready.",
   "i": 10
  },
  {
   "id": "v190-c4-c421-12",
   "title": "Contract Control Matrix",
   "type": "lifecycle",
   "description": "Grids contract control status against each responsible area.",
   "i": 11
  }
 ],
 "c422": [
  {
   "id": "v190-c4-c422-04",
   "title": "Outstanding Balance Profile",
   "type": "lifecycle",
   "description": "Tracks the profile of outstanding balances still owed by students.",
   "i": 3
  },
  {
   "id": "v190-c4-c422-05",
   "title": "Payment Lifecycle",
   "type": "radar",
   "description": "Maps a payment from invoiced through to fully collected.",
   "i": 4
  },
  {
   "id": "v190-c4-c422-06",
   "title": "Fee Exception Funnel",
   "type": "matrix",
   "description": "Highlights where fee-related exceptions are concentrated.",
   "i": 5
  },
  {
   "id": "v190-c4-c422-08",
   "title": "Collection Trend",
   "type": "trend",
   "description": "Tracks fee collection trends across recent reporting periods.",
   "i": 7
  },
  {
   "id": "v190-c4-c422-09",
   "title": "Payment Evidence Matrix",
   "type": "bar",
   "description": "Grids payment evidence completeness against each fee record.",
   "i": 8
  },
  {
   "id": "v190-c4-c422-11",
   "title": "Fee Metric Readiness",
   "type": "funnel",
   "description": "Follows fee metrics from unavailable through to fully calculated and ready.",
   "i": 10
  },
  {
   "id": "v190-c4-c422-12",
   "title": "Fee Control Health",
   "type": "lifecycle",
   "description": "Gauges the overall health of fee and FPS controls in place.",
   "i": 11
  }
 ],
 "c431": [
  {
   "id": "v190-c4-c431-03",
   "title": "Deferment Request Status",
   "type": "funnel",
   "description": "Compares deferment requests across the different status stages.",
   "i": 2
  },
  {
   "id": "v190-c4-c431-04",
   "title": "Withdrawal Request Status",
   "type": "lifecycle",
   "description": "Shows the current status mix of withdrawal requests.",
   "i": 3
  },
  {
   "id": "v190-c4-c431-05",
   "title": "Request Processing Time",
   "type": "radar",
   "description": "Tracks how long movement requests take to be processed.",
   "i": 4
  },
  {
   "id": "v190-c4-c431-06",
   "title": "Movement Exception Funnel",
   "type": "matrix",
   "description": "Highlights where exceptions are concentrated across movement requests.",
   "i": 5
  },
  {
   "id": "v190-c4-c431-08",
   "title": "Movement Evidence Matrix",
   "type": "trend",
   "description": "Grids movement request evidence against each stage of processing.",
   "i": 7
  },
  {
   "id": "v190-c4-c431-09",
   "title": "Movement Trend",
   "type": "bar",
   "description": "Tracks movement request volume across recent reporting periods.",
   "i": 8
  },
  {
   "id": "v190-c4-c431-11",
   "title": "Movement Metric Readiness",
   "type": "funnel",
   "description": "Follows movement metrics from unavailable through to fully calculated and ready.",
   "i": 10
  },
  {
   "id": "v190-c4-c431-12",
   "title": "Movement Control Health",
   "type": "lifecycle",
   "description": "Gauges the overall health of transfer, defer and withdraw controls.",
   "i": 11
  }
 ],
 "c441": [
  {
   "id": "v190-c4-c441-03",
   "title": "Refund Processing Time",
   "type": "funnel",
   "description": "Tracks how long refund requests take to be processed.",
   "i": 2
  },
  {
   "id": "v190-c4-c441-04",
   "title": "Refund Ageing",
   "type": "lifecycle",
   "description": "Tracks how long refund requests have been waiting for action.",
   "i": 3
  },
  {
   "id": "v190-c4-c441-06",
   "title": "Refund Exception Funnel",
   "type": "matrix",
   "description": "Highlights where exceptions are concentrated across refund requests.",
   "i": 5
  },
  {
   "id": "v190-c4-c441-07",
   "title": "Refund Amount Profile",
   "type": "gauge",
   "description": "Compares refund amounts across the requests processed.",
   "i": 6
  },
  {
   "id": "v190-c4-c441-08",
   "title": "Refund Evidence Matrix",
   "type": "trend",
   "description": "Grids refund evidence completeness against each request.",
   "i": 7
  },
  {
   "id": "v190-c4-c441-09",
   "title": "Refund Trend",
   "type": "bar",
   "description": "Tracks refund request volume across recent reporting periods.",
   "i": 8
  },
  {
   "id": "v190-c4-c441-11",
   "title": "Refund Metric Readiness",
   "type": "funnel",
   "description": "Follows refund metrics from unavailable through to fully calculated and ready.",
   "i": 10
  },
  {
   "id": "v190-c4-c441-12",
   "title": "Refund Control Health",
   "type": "lifecycle",
   "description": "Gauges the overall health of refund controls in place.",
   "i": 11
  }
 ],
 "c451": [
  {
   "id": "v190-c4-c451-03",
   "title": "Support Category Distribution",
   "type": "funnel",
   "description": "Compares support cases across the categories they were raised under.",
   "i": 2
  },
  {
   "id": "v190-c4-c451-04",
   "title": "Support Resolution Time",
   "type": "lifecycle",
   "description": "Tracks how long support cases take to reach resolution.",
   "i": 3
  },
  {
   "id": "v190-c4-c451-05",
   "title": "Support Lifecycle",
   "type": "radar",
   "description": "Maps a support case from raised through to closed.",
   "i": 4
  },
  {
   "id": "v190-c4-c451-06",
   "title": "Support Exception Funnel",
   "type": "matrix",
   "description": "Highlights where exceptions are concentrated across support cases.",
   "i": 5
  },
  {
   "id": "v190-c4-c451-08",
   "title": "Support Evidence Matrix",
   "type": "trend",
   "description": "Grids support case evidence against each stage of handling.",
   "i": 7
  },
  {
   "id": "v190-c4-c451-09",
   "title": "Support Trend",
   "type": "bar",
   "description": "Tracks student support case volume across recent reporting periods.",
   "i": 8
  },
  {
   "id": "v190-c4-c451-11",
   "title": "Support Metric Readiness",
   "type": "funnel",
   "description": "Follows support metrics from unavailable through to fully calculated and ready.",
   "i": 10
  },
  {
   "id": "v190-c4-c451-12",
   "title": "Support Control Health",
   "type": "lifecycle",
   "description": "Gauges the overall health of student support controls in place.",
   "i": 11
  }
 ],
 "c461": [
  {
   "id": "v190-c4-c461-02",
   "title": "Attendance Risk Profile",
   "type": "donut",
   "description": "Compares students by their current attendance risk level.",
   "i": 1
  },
  {
   "id": "v190-c4-c461-04",
   "title": "Conduct Case Status",
   "type": "lifecycle",
   "description": "Shows the current status mix of conduct cases across students.",
   "i": 3
  },
  {
   "id": "v190-c4-c461-05",
   "title": "Attendance Trend",
   "type": "radar",
   "description": "Tracks attendance trends across recent reporting periods.",
   "i": 4
  },
  {
   "id": "v190-c4-c461-06",
   "title": "Conduct Trend",
   "type": "matrix",
   "description": "Grids conduct case trends against each measured area.",
   "i": 5
  },
  {
   "id": "v190-c4-c461-08",
   "title": "Attendance Evidence Matrix",
   "type": "trend",
   "description": "Grids attendance evidence completeness against each student record.",
   "i": 7
  },
  {
   "id": "v190-c4-c461-09",
   "title": "Conduct Evidence Matrix",
   "type": "bar",
   "description": "Grids conduct case evidence completeness against each student record.",
   "i": 8
  },
  {
   "id": "v190-c4-c461-11",
   "title": "Attendance Metric Readiness",
   "type": "funnel",
   "description": "Follows attendance metrics from unavailable through to fully calculated and ready.",
   "i": 10
  },
  {
   "id": "v190-c4-c461-12",
   "title": "Conduct Exception Profile",
   "type": "lifecycle",
   "description": "Shows the share of conduct cases with an outstanding exception.",
   "i": 11
  }
 ]
};

const C5_ARCHIVED_DESCRIPTIONS = {
 "c511-network": "Maps how courses connect to the modules that make them up.",
 "c511-decision-time": "Tracks how long proposal decisions take across recent years.",
 "c511-proposal-bars": "Compares how complete supporting evidence is across course proposals.",
 "c511-module-bubbles": "Compares evidence strength across modules, sized by how much evidence exists.",
 "c511-module-radial": "Gauges what share of modules have complete design evidence.",
 "c511-module-stream": "Tracks module design evidence activity across recent periods.",
 "c511-review-timeline": "Tracks course reviews from scheduled through to completed over time.",
 "c511-review-actions": "Compares how complete supporting evidence is across course reviews.",
 "c511-gap-sunburst": "Grids evidence gaps against the record type each one was found in.",
 "c512-schedule": "Tracks upcoming course and module reviews against their scheduled dates.",
 "c512-review-type": "Compares how reviews are distributed across the different review types.",
 "c512-actions": "Shows the status mix of action plans raised from course reviews.",
 "c512-evidence": "Gauges how complete module review evidence is across the catalogue.",
 "c512-cycle-v110": "Tracks the review cycle from due through to fully completed.",
 "c512-coverage-v110": "Compares how much module review coverage feeds into course review.",
 "c512-action-aging-v110": "Tracks how long open review action plans have been outstanding.",
 "c512-actions-completion-v110": "Compares completed action plans against those still pending.",
 "c512-missing-evidence-v110": "Highlights reviews that are missing required supporting evidence.",
 "c512-followup-v110": "Tracks how implementation of review recommendations has trended over time.",
 "schedule": "Compares scheduled classes across each course offered.",
 "delivery-controls": "Gauges how many delivery controls are in place for scheduled classes.",
 "c521-flow": "Tracks a course through each stage of the planning process.",
 "c521-admission": "Shows the current status mix of admissions feeding into course planning.",
 "c521-session-readiness": "Gauges how ready room and timing arrangements are for scheduled sessions.",
 "c521-contracts": "Gauges what share of teaching contracts have complete date information.",
 "c521-date-completeness-v110": "Tracks how complete intake date records are across the catalogue.",
 "c521-unscheduled-v110": "Highlights module classes that still have no schedule assigned.",
 "c521-schedule-completeness-v110": "Gauges how complete class schedules are across the catalogue.",
 "c521-room-clashes-v110": "Highlights where room and time bookings clash with each other.",
 "c521-teacher-clashes-v110": "Highlights where a teacher's timetable has conflicting bookings.",
 "c521-contract-vs-start-v110": "Compares teaching contract dates against each course's commencement date.",
 "c521-contract-exceptions-v110": "Highlights teaching contracts that are unsigned or not yet sent.",
 "c522-platform": "Shows how delivery sessions are distributed across each platform used.",
 "c522-survey-categories": "Shows how survey responses are distributed across each category.",
 "c522-notice": "Gauges what share of observations were conducted with prior notice given.",
 "c522-concerns": "Compares delivery concerns raised across observation records.",
 "c522-planned-delivered-v110": "Compares planned delivery sessions against sessions actually delivered.",
 "c522-teacher-coverage-v110": "Compares observation coverage across each teacher delivering sessions.",
 "c522-module-coverage-v110": "Compares observation coverage across each module being delivered.",
 "c522-observation-mode-v110": "Shows the split between scheduled and ad-hoc delivery observations.",
 "c522-signoff-aging-v110": "Tracks how long delivery observations have waited for sign-off.",
 "c522-rating-distribution-v110": "Shows how delivery observation ratings are distributed overall.",
 "c522-strengths-v110": "Compares the most commonly noted strengths across delivery observations.",
 "c522-improvements-v110": "Compares the most commonly noted improvement areas across observations.",
 "c522-survey-volume-v110": "Tracks survey response volume for delivered sessions over time.",
 "c522-delivery-exceptions-v110": "Highlights delivery records with an outstanding exception to resolve.",
 "c531-type": "Compares partnerships across each type of agreement in place.",
 "c531-expiry": "Groups partnership agreements by how soon they are due to expire.",
 "c531-monitoring-type": "Shows how partnership monitoring activity is distributed by type.",
 "c531-scores": "Compares identification scores across candidate partnerships.",
 "c531-rating-stage": "Shows how partnerships are distributed across the provider rating stages.",
 "c531-threshold": "Gauges how many candidate partnerships met the selection threshold.",
 "c531-lifecycle-v110": "Maps a partnership agreement from proposed through to active.",
 "c531-signature-v110": "Gauges what share of partnership agreements have completed signature.",
 "c531-risk-v110": "Shows how partnership risk levels are distributed across the portfolio.",
 "c531-monitoring-recency-v110": "Tracks how recently each partnership was last monitored.",
 "c531-decisions-v110": "Shows the split of continuation decisions reached for partnerships.",
 "c531-missing-controls-v110": "Highlights partnerships missing required monitoring or evaluation records.",
 "c531-quality-completeness-v110": "Gauges how complete quality-related records are across partnerships.",
 "survey-question-score": "Compares survey scores across each individual question asked.",
 "learning-support": "Tracks learning support interventions raised for students.",
 "assessment-quality": "Gauges how complete and reliable the underlying assessment data is."
};

