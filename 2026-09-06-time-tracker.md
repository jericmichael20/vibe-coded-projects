# Time Tracker Implementation Plan

> For agentic workers: REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Build a single-file browser time tracker that lets one person add today’s tasks, run one live stopwatch, switch tasks, complete tasks, and review saved sessions.

**Architecture:** Keep one application state object with tasks, sessions, and activeTimer. Render all visible values from that state, persist it under time-tracker-v1, and use one delegated event listener for task and timer actions. Keep markup, custom CSS, and plain JavaScript in time-tracker.html.

**Tech Stack:** HTML, Tailwind CSS browser CDN 4, daisyUI 5, daisyUI nord theme, plain JavaScript, browser localStorage.

**Spec:** docs/superpowers/specs/2026-09-06-time-tracker-design.md

## Global Constraints

- Deliver one file: time-tracker.html.
- Load daisyUI from https://cdn.jsdelivr.net/npm/daisyui@5.
- Load Tailwind from https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.
- Keep custom styling inside the HTML style block.
- Use plain JavaScript inside the HTML script block.
- Use no build step.
- Use no image assets.
- Use no external icon library.
- Set <html data-theme="nord">.
- Store the state under the key time-tracker-v1.
- Do not add manual time entries, Pomodoro sessions, accounts, sync, projects, tags, estimates, due dates, reminders, or analytics.
- Use daisyUI semantic classes for buttons, cards, navigation, hero content, stats, timeline, inputs, checkboxes, badges, and alerts.
- Use direct labels, active voice, no adverbs, no jargon, no em dashes, and no generic productivity slogans.
- Keep the timer display derived from activeTimer.startedAt. Do not store a second elapsed-time counter.

## File Structure

- Create: time-tracker.html
  - HTML landmarks and daisyUI component markup
  - Custom CSS for timer digits, focus treatment, and responsive details
  - State model, persistence, rendering, task actions, timer actions, and verification hooks
- Read: docs/superpowers/specs/2026-09-06-time-tracker-design.md

The workspace has no Git repository, so use the task checklist and browser verification as review gates instead of commit steps.

---

### Task 1: Create the accessible page shell

**Files:**
- Create: time-tracker.html
- Test: browser console smoke check

**Interfaces:**
- Produces semantic regions with the IDs used by later tasks: app-status, timer-display, timer-task-title, timer-action, add-task-form, task-input, task-list, task-count, stats-time, stats-completed, activity-list, and clear-day.

- [ ] Step 1: Run the failing shell check

Open the empty file in a browser and run:

~~~js
[
  "app-status",
  "timer-display",
  "timer-task-title",
  "timer-action",
  "add-task-form",
  "task-input",
  "task-list",
  "task-count",
  "stats-time",
  "stats-completed",
  "activity-list",
  "clear-day"
].forEach((id) => console.assert(document.getElementById(id), "missing #" + id));
~~~

Expected: the assertions fail because the page has no shell yet.

- [ ] Step 2: Add the document head

Add this exact document head:

~~~html
<!doctype html>
<html lang="en" data-theme="nord">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="A focused time tracker with a task queue." />
    <title>Time Tracker</title>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  </head>
~~~

- [ ] Step 3: Add the landmark shell

Add a body with one header, one main, and one footer. Give the main region an h1 named Time Tracker. Add the status region as:

~~~html
<div id="app-status" class="alert hidden" role="status" aria-live="polite"></div>
~~~

Add empty elements with the exact IDs from the Interfaces block. Use lists for task-list and activity-list. Use a real button for clear-day.

- [ ] Step 4: Run the shell check again

Run the console check from Step 1.

Expected: every assertion passes.

---

### Task 2: Add the Queue First layout and daisyUI surfaces

**Files:**
- Modify: time-tracker.html
- Test: desktop and mobile browser viewports

**Interfaces:**
- Consumes: the shell IDs from Task 1.
- Produces: visible navbar, stats, hero, card, input, checkbox, badge, timeline, btn, and alert surfaces.

- [ ] Step 1: Write the failing layout check

Run this in the browser console:

~~~js
[
  ".navbar",
  ".stats",
  ".hero",
  ".card",
  ".input",
  ".btn",
  ".timeline"
].forEach((selector) => console.assert(document.querySelector(selector), "missing " + selector));
~~~

Expected: the assertions fail because the component surfaces do not exist.

- [ ] Step 2: Add the top navigation

