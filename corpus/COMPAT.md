# Corpus compatibility matrix

Records which `architecture-buddy` skill versions have known PASS calibration runs against golden ids (or migration targets). Update when a calibration or migration run is judged PASS/FAIL.

| skill_version | golden_id | cal_run | result | date |
|---------------|-----------|---------|--------|------|
| 0.3.0 | kafka | 2026-08-05-cal-kafka | PASS | 2026-08-05 |
| 0.3.0 | git | 2026-08-05-cal-git | PASS | 2026-08-05 |
| 0.3.0 | kubernetes | 2026-08-05-cal-kubernetes | PASS | 2026-08-05 |
| 0.3.0 | etcd | 2026-08-05-cal-etcd | PASS | 2026-08-05 |
| 0.3.0 | hdfs | 2026-08-05-cal-hdfs | PASS | 2026-08-05 |
| 0.3.0 | spark | 2026-08-05-cal-spark | PASS | 2026-08-05 |
| 0.3.0 | minecraft | 2026-08-05-cal-minecraft | PASS | 2026-08-05 |
| 0.3.0 | sre-buddy | 2026-08-05-mig-sre-buddy | PASS | 2026-08-05 |

Notes:

- `sre-buddy` is a **migration** target (`mig-sre-buddy`), not a formal GOLDEN under `corpus/golden/`.
- Phase 2 goldens `hdfs` / `spark` now have dedicated reproduction cal PASS runs (`skill_calibrated: 0.3.0`); `agent-runtime` still has no dedicated reproduction cal run yet (`skill_calibrated: none` in META).
- Phase 3 golden `minecraft` now has reproduction cal PASS (`corpus/runs/2026-08-05-cal-minecraft.md`; `skill_calibrated: 0.3.0`).
- Skill frontmatter version: `skill/architecture-buddy/SKILL.md` → `metadata.version: "0.3.0"`.
