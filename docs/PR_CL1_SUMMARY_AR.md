# PR-CL1: Summary and Answers to Key Questions

## إجابات الأسئلة الثلاثة الأساسية

### 1. ما الذي صار "learning" وليس مجرد evaluation؟

**قبل PR-CL1** (CodeLearningTrace فقط):
- تقييم معزول لتغيير واحد
- لا ذاكرة (stateless)
- لا قرار (decision)
- لا رابط مع المشكلة الأصلية

```python
# قديم: تقييم بلا ذاكرة
trace = CodeLearningTrace(change=..., evidence=..., residuals=..., failures=...)
result = trace.to_result()  # يعطي Rank فقط، ثم ينتهي
```

**بعد PR-CL1** (الحلقة المحكومة):
- دورة كاملة: مشكلة → اقتراح → تقييم → قرار → تراكم معرفة
- ذاكرة دستورية (KnowledgeStore يتراكم)
- قرار منطقي (merge_allowed / revise / rollback / blocked)
- تتبع السلسلة الكاملة (ProblemTrace → PatchProposal → Decision)

```python
# جديد: تعلم بالتراكم الدستوري
problem = ProblemTrace(...)  # ملاحظة المشكلة
proposal = PatchProposal(problem=problem, changes=..., rationale=...)  # اقتراح الحل
loop = GovernedCodeLearningLoop()  # حلقة بذاكرة
decision = loop.evaluate_proposal(proposal, ...)  # تقييم + قرار
# KnowledgeStore يتراكم، trace محفوظ، decision قابل للـ replay
```

**الفارق الجوهري**:
- **التراكم**: KnowledgeStore يحفظ أنواع الأدلة (evidence kinds) وعدد البقايا (residual counts)
- **الربط**: كل patch له مشكلة محددة (no solution without problem)
- **القرار**: النظام يقرر (لا ينفذ) بناءً على القيود الدستورية
- **الـ Replay**: كل قرار محفوظ كسلسلة كاملة: problem → proposal → evaluation → decision

**هذا "تعلم" لأن**:
1. الذاكرة تتراكم (لا تُنسى بعد كل تقييم)
2. الأنماط تُسجَّل (evidence kinds, residual patterns)
3. القرارات تُحفظ (للمراجعة والتحليل)
4. النظام يطبق دستوره (لا يتجاوزه)

**ليس "تعلم إحصائي"** بل **تعلم دستوري** — التراكم محكوم بالقوانين الثمانية.

---

### 2. ما الذي بقي خارج النطاق؟

**لم نبنِ في PR-CL1** (explicitly NOT built):

#### (أ) AI Code Agent الكامل
- ❌ لا توليد تلقائي للـ patches من وصف المشكلة
- ✅ نأخذ PatchProposal جاهز (من إنسان أو agent خارجي)
- ✅ نقيّم الاقتراح، لا نُنشئه

#### (ب) Auto-Merge Bot
- ❌ لا دمج تلقائي بناءً على الـ rank
- ✅ decision="merge_allowed" استشاري فقط
- ✅ مراجع بشري ينفذ الدمج

#### (ج) Self-Modifying Runtime
- ❌ لا code generation ديناميكي
- ❌ لا eval() أو exec()
- ❌ لا تعديل للـ classes في runtime
- ✅ النظام يلاحظ التغييرات، لا ينفذها

#### (د) Neural/Statistical Learners
- ❌ لا ML models
- ❌ لا embeddings أو gradient descent
- ✅ KnowledgeStore عبارة عن tuples فقط
- ✅ "Learning" = تراكم، ليس optimization

#### (هـ) Persistent Storage
- ❌ لا database
- ❌ لا file writes
- ✅ in-memory فقط
- ✅ replay() يعطي dict للحفظ (إذا أراد المستخدم)

#### (و) Multi-Agent Coordination
- ❌ لا distributed learning
- ❌ لا consensus protocol
- ✅ instance واحد من GovernedCodeLearningLoop

**لماذا خارج النطاق؟**

المبدأ الدستوري:
> **"الجبر العام لا يتوسع بالتراكم، بل يتدرج بالحد الأدنى الكافي"**

نبني **الحلقة الأدنى** التي تُمرِّن الدستور. Heavy learners تأتي لاحقاً (Phase 3+) بعد ربط الجبر بكل الطبقات.

---

### 3. ما الضمان أن النظام لا يغيّر نفسه ارتجاليًا؟

**ثلاث طبقات دفاع**:

#### الطبقة 1: Immutability (ضمان نوعي Type-Level)

