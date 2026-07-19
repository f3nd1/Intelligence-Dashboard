# Raw Supplied Agent DocType

```text
DocType
Agent
Module:
Educ Sg
Editable Grid:
Grid Page Length:
0
Track Changes:
Naming Rule:
Expression (old style)
Auto Name:
UCC-AGT-.YY.####
Max Attachments:
0
Allow Import (via Data Import Tool):
Title Field:
agent_or_company_name
Show Title in Link Fields:
Search Fields:
agent_or_company_name
Default Sort Field:
modified
Default Sort Order:
DESC
Make "name" searchable in Global Search:
No	Role	If user is the owner	Select	Read	Write	Create	Delete	Report	Export	Share	Print	Email
1	
System Manager
2	
Admissions Manager
3	
Head of Department - Academic of Learning Innovation
4	
Head of Department - Sales Enablement and Strategy
5	
Short Course Viewer
6	
Guest
7	
Principal
8	
Special Agent
No	Link DocType	Link Fieldname	Group
1	
Student
custom_agent
Students
Database Engine:
InnoDB
None:
e9d305b273d14520c7a644f30c0a9439
No	Label	Type	Name	Mandatory	Options	Default	Fetch From	Hidden	Display Depends On (JS)	Collapsible	Hide Border	In List View	In List Filter	In Filter	Read Only	Allow Bulk Edit	Mandatory Depends On (JS)	Max Height	Description
1	
📝 Details
Tab Break
details_tab
2	
HTML
custom_html_render
3	
AGENT DETAILS
Section Break
agent_details_section
4	
HTML
html_jeft
Instructions
The Agent DocType is designed for managing recruitment agents, centralising key information related to their application, monitoring, and performance evaluations.

Tab Name	Description
📝 Details	Contains essential agent details, including their status, company information, and registration details with UCC.
📇 Contact Profiles	Stores contact information, including CEO or Manager details, contact officers, and a company profile overview.
💼 Experience	Outlines the agent's recruitment experience with Singapore institutions and other international schools, including student recruitment data.
🗂️ Recruitment	Details the agent's recruitment methods for UCC, including exhibitions, marketing strategies, and service fees related to student applications.
📎 Miscellaneous	Includes additional documents such as business registration, company profile, referee details, and a declaration for the agent's application.
👍 Approval	Tracks the approval process, including processed dates, approval by authorities, risk assessments, and any provider ratings assigned.
🔍 Monitor & Review	Monitors agent performance through scheduled reviews and evaluations, ensuring compliance with UCC's performance indicators.

Utilize this DocType to manage and monitor recruitment agents effectively, ensuring comprehensive oversight and alignment with UCC's operational standards.

5	
Column Break
column_break_zgks
6	
Status
Select
status

For Approval
For Internal Use
Active
Inactive
Suspended
Terminated
Under Review
Prospective
Pending Verification
7	
Applying Company?
Check
applying_as_company
Individual
Company
0
8	
Agent Name or Company
Data
agent_or_company_name
9	
Company Date of Registration
Date
date_of_registration
eval:doc.applying_as_company == 1
eval:doc.applying_as_company == 1
Refer to RA's Company date of registration
10	
Expiry Date
Date
expiry_date
11	
RA Application Form Date
Date
custom_ra_application_form_date
Refer to the actual date the application form was submitted.
12	
Registration No
Data
registration_no
eval:doc.applying_as_company == 1
eval:doc.applying_as_company == 1
13	
Place of Registration
Select
place_of_registration

Afghanistan
Åland Islands
Albania
Algeria
American Samoa
Andorra
Angola
Anguilla
Antarctica
Antigua and Barbuda
Argentina
Armenia
Aruba
Australia
Austria
Azerbaijan
Bahamas
Bahrain
Bangladesh
Barbados
Belarus
Belgium
Belize
Benin
Bermuda
Bhutan
Bolivia
Bosnia and Herzegovina
Botswana
Bouvet Island
Brazil
British Indian Ocean Territory
Brunei Darussalam
Bulgaria
Burkina Faso
Burundi
Cambodia
Cameroon
Canada
Cape Verde
Cayman Islands
Central African Republic
Chad
Chile
China
Christmas Island
Cocos (Keeling) Islands
Colombia
Comoros
Congo
Congo, The Democratic Republic of The
Cook Islands
Costa Rica
Cote D'ivoire
Croatia
Cuba
Cyprus
Czech Republic
Denmark
Djibouti
Dominica
Dominican Republic
Ecuador
Egypt
El Salvador
Equatorial Guinea
Eritrea
Estonia
Ethiopia
Falkland Islands (Malvinas)
Faroe Islands
Fiji
Finland
France
French Guiana
French Polynesia
French Southern Territories
Gabon
Gambia
Georgia
Germany
Ghana
Gibraltar
Greece
Greenland
Grenada
Guadeloupe
Guam
Guatemala
Guernsey
Guinea
Guinea-bissau
Guyana
Haiti
Heard Island and Mcdonald Islands
Holy See (Vatican City State)
Honduras
Hong Kong
Hungary
Iceland
India
Indonesia
Iran, Islamic Republic of
Iraq
Ireland
Isle of Man
Israel
Italy
Jamaica
Japan
Jersey
Jordan
Kazakhstan
Kenya
Kiribati
Korea, Democratic People's Republic of
Korea, Republic of
Kuwait
Kyrgyzstan
Lao People's Democratic Republic
Latvia
Lebanon
Lesotho
Liberia
Libyan Arab Jamahiriya
Liechtenstein
Lithuania
Luxembourg
Macao
Macedonia, The Former Yugoslav Republic of
Madagascar
Malawi
Malaysia
Maldives
Mali
Malta
Marshall Islands
Martinique
Mauritania
Mauritius
Mayotte
Mexico
Micronesia, Federated States of
Moldova, Republic of
Monaco
Mongolia
Montenegro
Montserrat
Morocco
Mozambique
Myanmar
Namibia
Nauru
Nepal
Netherlands
Netherlands Antilles
New Caledonia
New Zealand
Nicaragua
Niger
Nigeria
Niue
Norfolk Island
Northern Mariana Islands
Norway
Oman
Pakistan
Palau
Palestinian Territory, Occupied
Panama
Papua New Guinea
Paraguay
Peru
Philippines
Pitcairn
Poland
Portugal
Puerto Rico
Qatar
Reunion
Romania
Russian Federation
Rwanda
Saint Helena
Saint Kitts and Nevis
Saint Lucia
Saint Pierre and Miquelon
Saint Vincent and The Grenadines
Samoa
San Marino
Sao Tome and Principe
Saudi Arabia
Senegal
Serbia
Seychelles
Sierra Leone
Singapore
Slovakia
Slovenia
Solomon Islands
Somalia
South Africa
South Georgia and The South Sandwich Islands
Spain
Sri Lanka
Sudan
Suriname
Svalbard and Jan Mayen
Swaziland
Sweden
Switzerland
Syrian Arab Republic
Taiwan
Tajikistan
Tanzania, United Republic of
Thailand
Timor-leste
Togo
Tokelau
Tonga
Trinidad and Tobago
Tunisia
Turkey
Turkmenistan
Turks and Caicos Islands
Tuvalu
Uganda
Ukraine
United Arab Emirates
United Kingdom
United States
United States Minor Outlying Islands
Uruguay
Uzbekistan
Vanuatu
Venezuela
Viet Nam
Virgin Islands, British
Virgin Islands, U.S.
Wallis and Futuna
Western Sahara
Yemen
Zambia
Zimbabwe
eval:doc.applying_as_company == 1
eval:doc.applying_as_company == 1
14	
Countries of Recruitment
Data
countries_of_recruitment
15	
CONTACT DETAILS
Section Break
contact_details_section
16	
Telephone No
Data
telephone_no
17	
Full Address
Data
full_address
18	
Registered Address
Data
registered_address
19	
Column Break
column_break_ajti
20	
Email
Data
email
Email
21	
Fax No
Data
fax_no
22	
COMMISION TABLE
Section Break
ucc_registration_details_section
23	
Registration
Table
registration
Agent Registration Childtable
24	
📇 Contact Profiles
Tab Break
contact_and_profiles_tab
25	
Section Break
section_break_hsps
26	
Are the CEO/Manager or Contact Officer details different from the above?
Check
ceo_differ
0
eval:doc.applying_as_company == 1;
27	
NAME OF CHIEF EXECUTIVE OFFICER (CEO) / MANAGER
Section Break
name_of_chief_executive_officer__manager_section
28	
First Name
Data
ceo_first_name
eval:doc.ceo_differ == 1;
29	
Position
Data
ceo_position
eval:doc.ceo_differ == 1;
30	
Column Break
column_break_wpgv
31	
Last Name
Data
ceo_last_name
eval:doc.ceo_differ == 1;
32	
Sex
Select
gender

MALE
FEMALE
eval:doc.ceo_differ == 1;
33	
CONTACT OFFICER INFORMATION
Section Break
name_of_contact_officer_section
34	
First Name
Data
co_first_name
eval:doc.ceo_differ == 1;
35	
Position
Data
co_position
eval:doc.ceo_differ == 1;
36	
Column Break
column_break_ywdr
37	
Last Name
Data
co_last_name
eval:doc.ceo_differ == 1;
38	
Sex
Select
co_gender

MALE
FEMALE
eval:doc.ceo_differ == 1;
39	
COMPANY PROFILE
Section Break
section_break_21
40	
Short Description of the Company Profile
Text Editor
company_description
41	
State your Company’s knowledge and/or personal experience in recruiting students
Text Editor
company_experience
42	
💼 Experience
Tab Break
experience_tab
43	
RECRUITMENT EXPERIENCE WITH SINGAPORE INSTITUTIONS
Section Break
recruitment_experience_with_singapore_institutions_section
44	
Has Representation?
Check
has_representation
0
45	
Which Singapore schools/universities/institutions do you already represent
Table
school_representation
Agent School Childtable
eval:doc.has_representation == 1;
46	
How many students do you send to Singapore yearly?
Data
recruited_students_yearly
eval:doc.has_representation == 1;
47	
RECRUITMENT EXPERIENCE WITH OTHER COUNTRIES
Section Break
recruitment_experience_with_other_institutions_section
48	
Has Experience?
Check
has_experience
0
49	
Which School/ Universities/Institutions do you recruit for other than Singapore?
Table
school_recruit
Agent Recruit Childtable
eval:doc.has_experience == 1;
50	
How many students do you send to each country other than Singapore yearly?
Data
outside_sg
eval:doc.has_experience == 1;
51	
RECRUITMENT CAPACITY FOR UCC
Section Break
recruitment_capacity_for_ucc_section
52	
How many students will you be able to recruit for UCC yearly?
Table
students_ucc_yearly
Agent Yearly Recruitment Childtable
53	
Section Break
section_break_ofxt
How many students will you be able to recruit for UCC yearly?
54	
1st Quarter
Data
1st_quarter_target
55	
Column Break
column_break_nhjt
56	
2nd Quarter
Data
2nd_quarter_target
57	
Column Break
column_break_hpcw
58	
3rd Quarter
Data
3rd_quarter_target
59	
Column Break
column_break_wzzy
60	
4th Quarter
Data
4th_quarter_target
61	
🗂️ Recruitment
Tab Break
recruitment_strategy_and_payment_tab
62	
Please specify how you will recruit student for UCC?
Section Break
please_specify_how_you_will_recruit_student_for_ucc_section
63	
Exhibition
Check
exhibition
0
64	
Online Marketing
Check
online_marketing
0
65	
Seminar Talk
Check
seminar_talk
0
66	
School Talk
Check
school_talk
0
67	
1-to-1 Preview Session
Check
one_to_one
0
68	
Advertisement
Check
advertisement
0
69	
Column Break
column_break_svce
70	
Others
Check
others
0
71	
Please Specify
Text
please_specify
eval:doc.others == 1
60px
72	
Please give full details of any service fees you invoiced or intend to invoice the applicant for processing a student application:
Text
details_service_fees
60px
73	
Banking Information
Section Break
payment_detail_1_section
74	
Bank Name / Branch
Data
agent_bank_branch
75	
Account Number
Data
agent_account_number
76	
Bank Address
Data
agent_bank_address
77	
Column Break
column_break_ytni
78	
SWIFT code
Data
agent_swift_code
79	
Account Name
Data
agent_account_name
80	
Intermediary Bank Details
Section Break
payment_detail_2_section
81	
Intermediary Bank(s) Name / Branch
Data
agent_inter_bank_branch
82	
Intermediary Bank(s) SWIFT Code
Data
agent_inter_swift_code
83	
Column Break
column_break_iokb
84	
Intermediary Bank(s) Account Name
Data
agent_inter_account_name
85	
Intermediary Bank(s) Bank Address
Data
agent_inter_bank_address
86	
📎 Misc.
Tab Break
referee_and_documents_tab
87	
Referee Details
Section Break
referee_details_section
88	
Referee Name
Data
referee_name
89	
Referee Position
Data
referee_position
90	
Referee Phone
Data
referee_phone
91	
Column Break
column_break_tnxl
92	
Referee Organization
Data
referee_organization
93	
Referee Email
Data
referee_email
94	
Relationship to Applicant
Data
relationship_to_applicant
95	
Document Submission
Section Break
document_submission_section
96	
Business Registration
Attach
business_registration
Comprehensive information about your company information business information, such as details registered with ACRA or equivalent regulatory bodies.
97	
Table
table_vsbe
Agent Submission Document Childtable
98	
Column Break
column_break_anrp
99	
Company Profile
Attach
company_profile
Present an overview of your company's background, mission, vision, services offered, key personnel, and notable achievements.
100	
Column Break
column_break_leta
101	
Additional Documents
Attach
additional_documents
Include any supplementary materials that bolster your application, such as testimonials, references, marketing plans, or other relevant documents.
102	
Declaration
Section Break
declaration_section
103	
Name
Data
name_of_applicant
This will also be used under the "Declaration" (Print Format)
104	
Date
Date
date
105	
Column Break
column_break_utnn
106	
NRIC / Passport No
Data
nric_passport
107	
Signature
Signature
signature
Signature
108	
👍 Approval
Tab Break
approval_tab
109	
Approval
Section Break
approval_section
110	
Employee
Link
employee
Employee
111	
Processing Officer
Link
processing_officer
User
112	
Processing Officer Name
Data
processing_officer_name
processing_officer.full_name
113	
Processed Date
Date
processed_date
114	
Column Break
column_break_gnzv
115	
Approved by
Link
approved_by
User
116	
Approved by (Full Name)
Data
approved_by_full_name
User
approved_by.full_name
117	
Approved Date
Date
approved_date
118	
Identification and Selection Rating
Section Break
selection_rating_section
Focuses on the added value an agent brings to UCC.
119	
Shared Values and Vision
Rating
share_values_rating
Evaluates shared values, mission, vision, and culture.
120	
Legal Recognition and Compliance
Rating
legal_rating
Confirms legal recognition and compliance.
121	
Partnership Growth and Expansion
Rating
partnership_rating
Monitors growth and expansion opportunities.
122	
Column Break
column_break_eogi
123	
Collaborative Willingness and Strategic Alignment
Rating
collaborative_rating
Evaluates collaboration and strategic alignment.
124	
Financial and Operational Benefits
Rating
financial_rating
Examines financial and operational benefits.
125	
Communication Skills and Effectiveness
Rating
communication_rating
Assesses communication skills and effectiveness.
126	
Column Break
column_break_ulmk
127	
Cultural Competence and Diversity Engagement
Rating
cultural_rating
Evaluates cultural competence and engagement.
128	
Support and Resource Sharing
Rating
support_rating
Determines support and resource availability.
129	
Sustainability and Ethical Practices
Rating
sustainability_rating
Evaluates sustainability and ethical practices.
130	
Section Break
section_break_xbgb
131	
Provider Rating
Link
provider_rating
Provider Rating
132	
Average Partner Identification and Selection
Float
average_identification_and_selection_score
provider_rating.rating
133	
Column Break
column_break_nwcd
134	
Remarks
Text
remarks
provider_rating.note
135	
Section Break
section_break_ijhx
136	
Rating
Table
rating
Agent Provider Rating Childtable
137	
HTML
html_lxzc
138	
Onboarding
Section Break
onboarding_section
139	
Checklist Template
Link
checklist_template
Checklist Template
140	
Onboarding Checklist
Table
onboarding_checklist
Checklist List
141	
Section Break
section_break_vwuk
142	
Checklist Inline Editor
HTML
checklist_inline_editor
143	
🔍 Monitor
Tab Break
monitor_review_tab
144	
Agent Training and Review Log
Section Break
agent_training_and_review_log_section
145	
Training Log
Table
training_log
Agent Training and Review Log
146	
Section Break
section_break_vtxz
147	
Done Consent and Onboarding Survey?
Check
done_consent_and_onboarding_survey
0
148	
Column Break
column_break_eutt
149	
Onboarding Survey Date
Date
onboarding_survey_date
150	
Monitoring Schedule and Oversight
Section Break
monitor_section
Click "Edit" for more information.
151	
Agent Rating List
Table
agent_rating_list
Agent Rating List Childtable
152	
Service Performance Indicators
Table
agent_monitoring_childtable
Agents Monitoring Childtable
153	
Monitoring Summary
Text Editor
monitoring_summary
Additional qualitative feedback or notes regarding the monitoring of agent.
154	
Renewal Overview
Section Break
evaluation_overview_section
Evaluate the outcomes of the contract with the agent.
155	
Table
table_tczl
Agents Evaluation Childtable
156	
Agent Performance
Section Break
agent_performance_section
157	
Student Feedback
Table
student_feedback
Agent Student Onboarding Feedback
158	
Additional Notes
Section Break
evaluation_summary_section
159	
Text Editor
text_editor_pftn
Follow up action and summary of the evaluation outcome of the agreements.
160	
Exit Management
Section Break
exit_management_section
161	
Resignation Letter Date
Date
resignation_letter_date
162	
Relieving Date
Date
relieving_date
163	
Column Break
column_break_foeg
164	
Exit Interview Held On
Date
exit_interview_held_on
165	
Exit Interview
Link
exit_interview
Exit Interview
166	
Feedback
Section Break
feedback_section
167	
Reason for Leaving
Text
reason_for_leaving
168	
Column Break
column_break_rrkn
169	
Feedback
Text
feedback
170	
☢️ Internal
Tab Break
others_tab
171	
Notify Users
Section Break
notify_users_section
Key in the Master Agent email and the correspondence with student and agent will also be forwarded.
172	
Notify Users
Table
notify_users
User Email List
173	
Agent Credentials
Section Break
agent_credentials_section
This for LMS access
174	
Name
Data
username
175	
Password
Data
password
176	
Welcome Email Sent
Check
welcome_email_sent
0
177	
Column Break
column_break_muij
178	
Contract
Link
contract
Agent Contract
179	
NDA
Link
nda
Non Disclosure Agreement
180	
Section Break
section_break_tnzd
181	
Agent's Owner
Link
agent_owner
User
182	
Column Break
column_break_pyiq
183	
Agent Search Type
Select
agent_search_type

Proactive
Reactive
184	
Risk Assessment
Section Break
risk_assessment_section
185	
Risk assessment
Table
risk_assessment
Risk Identification Childtable
186	
Risk Management
Table
risk_management
Risk Justification Childtable
187	
Section Break
section_break_cnso
188	
Letter Head
Link
letter_head
Letter Head
UCC Agent Letter Head
189	
Full Course Commission
Data
fc_commission
190	
Short Course Commission
Data
sc_commission
191	
Column Break
column_break_ypry
192	
Provider
Link
supplier
Provider
193	
Identification Types
Select
identification_types

Proactive
Reactive
194	
🔔 Agent Notification
Tab Break
agent_notification_tab
Row Format:
Dynamic
Rows Threshold for Grid Search:
0
```