Use this structure inside body:

~~~html
<header class="navbar border-b border-base-300 bg-base-100 px-4 sm:px-6">
  <div class="navbar-start">
    <a class="btn btn-ghost px-2 text-lg font-semibold" href="#main-content">Time Tracker</a>
  </div>
  <div class="navbar-end gap-2">
    <time id="today-label" class="hidden text-sm text-base-content/60 sm:block"></time>
    <button id="clear-day" class="btn btn-ghost btn-sm" type="button">Clear day</button>
  </div>
</header>
~~~

- [ ] Step 3: Add the main surfaces

Use main with id main-content and a responsive container. Place a horizontal stats surface above a two-column grid. Put the timer in a hero with hero-content and a nested card, then put the Today queue beside it. Use this exact queue form shape:

~~~html
<form id="add-task-form" class="join w-full" novalidate>
  <label class="sr-only" for="task-input">Task name</label>
  <input id="task-input" class="input join-item min-w-0 flex-1" type="text" maxlength="120" autocomplete="off" placeholder="Add a task" />
  <button class="btn btn-primary join-item" type="submit">Add task</button>
</form>
~~~

Add task-count beside the Today heading and place task-list inside a ul. Add an Activity card below the grid with activity-list as a vertical timeline container.

- [ ] Step 4: Add empty-state content

Use these exact visible strings in the initial markup:

~~~html
<p id="task-empty" class="py-8 text-center text-sm text-base-content/60">No tasks yet. Add one to begin.</p>
<p id="activity-empty" class="py-8 text-center text-sm text-base-content/60">No sessions yet.</p>
~~~

Give the timer card the heading Now, the task title No active task, the initial display 00:00:00, and a disabled Start timer button until a task exists.

- [ ] Step 5: Run the layout check

Run the console check from Step 1 at a wide viewport and a narrow viewport.

Expected: every component assertion passes, the desktop layout uses two columns, and the narrow layout stacks the timer before the queue.

---

### Task 3: Add state normalization and localStorage persistence

**Files:**
- Modify: time-tracker.html
- Test: browser console state round-trip check

**Interfaces:**
- Produces: emptyState(), normalizeState(value), loadState(), saveState(), appState, STORAGE_KEY, and storageMessage.

- [ ] Step 1: Run the failing persistence check

Run:

~~~js
console.assert(typeof window.loadState === "function", "loadState is missing");
console.assert(typeof window.saveState === "function", "saveState is missing");
~~~

Expected: both assertions fail because the persistence functions do not exist.

- [ ] Step 2: Add the state constants and factory

Add this exact state setup in the script block:

~~~js
const STORAGE_KEY = "time-tracker-v1";
let storageMessage = "";

function emptyState() {
  return { tasks: [], sessions: [], activeTimer: null };
}

let appState = emptyState();
~~~

- [ ] Step 3: Add state normalization

Add this exact function:

~~~js
function normalizeState(value) {
  const tasks = Array.isArray(value?.tasks)
    ? value.tasks
        .filter((task) => task && typeof task.id === "string" && typeof task.title === "string")
        .map((task) => ({
          id: task.id,
          title: task.title.slice(0, 120),
          completed: Boolean(task.completed),
          createdAt: Number(task.createdAt) || Date.now()
        }))
    : [];

  const sessions = Array.isArray(value?.sessions)
    ? value.sessions
        .filter((session) => session && typeof session.id === "string" && typeof session.taskId === "string")
        .map((session) => ({
          id: session.id,
          taskId: session.taskId,
          startedAt: Number(session.startedAt) || Date.now(),
          endedAt: Number(session.endedAt) || Date.now(),
          durationMs: Math.max(0, Number(session.durationMs) || 0)
        }))
    : [];

  const activeTimer = value?.activeTimer && typeof value.activeTimer.taskId === "string"
    ? { taskId: value.activeTimer.taskId, startedAt: Number(value.activeTimer.startedAt) || Date.now() }
    : null;

  return { tasks, sessions, activeTimer };
}
~~~

- [ ] Step 4: Add read and write helpers

Add these exact functions and expose them for the browser smoke check:

~~~js
function loadState() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? normalizeState(JSON.parse(saved)) : emptyState();
  } catch {
    storageMessage = "Your data could not be saved.";
    return emptyState();
  }
}

function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(appState));
    storageMessage = "";
    return true;
  } catch {
    storageMessage = "Your data could not be saved.";
    return false;
  }
}

