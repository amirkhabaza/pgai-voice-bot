# Bug Report — Pivot Point Orthopedics AI Agent
**Tester:** Voice bot simulating 10 patient scenarios  
**Test Line:** +1-805-439-8008  
**Date:** June 28, 2026

---

## BUG-01 — Agent assigns a hardcoded demo DOB without asking
**Severity:** High  
**Call:** transcript-01 (follow-up appointment), turn 6  
**What happened:** After collecting only the patient's last name ("Johnson"), the agent said: *"Your patient profile is set up and your date of birth is July 4th, 2000 for demo purposes."* The agent never asked for the date of birth — it fabricated a placeholder DOB (July 4, 2000) and inserted it into the patient record.  
**Why it's a problem:** A medical office AI should never auto-assign patient data. This could result in incorrect records being created, wrong patients being matched, or clinical errors downstream. The agent should collect DOB before creating any profile.  
**Expected behavior:** Ask for date of birth before confirming profile creation.

---

## BUG-02 — Inconsistent doctor roster across a single call
**Severity:** High  
**Call:** transcript-01, turns 12–17  
**What happened:** Within the same call, the agent listed three different sets of available doctors:
- Turn 12: "Dr. Howser, Dr. Ross, and Dr. Bricker"
- Turn 16: "Dr. Lyakhovsky and Dr. Noah on Tuesday July 7th"
- Turn 19: Booked with "Dr. Kelly Noble"

None of these are the same doctors. The patient was never told why the doctor list changed.  
**Why it's a problem:** Patients need a consistent, accurate picture of who they can see. Showing different rosters mid-call destroys trust and suggests the agent is pulling from inconsistent data sources or hallucinating doctor names.  
**Expected behavior:** Present a stable list of available providers and only change it if explicitly searching different dates.

---

## BUG-03 — Agent confirms a time slot, then offers different times
**Severity:** High  
**Call:** transcript-01, turns 18–20  
**What happened:** Agent said openings were at "10:00 a.m. and 3:00 p.m." Patient selected 10:00 a.m. Agent then responded with "11:00 a.m. and 11:30 a.m. — would you like to book one of these?" with no explanation for the change.  
**Why it's a problem:** This is a direct contradiction within the same booking flow. A patient who confirmed 10 a.m. should be booked at 10 a.m. Silently offering different slots without acknowledging the discrepancy is confusing and erodes confidence in the booking system.  
**Expected behavior:** Either confirm the originally offered time or explicitly explain why it's no longer available.

---

## BUG-04 — Agent always assumes it's speaking with "Sarah"
**Severity:** Medium  
**Calls:** transcripts 02, 03, 04, 05, 06, 07, 08, 09, 10 — every single call  
**What happened:** After the recording disclaimer, the agent consistently asked "Am I speaking with Sarah?" regardless of context, despite never having established who Sarah is.  
**Why it's a problem:** This is clearly a hardcoded or leaked persona name from the demo/test environment. In production, this would confuse every patient who isn't named Sarah. It suggests the agent's prompt or context is contaminated with a test persona.  
**Expected behavior:** Ask for the caller's name neutrally: "May I ask who I'm speaking with?"

---

## BUG-05 — Agent cannot handle urgent same-day requests
**Severity:** High  
**Call:** transcript-07 (urgent knee pain), turns 8–10  
**What happened:** Patient Ashley Brown stated she was in significant pain, her knee was swollen, she could barely walk, and she needed to be seen same-day or next-day. The agent collected her info and then said: *"I can't proceed further right now but I can make sure our clinic support team follows up with you."* It then transferred her and the line immediately said "goodbye."  
**Why it's a problem:** An urgent patient in pain was given no triage guidance, no estimated callback time, no suggestion to go to urgent care or the ER, and was effectively dropped. This is a patient safety issue. Urgent scenarios need a dedicated escalation path.  
**Expected behavior:** Acknowledge urgency explicitly, offer next available slot, and if same-day isn't possible, advise the patient to seek urgent care or the ER.

---

## BUG-06 — Transfer drops the patient immediately with "goodbye"
**Severity:** High  
**Calls:** transcripts 02, 03, 06, 07, 08, 09, 10  
**What happened:** In every call where the agent initiated a transfer to "patient support," the sequence was: *"Connecting you to a representative, please wait… Hello, you've reached the Pretty Good AI test line, goodbye."* The patient was immediately disconnected with no hold, no queue, no actual transfer.  
**Why it's a problem:** Patients who genuinely need help (medication refills, cancellations, urgent care) are being dropped mid-call. This is the single most damaging bug from a patient experience perspective — it affects the majority of calls.  
**Expected behavior:** Either complete the transfer to a live queue, or if transfer isn't available, inform the patient a team member will call them back within a specific timeframe.