```python
@dataclass(frozen=True)  # ← لا يمكن التعديل بعد الإنشاء
class ProblemTrace: ...

@dataclass(frozen=True)
class PatchProposal: ...

@dataclass(frozen=True)
class CodeLearningDecision: ...
```

**الضمان**: لا يمكن لأي object تعديل حالته الداخلية. كل dataclass مُجمّد.

---

#### الطبقة 2: No-Execute Contract (ضمان إجرائي Operational)

```python
class GovernedCodeLearningLoop:
    def evaluate_proposal(self, proposal: PatchProposal, ...) -> CodeLearningDecision:
        # ❌ لا نفعل:
        # - تنفيذ proposal.changes (no write to filesystem)
        # - استيراد الكود المعدّل (no dynamic import)
        # - eval/exec للكود المقترح
        # - تعديل entries في _knowledge_store (append-only)

        # ✅ نفعل فقط:
        # - قراءة proposal fields
        # - إنشاء CodeLearningTrace
        # - تطبيق rank policy
        # - إضافة إلى KnowledgeStore (append, not modify)
        # - إعادة decision (استشاري)
```

**الضمان**: الحلقة **observational only** — تقرأ، تطبق السياسة، تُراكم، تعيد القرار. **لا تنفذ**.

---

#### الطبقة 3: Constitutional Gates (ضمان جبري Algebraic)

**القوانين الثمانية** مُطبّقة في `evaluate_proposal`:

1. **No Evidence → CANDIDATE** → decision="revise"
2. **No CERTIFIED without Evidence** → max(CANDIDATE, LICENSED)
3. **No CERTIFIED with Residuals** → LICENSED max → decision="revise"
4. **Fatal Failure → REFUTED** → decision="rollback"
5. **Architectural Change without Admission → BLOCKED** → decision="blocked"
6. **Passing Tests ≠ Architectural Correctness** → architectural admission required
7. **Every Decision Carries Trace** → full replay chain preserved
8. **KnowledgeStore Accumulates** → append-only, no modification

**الضمان**: حتى لو أردنا auto-merge، البوابات تمنعه:
- تغيير معماري بلا admission → BLOCKED
- أي بقايا → max LICENSED (ليس CERTIFIED) → decision != "merge_allowed"
- فشل قاتل → REFUTED → decision="rollback"

**مثال Runtime Enforcement**:

```python
# محاولة تجاوز الدستور
proposal = PatchProposal(
    problem=problem,
    changes=[CodeChange(path="core.py", ...)],  # تغيير معماري
    architectural_admission=None,  # لا admission!
)

decision = loop.evaluate_proposal(proposal, test_evidence=[...])

# النتيجة:
# decision.decision == "blocked"
# decision.reason == "Architectural change without admission (violates constitution)"
```

**النظام لا يستطيع تجاوز بواباته** لأن:
1. `evaluate_proposal` يُطبّق البوابات قبل القرار
2. القرار استشاري (المستخدم ينفذ)
3. البوابات دوال نقية (deterministic, no side effects)
4. لا code generation في runtime

---

## التحقق الوظيفي

```
Test 1: Bug fix with evidence, no residuals → merge_allowed ✓
Test 2: Architectural change without admission → blocked ✓
Test 3: Evidence + residuals → LICENSED → revise ✓
Test 4: Fatal failure → REFUTED → rollback ✓
Test 5: KnowledgeStore accumulates evidence ✓
```

---

## الخلاصة

**PR-CL1 يضيف**:
- حلقة تعلم محكومة (governed learning loop)
- ذاكرة دستورية (constitutional memory)
- قرارات منطقية (decision logic)
- ربط المشاكل بالحلول (problem traceability)

**PR-CL1 لا يضيف**:
- توليد كود AI
- دمج تلقائي
- تعديل ذاتي في runtime
- متعلمين عصبيين

**الضمانات**:
- عدم التغيير (immutability)
- عدم التنفيذ (no-execute contract)
- البوابات الدستورية (8 critical laws)

**التعلم كذاكرة دستورية، ليس استدلالاً إحصائياً.**

---

**Files**:
- `src/fvafk/algebra/code_learning_loop.py` (320 lines, core implementation)
- `tests/test_algebra_code_learning_loop.py` (comprehensive test suite)
- `docs/PR_CL1_CODE_LEARNING_LOOP.md` (full documentation)
- `src/fvafk/algebra/__init__.py` (exports added)

**Commit**: 87567c8
**Status**: ✅ All tests pass, ready for review
