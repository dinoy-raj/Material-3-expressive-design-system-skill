# Reviewing a design or implementation

Use this guide when you're asked to review, audit or critique a screen, a flow, a pull request or a component in the M3 Expressive style. A review gives findings with evidence and ends in a verdict. It doesn't silently rewrite the work.

## How to review

1. **Find the scope.** List the screens, states, platforms and window sizes you were given. Note what you weren't given (for example "only a light theme screenshot").
2. **Identify the task.** Say what the screen is for and what its main action is. If you can't tell within a few seconds, that's the first finding.
3. **Work through the checks below** in order. The early sections matter more than the later ones.
4. **Record each finding** in the format below. Back each one with evidence: a file and line, a component name, a screenshot region, a measured contrast ratio.
5. **Give a verdict.**

## Checks

### 1. Task and hierarchy

- One screen pattern from `docs/screen-patterns.md` is recognisable, or the deviation has a reason.
- There's one hero and one filled button. The main action is obvious.
- Navigation, actions, selection and destructive actions look and behave differently.
- Loading, empty, error, offline and success states exist (see "States" in `docs/screen-patterns.md`).

### 2. Accessibility (always a blocker if it fails)

- Text contrast is 4.5:1 (3:1 at 24px and up); borders, tracks and focus rings are 3:1.
- Targets are 48dp (touch) or 24px with spacing (web pointer).
- Every gesture has a tap or keyboard alternative.
- Icon-only controls have names; state is exposed, not only shown.
- It works at 200% font scale, with reduced motion, and in RTL.
- See `docs/accessibility.md` for the full list.

### 3. M3 Expressive behaviour

- Pressables are pills or library shapes and morph on press; containers are `shape-xl`.
- Selection changes shape, not only colour.
- Grouped items sit 2dp apart with large outer and small inner corners.
- Spatial springs move things; effects springs change colour and opacity; there's no bounce on routine actions.
- Emphasis comes from type and tonal containers, not dividers, edge stripes or drop shadows on cards.
- Expression is proportionate (see "How much expression" in `SKILL.md`). Dense or utility screens use the standard motion scheme and fewer expressive moments.

### 4. Foundations

- Colours, type, shapes, spacing and motion come from tokens; no hard-coded hex values or radii.
- Light and dark themes both work. Dynamic colour, if used, doesn't break brand moments or meaning.
- Compact and expanded layouts are both defined.

### 5. Platform and code (implementations only)

- APIs exist in the version the project uses; experimental opt-ins are narrow and noted.
- No incidental dependency upgrades, library swaps or unrelated edits.
- The project's lint, tests and build pass, and the author says which ones they ran.

### 6. Content

- Sentence case, second person, verbs on buttons, real units, locale-aware formatting, no concatenated strings.

## Severity

| Severity | Meaning | Examples |
| --- | --- | --- |
| **Blocker** | Some users can't complete the task, or it breaks on a supported platform | Contrast below 3:1, swipe-only confirm, missing error state on payment, API not in the project's library version |
| **Major** | Clearly wrong for M3E or noticeably harder to use | Two filled buttons, no compact layout, hard-coded colours that break dark theme, bounce on every tap |
| **Minor** | Polish | Inconsistent shape per entity, an eyebrow in title case, a slightly wrong spring token |

## Finding format

```
[Severity] Short title
Where: file:line, component, or screen and region
Evidence: what you measured or saw
Why it matters: who it affects and how
Fix: the specific change, using kit tokens and components
```

Avoid vague findings like "make it more expressive". Name the token, component or rule.

## Verdict

End with one of these:

- **Ready:** no blockers or majors.
- **Ready with follow-up:** no blockers; the majors and minors listed can ship as tracked follow-ups.
- **Needs changes:** at least one blocker, or majors that together make the main task hard.

Then add one line on what you couldn't check (for example "not tested with TalkBack; only the light theme was provided").
