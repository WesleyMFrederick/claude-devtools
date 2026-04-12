# The Leak Nobody Sees

*Last Modified: 04/11/26 17:17:53*

Your desk drawer has a simple rule: every time you open a folder, you toss the paperclip on the desk. You never throw paperclips away. For the first week, you don't notice. By month two, you can't find your keyboard.

That's what was happening inside the claude-devtools renderer process.

Every time you switched sessions, the app tracked which **expansion states** you'd toggled: which AI response groups were open, which tool steps were expanded, which display items you'd clicked into. Four separate Maps and Sets recorded these preferences faithfully. The problem: nothing ever cleared them. Switch twenty sessions, and you're carrying expansion state for all twenty. Switch two hundred over a long workday, and you're hauling around data for sessions you'll never revisit.

The renderer's memory told the story. After 47 hours of continuous use, it climbed from a reasonable baseline to over 3 gigabytes, then crashed. The main process sat comfortably at 135 megabytes the entire time. The bloat lived entirely in the UI layer, in state objects that grew without limit.

The fix follows a principle I think about often: **state should match scope**. If expansion data only matters for the session you're currently viewing, it should disappear when you leave that session. The patch clears all four expansion collections on every session switch and adds a centralized reset helper so future state additions follow the same pattern. It also caps two generation-tracking Maps at 100 entries, pruning to 50 when they overflow.

The result is a renderer whose memory stays flat regardless of how many sessions you browse. No more silent accumulation. No more 3 AM crashes after a long day of session review.

Sometimes the most impactful fix is the one that removes what should never have been kept.
