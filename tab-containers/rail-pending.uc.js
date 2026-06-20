// ==UserScript==
// @name tab-containers-rail-pending
// @description Hold expanded tab chrome through sidebar collapse delay
// @include main
// @grant none
// ==/UserScript==

(() => {
  "use strict";

  const ID = "gvrTabContainersRailPending";
  if (globalThis[ID]?.destroy) {
    globalThis[ID].destroy();
  }

  const toolbox = document.getElementById("navigator-toolbox");
  if (!toolbox) {
    return;
  }

  let timer = 0;

  const parseMs = (raw) => {
    const s = String(raw || "").trim();
    if (!s) {
      return 500;
    }
    if (s.endsWith("ms")) {
      return Math.max(0, parseFloat(s));
    }
    if (s.endsWith("s")) {
      return Math.max(0, parseFloat(s) * 1000);
    }
    const n = parseFloat(s);
    return Number.isFinite(n) ? n : 500;
  };

  const delayMs = () =>
    parseMs(getComputedStyle(toolbox).getPropertyValue("--transition-delay-fast"));

  const isExpanded = () => {
    if (toolbox.matches("[has-popup-menu='true'], [movingtab], [flash-popup]")) {
      return true;
    }
    return !!toolbox.querySelector(
      '#urlbar[open], toolbarbutton[open="true"]:not(#zen-sidepanel-button)'
    );
  };

  const clearPending = () => toolbox.removeAttribute("data-rail-pending");

  const armPending = () => {
    clearTimeout(timer);
    toolbox.setAttribute("data-rail-pending", "true");
    timer = setTimeout(clearPending, delayMs());
  };

  const onEnter = () => {
    clearTimeout(timer);
    clearPending();
  };

  const onLeave = () => {
    if (isExpanded()) {
      return;
    }
    armPending();
  };

  toolbox.addEventListener("mouseenter", onEnter);
  toolbox.addEventListener("mouseleave", onLeave);

  globalThis[ID] = {
    destroy() {
      clearTimeout(timer);
      toolbox.removeEventListener("mouseenter", onEnter);
      toolbox.removeEventListener("mouseleave", onLeave);
      clearPending();
      delete globalThis[ID];
    },
  };
})();