window.loadState = loadState;
window.saveState = saveState;
appState = loadState();
~~~

- [ ] Step 5: Run the round-trip check

Run:

~~~js
appState = { tasks: [{ id: "test", title: "Test task", completed: false, createdAt: Date.now() }], sessions: [], activeTimer: null };
console.assert(saveState() === true, "saveState should succeed");
console.assert(loadState().tasks[0].title === "Test task", "saved task should load");
localStorage.removeItem("time-tracker-v1");
appState = emptyState();
~~~

Expected: every assertion passes and the test record is removed.

---

### Task 4: Add task creation, queue rendering, and completion

**Files:**
- Modify: time-tracker.html
- Test: add, reject, complete, and refresh flows

**Interfaces:**
- Consumes: appState, saveState(), and the Task 2 IDs.
- Produces: addTask(title), toggleTask(taskId), orderedTasks(), renderTasks(), and delegated task events.

- [ ] Step 1: Write the failing task-flow check

Run:

~~~js
document.querySelector("#task-input").value = "Write report";
document.querySelector("#add-task-form").requestSubmit();
console.assert(document.querySelectorAll("#task-list li").length === 1, "task should render");
~~~

Expected: the list stays empty because task creation is not wired.

- [ ] Step 2: Add task creation

Add this exact function:

~~~js
function addTask(title) {
  const trimmed = title.trim();
  if (!trimmed) {
    showMessage("Enter a task name.", "error");
    return false;
  }

  appState.tasks.push({
    id: crypto.randomUUID(),
    title: trimmed.slice(0, 120),
    completed: false,
    createdAt: Date.now()
  });
  saveState();
  return true;
}
~~~

- [ ] Step 3: Add ordering and row rendering

Add orderedTasks() with this exact ordering rule:

~~~js
function orderedTasks() {
  return [...appState.tasks].sort((a, b) => {
    const activeRank = (task) => appState.activeTimer?.taskId === task.id ? 0 : 1;
    const completeRank = (task) => task.completed ? 1 : 0;
    return activeRank(a) - activeRank(b) || completeRank(a) - completeRank(b) || a.createdAt - b.createdAt;
  });
}
~~~

Render each row with a real checkbox, a text label, a status badge, and a Start timer button. Set data-task-id on the row and button. Assign data-active="true" to the active row and include the text Active in its badge.

- [ ] Step 4: Add task event delegation

Use one document listener:

~~~js
document.addEventListener("click", (event) => {
  const startButton = event.target.closest("[data-action='start']");
  const completeBox = event.target.closest("[data-action='complete']");
  if (startButton) startTimer(startButton.dataset.taskId);
  if (completeBox) toggleTask(completeBox.dataset.taskId);
});
~~~

Add the form listener:

~~~js
document.querySelector("#add-task-form").addEventListener("submit", (event) => {
  event.preventDefault();
  if (addTask(document.querySelector("#task-input").value)) {
    document.querySelector("#task-input").value = "";
    render();
  }
});
~~~

- [ ] Step 5: Add completion and render calls

Implement toggleTask(taskId) to locate the task, stop the active timer when the active task is completed, set completed = !completed, call saveState(), and call render().

- [ ] Step 6: Run the task-flow check

Add a task named Write report, add a whitespace-only task, complete Write report, refresh the page, and inspect the list.

Expected: the valid task appears, the blank task shows Enter a task name., the completed task stays saved, and the completed row appears after incomplete rows.

---

### Task 5: Add the live stopwatch and session timeline

**Files:**
- Modify: time-tracker.html
- Test: start, stop, switch, refresh, and complete-active-task flows

**Interfaces:**
- Consumes: appState, saveState(), render(), showMessage(), and task IDs.
- Produces: formatDuration(ms), formatClock(ms), finalizeActiveSession(endedAt), startTimer(taskId), stopTimer(), and the timer ticker.

- [ ] Step 1: Write the failing timer check

Run:

~~~js
document.querySelector("[data-action='start']")?.click();
console.assert(appState.activeTimer, "active timer should exist after Start timer");
~~~

Expected: the active timer remains empty because timer behavior is not wired.

- [ ] Step 2: Add duration formatters

Add these exact functions:

~~~js
function formatDuration(milliseconds) {
  const totalSeconds = Math.max(0, Math.floor(milliseconds / 1000));
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return hours + "h " + minutes + "m " + seconds + "s";
}