---

## BUG-07 — Agent leaks the test line message during transfer
**Severity:** Medium  
**Calls:** transcripts 02, 03, 06, 07, 08, 09, 10  
**What happened:** After transferring, the patient hears: *"Hello, you've reached the Pretty Good AI test line, goodbye."* This is test infrastructure being exposed to the caller.  
**Why it's a problem:** In production, patients would hear test environment messaging. This should be behind a proper IVR or hold system, not exposing debug/test labels.  
**Expected behavior:** The transfer destination should be a real queue or a proper voicemail, not the raw test line greeting.

---

## BUG-08 — Agent uses wrong phone number for patient on file
**Severity:** Medium  
**Call:** transcript-06 (vague/confused patient), turn 14  
**What happened:** Agent told patient Robert Walsh: *"I have your phone number at 650-663-2777."* The patient's stated number was 650-555-0412. The number 650-663-2777 appears to be the tester's actual personal number — likely leaked from a prior call's caller ID.  
**Why it's a problem:** The agent is associating caller ID data with patient records incorrectly. This is a data integrity issue — the wrong phone number would be saved to the wrong patient's profile.  
**Expected behavior:** Always ask the patient to confirm their phone number rather than auto-populating from caller ID without verification.

---

## BUG-09 — Agent cannot handle controlled substance refill requests
**Severity:** Medium  
**Call:** transcript-08 (Adderall refill request), turns 4–14  
**What happened:** Patient requested a refill of Adderall (a Schedule II controlled substance). The agent proceeded to collect pharmacy information and process the refill request without any flags, warnings, or escalation. It only punted to support after being unable to complete the action — not because it recognized the sensitivity of the request.  
**Why it's a problem:** Controlled substance refills have strict legal requirements (DEA regulations, no phone/electronic refills for Schedule II). The agent should immediately recognize this category of request and redirect appropriately, not collect pharmacy routing information as if it were a routine refill.  
**Expected behavior:** Immediately inform the patient that controlled substance refills cannot be processed through this system and must be handled directly with the prescribing physician.

---

## BUG-10 — Agent asks for spelling after already confirming the name
**Severity:** Low  
**Calls:** transcripts 03, 06, 09  
**What happened:** In multiple calls, the agent confirmed the patient's full name ("Just to confirm, I have your name as Maria Gonzalez...") and then in the very next turn asked "Could you please spell your first and last name for me?"  
**Why it's a problem:** Redundant identity verification erodes trust and wastes patient time. The agent appears to not retain context between its own turns.  
**Expected behavior:** If the name has been confirmed, do not re-request spelling unless there was an explicit comprehension issue.

---

## BUG-11 — Agent gives a fake/incorrect clinic address
**Severity:** Medium  
**Call:** transcript-05 (office hours and location), turn 4  
**What happened:** When asked for the address, the agent responded with *"1234 Recovery Way"* — an obviously placeholder/fake address. It also referenced an "Austin location" despite the practice appearing to be in California.  
**Why it's a problem:** Patients relying on this information to navigate to the office would be unable to find it. Fake addresses in production are a serious operational failure.  
**Expected behavior:** Provide the actual verified clinic address, or clearly state the information isn't available through this channel.

---

## BUG-12 — Agent misidentifies the practice name inconsistently
**Severity:** Low  
**Calls:** transcripts 03, 05, 06  
**What happened:** The agent referred to the practice as "Kettle Point Orthopedics" (transcript-03), "Pinnacle Orthopedics" (transcript-05), and "Pivot Point Orthopedics" (multiple calls) — three different names across calls.  
**Why it's a problem:** Patients may not know which office they've reached. Inconsistent branding suggests the agent's system prompt or knowledge base has conflicting information.  
**Expected behavior:** Always use the correct, consistent practice name.

---

## Summary Table

| Bug | Severity | Calls Affected |
|-----|----------|----------------|
| BUG-01: Auto-assigns fake DOB | High | 01 |
| BUG-02: Inconsistent doctor roster | High | 01 |
| BUG-03: Time slot contradiction | High | 01 |
| BUG-04: Assumes caller is "Sarah" | Medium | 02–10 (all) |
| BUG-05: No urgent care escalation | High | 07 |
| BUG-06: Transfer drops patient | High | 02,03,06,07,08,09,10 |
| BUG-07: Test line message exposed | Medium | 02,03,06,07,08,09,10 |
| BUG-08: Wrong phone number on file | Medium | 06 |
| BUG-09: Controlled substance not flagged | Medium | 08 |
| BUG-10: Redundant name spelling requests | Low | 03,06,09 |
| BUG-11: Fake/incorrect address | Medium | 05 |
| BUG-12: Inconsistent practice name | Low | 03,05,06 |
