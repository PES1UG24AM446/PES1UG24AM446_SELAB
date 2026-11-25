# Lab 1 Requirements Review

The following AI-assisted review checks the published requirements for clarity, testability and relevance to scenario 05. The peer-exchange activity calls for a separate classmate’s review.

| Requirement | Comments | Check in the submitted requirements |
| --- | --- | --- |
| FR-001 | State whether 100 credits is an exact total and what happens to a stored bid on failure. | The 99, 100 and 101 credit cases distinguish the boundary, and rejected submissions leave the stored bid unchanged. |
| FR-002 | Make duplicate ranks and missing amounts independently testable. | The acceptance criteria cover duplicate and missing ranks, missing amounts and preservation after reload. |
| FR-003 | Define whether adjacent events count as overlapping. | The acceptance test distinguishes a one-minute overlap from exactly adjacent slots. |
| FR-004 | Specify what to do when the first waitlist candidate is ineligible. | The test skips the candidate, promotes the next eligible student once and checks the notification deadline. |
| FR-005 | A required reason alone cannot establish authorization. | The test exercises a student request, a registrar request and a blank reason. |
| NFR-001 | A throughput number needs a reproducible measurement plan. | The acceptance test fixes the workload, requires three runs and checks elapsed time and conflicts. Deployment benchmarking remains an implementation task. |
| NFR-002 | Audit evidence must cover integrity and retrieval as well as retention. | The tests check unauthorized writes, changed records, retrieval time and the retention policy. |