function formatClock(milliseconds) {
  const totalSeconds = Math.max(0, Math.floor(milliseconds / 1000));
  const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
  const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
  const seconds = String(totalSeconds % 60).padStart(2, "0");
  return hours + ":" + minutes + ":" + seconds;
}
~~~

- [ ] Step 3: Add session finalization

Add this exact function:

~~~js
function finalizeActiveSession(endedAt = Date.now()) {
  if (!appState.activeTimer) return null;
  const { taskId, startedAt } = appState.activeTimer;
  const session = {
    id: crypto.randomUUID(),
    taskId,
    startedAt,
    endedAt,
    durationMs: Math.max(0, endedAt - startedAt)
  };
  appState.sessions.push(session);
  appState.activeTimer = null;
  return session;
}
~~~

- [ ] Step 4: Add start, stop, and ticker logic

Starting a different task must call finalizeActiveSession() before creating the new activeTimer. Stopping the timer must call finalizeActiveSession(), saveState(), and render().

Use one interval while a timer runs:

~~~js
let tickHandle = null;

function syncTicker() {
  if (appState.activeTimer && !tickHandle) {
    tickHandle = window.setInterval(renderTimer, 1000);
  }
  if (!appState.activeTimer && tickHandle) {
    window.clearInterval(tickHandle);
    tickHandle = null;
  }
}
~~~

renderTimer() must derive elapsed time from Date.now() - appState.activeTimer.startedAt, update timer-display, update timer-action between Start timer and Stop timer, and keep aria-live="polite" on the display.

- [ ] Step 5: Render saved sessions

Render appState.sessions in reverse chronological order inside activity-list. Each li must use the daisyUI timeline structure with timeline-start, timeline-middle, and timeline-end. Resolve the task title from taskId; use Deleted task when the task no longer exists.

- [ ] Step 6: Run the timer-flow check

Start a task, wait for the display to change, stop it, start a second task, refresh the page while the second timer runs, and complete the active task.

Expected: the first session appears in Activity, the second timer resumes after refresh, and completing the active task saves its session and marks the task complete.

---

### Task 6: Add live stats, status messages, and clear-day behavior

**Files:**
- Modify: time-tracker.html
- Test: totals, errors, and reset confirmation

**Interfaces:**
- Consumes: appState, storageMessage, formatDuration(), and finalizeActiveSession().
- Produces: showMessage(message, type), renderStats(), renderTodayLabel(), and the clear-day action.

- [ ] Step 1: Write the failing stats check

Run:

~~~js
console.assert(document.querySelector("#stats-time").textContent !== "", "tracked time should render");
console.assert(document.querySelector("#stats-completed").textContent !== "", "completed count should render");
~~~

Expected: the values remain blank because derived stats are not wired.

- [ ] Step 2: Add the status renderer

Implement showMessage(message, type = "info") so it sets the text of app-status, toggles hidden, and applies alert-error when type === "error". Keep the success path quiet after normal actions.

- [ ] Step 3: Add stats rendering

Compute tracked time from saved sessions plus the active elapsed time. Compute completed tasks from appState.tasks. Write the results into stats-time and stats-completed. Use formatDuration() for the tracked time.

- [ ] Step 4: Add the date label

Render today’s date with Intl.DateTimeFormat(undefined, { dateStyle: "full" }) into today-label.

- [ ] Step 5: Add clear-day behavior

Wire the button with this exact confirmation text:

~~~js
document.querySelector("#clear-day").addEventListener("click", () => {
  if (!window.confirm("Clear all tasks and sessions?")) return;
  appState = emptyState();
  saveState();
  render();
});
~~~

- [ ] Step 6: Render storage errors

After loadState() and every saveState(), call showMessage(storageMessage, "error") when storageMessage has a value.

- [ ] Step 7: Run the stats and reset check

Create one task, track time, stop it, complete it, inspect stats, click Clear day, cancel once, then confirm once.

Expected: tracked time and completed count update, cancel preserves data, and confirmation clears tasks, sessions, timer state, and totals.

---

### Task 7: Finish accessibility, responsive polish, and copy review

**Files:**
- Modify: time-tracker.html
- Test: keyboard and viewport checks

**Interfaces:**
- Consumes: the complete markup and render functions from Tasks 1 through 6.
- Produces: final semantic labels, focus treatment, responsive behavior, and direct interface copy.

- [ ] Step 1: Run the failing accessibility checklist

