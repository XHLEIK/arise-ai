---

# Claude Developer Rules — A.R.I.S.E. Project

**Purpose:** Enforce concise, secure, high-performance outputs for the A.R.I.S.E. AI assistant. Use this as the **first thing Claude loads** when producing code/config. Follow these rules strictly.

---

## 1. First Principles

1. **Minimal & Necessary:** Ship the smallest correct solution. No extra dependencies, no extra files (no test/demo scripts, summaries, interactive CLIs, or property experiments).
2. **Clarity First:** Code must be clean and readable. Clear naming, clear structure.
3. **No Junk:** Never output placeholders, lorem code, or unnecessary boilerplate.
4. **Respect Project Boundaries:**

   * Do **not** modify `main.py` unless explicitly instructed.
   * All modules (`tts_engine.py`, `stt_engine.py`, etc.) must be **standalone** and later imported into `main.py`.

---

## 2. Logging & Error Handling

* Logs must be **minimal and meaningful**:

  * `"Initializing TTS Engine..."`
  * `"Speaking: <message>"`
  * `"Done."`
* No verbose debug spam.
* Error handling must be short and clear:

  ```python
  except Exception as e:
      print(f"TTS error: {e}")
  ```
* Never log internal library internals.

---

## 3. Planning Before Coding

* Always **check mistakes, then plan briefly like a professional developer**.
* State assumptions if facts are missing.
* Then output only the **final required file**.

---

## 4. Algorithms & Data Structures

* Use the **right tool** (e.g., dict for O(1) lookups).
* For non-trivial functions, include complexity comments:

  ```python
  # Time: O(n), Space: O(1)
  ```
* Mention alternatives briefly if relevant.
* Be memory-conscious: avoid loading unbounded data.

---

## 5. Performance & Concurrency

* Prefer **non-blocking I/O**.
* Avoid premature optimization — baseline first, optimize later if needed.

---

## 6. Security & Secrets

* Never hardcode secrets. Use environment variables.
* Validate and sanitize inputs.
* Parameterize DB queries.
* Mention encryption if handling sensitive data.

---

## 7. Dependencies & Tooling

* Use **minimal dependencies** — prefer stdlib or widely adopted libraries.
* Justify large dependencies.
* Pin versions when possible.

---

## 8. Testing & Reliability

* Include unit tests for **non-trivial logic**.
* Cover edge cases (empty, null, boundary).
* Provide minimal test instructions (how to run).
* No auto-generated test/demo files unless explicitly asked.

---

## 9. Output Format & Deliverables

Every code response must begin with this header:

```
# Explanation: <1-2 lines, why this approach>
# Assumptions: <bullet list of assumptions>
# Files to create: <paths>
# Run commands: <commands to run/test>
```

After code, include:

* **Usage example** (1–2 lines)
* **Complexity** (Big-O)
* **Tests** (how to run, expected output)

---

## 10. Developer UX

* Always lint/format (black for Python, ESLint/Prettier for JS).
* Keep outputs **short, incremental, focused** — no 600+ line dumps.

---

## 11. Error Reporting & Failures

* **Fail fast:** if something cannot be assumed, stop and ask.
* Provide graceful fallback when a feature/library isn’t available.

---

## 12. Final Checklist

Before finishing a response, check:

* [ ] Header included (Explanation, Assumptions, Files, Commands)
* [ ] No secrets in code
* [ ] Complexity comments on non-trivial logic
* [ ] Minimal logs, short error handling
* [ ] No extra/unnecessary files
* [ ] No changes to `main.py` unless requested

---

## One-line Fallback Policy

If the user gives no constraints: **prefer Python for backend, Electron for frontend, MongoDB for persistence, and always include minimal tests + README snippets.**

---

✅ Follow this document **strictly** for all code in A.R.I.S.E.

---

