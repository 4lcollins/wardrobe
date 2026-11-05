(() => {
  const dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  const hourHeight = 48;
  const snapMinutes = 30;
  let calendarState;
  let activeEditor;

  const toMinutes = (hour) => Math.round(Number(hour) * 60);
  const toHour = (minutes) => minutes / 60;
  const formatTime = (minutes) => {
    const hour = Math.floor(minutes / 60) % 24;
    const minute = minutes % 60;
    const period = minutes < 720 || minutes === 1440 ? "AM" : "PM";
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${String(minute).padStart(2, "0")} ${period}`;
  };

  function render(editor) {
    activeEditor = editor;
    if (!calendarState) calendarState = JSON.parse(editor.dataset.template);
    editor.innerHTML = `<div class="calendar-week">${dayNames.map((day, index) => `
      <section class="calendar-day" data-day="${index}">
        <header class="calendar-day-title">${day}<button type="button" class="calendar-add" aria-label="Add block to ${day}">+</button></header>
        <div class="calendar-track">
          ${Array.from({ length: 24 }, (_, hour) => `<div class="calendar-hour" style="top:${hour * hourHeight}px"><span>${formatTime(hour * 60)}</span></div>`).join("")}
          ${(calendarState[index] || []).map((block, blockIndex) => {
            const start = toMinutes(block.start_hour);
            const end = toMinutes(block.end_hour);
            const top = start / 60 * hourHeight;
            const height = Math.max((end - start) / 60 * hourHeight, 28);
            return `<article class="calendar-block calendar-color-${blockIndex % 4}" data-day="${index}" data-block="${blockIndex}" style="top:${top}px;height:${height}px">
              <input class="calendar-block-name" aria-label="${day} block name" value="${escapeHtml(block.name)}">
              <span class="calendar-block-time">${formatTime(start)}–${formatTime(end)}</span>
              <button type="button" class="calendar-delete" aria-label="Delete ${escapeHtml(block.name)}">×</button>
              <span class="calendar-resize" aria-label="Resize block"></span>
            </article>`;
          }).join("")}
        </div>
      </section>`).join("")}</div>`;
    publish();
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
  }

  function publish() {
    const value = JSON.stringify(calendarState);
    Shiny.setInputValue("calendar-calendar_data", value, { priority: "event" });
  }

  document.addEventListener("click", (event) => {
    const add = event.target.closest(".calendar-add");
    if (add) {
      const day = Number(add.closest(".calendar-day").dataset.day);
      calendarState[day] ||= [];
      calendarState[day].push({ name: "New block", start_hour: 9, end_hour: 10 });
      render(activeEditor);
      publish();
      return;
    }
    const remove = event.target.closest(".calendar-delete");
    if (remove) {
      const block = remove.closest(".calendar-block");
      calendarState[block.dataset.day].splice(Number(block.dataset.block), 1);
      render(activeEditor);
      publish();
    }
  });

  document.addEventListener("input", (event) => {
    if (!event.target.matches(".calendar-block-name")) return;
    const block = event.target.closest(".calendar-block");
    calendarState[block.dataset.day][Number(block.dataset.block)].name = event.target.value;
    publish();
  });

  let drag;
  document.addEventListener("pointerdown", (event) => {
    const block = event.target.closest(".calendar-block");
    if (!block || event.target.matches("input,button")) return;
    drag = {
      block,
      day: Number(block.dataset.day),
      index: Number(block.dataset.block),
      y: event.clientY,
      start: toMinutes(calendarState[block.dataset.day][Number(block.dataset.block)].start_hour),
      end: toMinutes(calendarState[block.dataset.day][Number(block.dataset.block)].end_hour),
      resize: event.target.matches(".calendar-resize"),
    };
    block.setPointerCapture(event.pointerId);
    event.preventDefault();
  });

  document.addEventListener("pointermove", (event) => {
    if (!drag) return;
    const delta = Math.round((event.clientY - drag.y) / (hourHeight / 60) / snapMinutes) * snapMinutes;
    const block = calendarState[drag.day][drag.index];
    if (drag.resize) {
      const end = Math.max(drag.start + snapMinutes, Math.min(1440, drag.end + delta));
      block.end_hour = toHour(end);
    } else {
      const duration = drag.end - drag.start;
      const start = Math.max(0, Math.min(1440 - duration, drag.start + delta));
      block.start_hour = toHour(start);
      block.end_hour = toHour(start + duration);
    }
    const start = toMinutes(block.start_hour);
    const end = toMinutes(block.end_hour);
    drag.block.style.top = `${start / 60 * hourHeight}px`;
    drag.block.style.height = `${Math.max((end - start) / 60 * hourHeight, 28)}px`;
    drag.block.querySelector(".calendar-block-time").textContent = `${formatTime(start)}–${formatTime(end)}`;
    publish();
  });
  document.addEventListener("pointerup", () => {
    if (drag) render(activeEditor);
    drag = null;
  });
  document.addEventListener("pointercancel", () => { drag = null; });

  const observer = new MutationObserver(() => {
    const editor = document.getElementById("calendar-editor");
    if (editor && editor !== activeEditor) render(editor);
  });
  observer.observe(document.body, { childList: true, subtree: true });
})();