Check the page with the keyboard and record each missing result:

~~~text
Tab reaches the task input.
Enter submits a task.
Tab reaches every visible button.
Focus remains visible.
The timer has aria-live="polite".
The status region has role="status" and aria-live="polite".
Every icon-only button has an aria-label.
~~~

Expected: at least the timer and status requirements fail until the final markup is applied.

- [ ] Step 2: Add accessible labels and live regions

Keep a visible label for the task input, add aria-live="polite" to timer-display, add aria-pressed="true" to the active timer control when the timer runs, and give every icon-only control an aria-label.

- [ ] Step 3: Add the final custom CSS

Keep custom CSS limited to this exact set of concerns:

~~~css
body {
  min-height: 100vh;
}

.timer-digits {
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.06em;
}

.task-title {
  overflow-wrap: anywhere;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
~~~

- [ ] Step 4: Check responsive layout

Inspect the page at 1440 x 900 and 390 x 844.

Expected: the desktop view shows the timer beside Today, the mobile view stacks timer, Today, stats, and Activity, and long task titles wrap without horizontal scrolling.

- [ ] Step 5: Scan interface copy

Run:

~~~bash
rg -n "—|seamless|effortless|unlock|supercharge|revolutionize|leverage|productivity|robust|powerful|delve" time-tracker.html || true
~~~

Expected: no matches. Keep these exact action labels: Start timer, Stop timer, Add task, Clear day, and Enter a task name.

---

### Task 8: Run the final verification and scorecards

**Files:**
- Modify: time-tracker.html only when a verification check fails.
- Test: browser smoke test, responsive inspection, accessibility checklist, copy scan

**Interfaces:**
- Consumes: the complete page from Tasks 1 through 7.
- Produces: a verified time-tracker.html and final scorecards for accessibility, performance, theming, responsive behavior, anti-patterns, and copy.

- [ ] Step 1: Serve the file over HTTP

Run from the workspace:

~~~bash
python3 -m http.server 4173
~~~

Open http://127.0.0.1:4173/time-tracker.html in a Chromium browser.

- [ ] Step 2: Run the core functional checklist

Verify these exact cases:

~~~text
1. Load with an empty browser key.
2. Add “Prepare weekly report” with Enter.
3. Submit a blank task and see “Enter a task name.”.
4. Start the report timer and watch the seconds change.
5. Start “Review inbox” and see the report session move to Activity.
6. Refresh while “Review inbox” runs and confirm the timer resumes.
7. Complete the active task and confirm its session saves.
8. Refresh and confirm tasks, sessions, totals, and completion state persist.
9. Click Clear day, cancel, and confirm that data remains.
10. Click Clear day again, confirm, and verify the empty state returns.
~~~

- [ ] Step 3: Run the accessibility checklist

Use the keyboard for the add, start, stop, complete, and clear flows. Confirm visible focus, accessible button names, heading order, live regions, and readable contrast.

- [ ] Step 4: Stress-test realistic content

Add a 120-character task title and confirm it wraps. Add several tasks and confirm active, incomplete, and completed ordering. Start and stop sessions with short durations and confirm the timeline remains readable.

- [ ] Step 5: Run the copy scan

Repeat the rg scan from Task 7 and read every visible string in the rendered page. Remove any filler, vague claim, adverb, jargon, or em dash.

- [ ] Step 6: Score the finished page

Record one 0 to 4 score for each Impeccable dimension:

~~~text
Accessibility: 0 to 4
Performance: 0 to 4
Theming: 0 to 4
Responsive: 0 to 4
Anti-patterns: 0 to 4
~~~

Fix every dimension scored 0, 1, or 2, then score it again. Record Stop Slop copy scores from 1 to 10 for Directness, Rhythm, Trust, Authenticity, and Density. Revise any total below 35/50.

## Plan self-review

- Spec coverage: Tasks 1 and 2 cover the page structure and daisyUI surfaces. Tasks 3 through 6 cover state, persistence, task actions, timer actions, sessions, errors, stats, and reset. Task 7 covers accessibility, responsiveness, and copy. Task 8 covers final verification and scorecards.
- Placeholder scan: no placeholder instructions remain.
- Interface consistency: all tasks use appState, STORAGE_KEY, loadState(), saveState(), render(), showMessage(), startTimer(), stopTimer(), and the IDs defined in Task 1.
- Scope: the plan creates one HTML file and keeps excluded features out of the implementation.

