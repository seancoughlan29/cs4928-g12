# Current-source feasibility check — 17 October 2026

The frozen sample is historical source from the supplied dataset. Its source
commit is not included in that file. A content hash pins what was evaluated,
but does not establish the date or current validity of its comments.

A read-only check of [AnkiDroid](https://github.com/ankidroid/Anki-Android)
resolved its then-current head to
[`311111b4f8a9a8f33494ab23bf13c95d64417a5c`](https://github.com/ankidroid/Anki-Android/commit/311111b4f8a9a8f33494ab23bf13c95d64417a5c).
At that pinned revision:

- The API lookup for
  `AnkiDroid/src/main/java/com/ichi2/anki/Preferences.java` returned 404.
- The parent directory contains a `preferences` directory.
- That directory contains `Preferences.kt`, `GeneralSettingsFragment.kt`,
  `NotificationsSettingsFragment.kt` and other Kotlin files.

These observations are recorded in `evidence/access-20261017.json`. They show
that the old file path is not available at this revision. They do **not** prove
which current method corresponds to any selected comment, or that a particular
comment has been removed. No Kotlin/Java build or tests were run in this check.

After detection selects the ten cases, trace their methods, relevant literals
and history to current equivalents. Record one of `MATCHED_UNCHANGED`,
`MATCHED_CHANGED`, `REMOVED_WITH_EVIDENCE`, or `UNRESOLVED`, with a commit/path
and reason. Review changed labels against current behaviour. Do not carry old
labels forward automatically or treat an unresolved case as a successful repair.

If current Java-only repair is mandatory and the selected cases cannot be
traced to eligible code, take this exact failure and the frozen case list to
the coordinator for the module contingency. Do not replace the sample after
seeing which cases are easy to repair.
