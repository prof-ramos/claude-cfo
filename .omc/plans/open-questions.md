# Open Questions

This file tracks unresolved questions, decisions deferred to the user, and items needing clarification before or during execution.

---

## E2E Tests - 2026-03-06 (Updated after Architect Review)

- [ ] **Sidebar widget access confirmation** — Need to verify during implementation that `at.sidebar.radio` and `at.sidebar.button` work as expected. Documentation is unclear.
  - *Action:* Run `test_sidebar_api_verification` first and document findings in README

- [ ] **Exact checkbox count** — Currently estimated at ~246 across 15 disciplines. Will confirm during implementation and update documentation.

### Resolved (After Architect Review)

- [x] **AppTest widget access patterns** — RESOLVED: Use explicit keys with pattern `cb_{discipline}||{topic}`. The app defines these keys at line 609: `key=f"cb_{key}"` where `key = get_topic_key(discipline, topic)`.

- [x] **Sidebar vs main widget access** — RESOLVED: Sidebar has status filter radio and discipline buttons. Main area has metrics mode radio and topic checkboxes.

- [x] **Progress file mocking** — RESOLVED: Must use environment variable `PROGRESS_FILE` instead of `monkeypatch.setattr` because `PROGRESS_FILE` is a module-level constant evaluated at import time, and `AppTest.from_file()` loads the app in a subprocess.

- [x] **Persistence testing** — RESOLVED: Added `test_persistence_across_runs` to verify progress survives separate `AppTest` instances.

---

## UX Improvements - Hierarchical Edital - 2026-03-06

- [ ] **Remove st.rerun() impact on metrics** — Need to verify if removing `st.rerun()` at line 614 causes metrics to not update in real-time. If needed, may need to use `st.experimental_rerun()` or accept delayed updates.
  - *Action:* Test thoroughly during Phase 2 implementation

- [ ] **Indentation readability in 2-column layout** — Need user testing to confirm that 3-space indentation (` `) is visually clear when topics are split across 2 columns.
  - *Action:* If confusing, consider switching to single-column layout for hierarchical topics

- [ ] **Checkbox behavior when unchecking parent** — Should unchecking a parent topic automatically uncheck all descendants? Current spec only implements auto-check, not auto-uncheck.
  - *Decision needed:* User preference for auto-uncheck behavior

- [ ] **Display of topic numbers** — Should the full number (e.g., "1.2.3") be visible in the checkbox label, or just the text? Current spec shows only text.
  - *Decision needed:* User preference for displaying hierarchical numbers
