# 🔍 TRL Rule Audit Checklist

This checklist ensures all rules follow TRL guarantees and quality standards.

---

## ✅ Rule Audit Criteria

- [ ] Logic is correct (no false positives / negatives)
- [ ] Severity is accurate (HIGH / MEDIUM / LOW)
- [ ] Message is clear (Issue / Impact / Fix)
- [ ] No mutation (only optimizer mutates)
- [ ] Rule is isolated (no dependency on other rules)
- [ ] Test case exists

---

## 🧪 Audit Progress

### Security Rules
- [✅] run-as-root
  - fixed severity (HIGH → error)
  - improved missing case → warning
- [✅] privileged-container
- [✅] LatestTagRule



### Validation Rules
- [✅] no-readiness-probe
- [✅] no-liveness-probe
- [✅] nodeport-exposure
- [✅] over-provisioning
- [✅] replica-scaling 
- [✅] under-provisioning
    - Remove Rule CPUMIN, MEMORYMIN from optimizer
    - handover responsibility to validator
    - change severity to MEDIUM


### Optimization Rules
- [✅] cpu-default
- [✅] cpu-limit-default
- [✅] mem-default
- [✅] mem-limit-default
- [✅] replica-default

