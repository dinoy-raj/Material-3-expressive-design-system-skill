# Snackbar

Brief confirmation at the bottom of the screen, on `inverse-surface`, with at most one action.

**Provide:** `message` (past tense, what happened: "Saved to Favourites"), optional `action` ("Undo", "View") and `onAction`.

- Show for four to ten seconds above the navigation bar; never stack two.
- Don't use a snackbar for errors that block progress; use an inline error or a dialog.
