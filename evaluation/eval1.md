# Initial Retrieval Evaluation (eval1)

This is the recorded output from the initial retrieval benchmark, run against the 42 generated and manually reviewed labels in [`questions.json`](questions.json). The `Avg Latency` value reflects this run and can vary across environments.

```text
Loading weights: 100%|██████████████████████████████████████████████████████████████████████████████████████| 103/103 [00:00<00:00, 6330.42it/s]
Loaded 42 questions

===== RETRIEVAL EVALUATION =====
Total Questions: 42
Hit@1:           0.833
Hit@3:           1.000
MRR@3:           0.901
Avg Latency:     46.79 ms

===== FAILED TOP-1 QUESTIONS =====

ID: Q003
Question: How should API endpoints represent resources and actions?
Expected: [{'source': 'api_standards.txt', 'section': 'Resource Design'}]
  Rank 1: api_standards.txt / Request and Response Formats
  Rank 2: api_standards.txt / overview
  Rank 3: api_standards.txt / Resource Design

ID: Q010
Question: What types of tests should a pipeline include?
Expected: [{'source': 'ci_cd_guide.txt', 'section': 'Test Stages'}]
  Rank 1: ci_cd_guide.txt / Continuous Integration
  Rank 2: ci_cd_guide.txt / Test Stages
  Rank 3: ci_cd_guide.txt / Pipeline Reliability

ID: Q014
Question: What checks must pass before a release?
Expected: [{'source': 'deployment_guide.txt', 'section': 'Build Validation'}, {'source': 'ci_cd_guide.txt', 'section': 'Continuous Integration'}, {'source': 'ci_cd_guide.txt', 'section': 'Security and Quality Gates'}]
  Rank 1: release_management.txt / Release Readiness
  Rank 2: ci_cd_guide.txt / Security and Quality Gates
  Rank 3: release_management.txt / Release Execution

ID: Q018
Question: What information should be recorded when declaring an incident?
Expected: [{'source': 'incident_response.txt', 'section': 'Detect and Declare'}, {'source': 'troubleshooting_guide.txt', 'section': 'Start with the Symptom'}]
  Rank 1: incident_response.txt / Example Incident Checklist
  Rank 2: security_guidelines.txt / Logging and Incident Handling
  Rank 3: incident_response.txt / Detect and Declare

ID: Q038
Question: What information is useful to capture when reporting a service problem?
Expected: [{'source': 'troubleshooting_guide.txt', 'section': 'Start with the Symptom'}, {'source': 'incident_response.txt', 'section': 'Detect and Declare'}]
  Rank 1: troubleshooting_guide.txt / Confirm Resolution
  Rank 2: incident_response.txt / Resolve and Recover
  Rank 3: troubleshooting_guide.txt / Start with the Symptom

ID: Q039
Question: What should responders do when a recent change appears related to an incident?
Expected: [{'source': 'troubleshooting_guide.txt', 'section': 'Check Recent Changes'}, {'source': 'release_management.txt', 'section': 'Rollback and Forward Fixes'}, {'source': 'deployment_guide.txt', 'section': 'Rollback Procedure'}]
  Rank 1: troubleshooting_guide.txt / Escalation
  Rank 2: troubleshooting_guide.txt / Check Recent Changes
  Rank 3: incident_response.txt / Communicate

ID: Q042
Question: What are possible causes of authentication failures?
Expected: [{'source': 'troubleshooting_guide.txt', 'section': 'Common Symptom Patterns'}]
  Rank 1: troubleshooting_guide.txt / Start with the Symptom
  Rank 2: security_guidelines.txt / Secrets and Credentials
  Rank 3: troubleshooting_guide.txt / Common Symptom Patterns
```
