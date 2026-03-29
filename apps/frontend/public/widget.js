(function () {
  "use strict";

  var ACCENT = "#00E5A0";
  var BG = "#0A0F1E";
  var BORDER = "rgba(0,229,160,0.18)";
  var SHADOW = "0 8px 32px rgba(0,0,0,0.45)";

  var script = document.currentScript ||
    (function () {
      var scripts = document.getElementsByTagName("script");
      return scripts[scripts.length - 1];
    })();

  var clientId = script.getAttribute("data-client") || "demo";
  var botUrl = script.src.replace(/\/widget\.js.*$/, "");

  var isOpen = false;
  var panel, button;

  function injectStyles() {
    var style = document.createElement("style");
    style.textContent =
      "#nexora-widget-btn{" +
        "position:fixed;bottom:24px;right:24px;z-index:2147483647;" +
        "width:56px;height:56px;border-radius:50%;border:none;cursor:pointer;" +
        "background:" + ACCENT + ";box-shadow:" + SHADOW + ";" +
        "display:flex;align-items:center;justify-content:center;" +
        "transition:transform 160ms ease,opacity 160ms ease;" +
      "}" +
      "#nexora-widget-btn:hover{transform:scale(1.08);opacity:0.92;}" +
      "#nexora-widget-panel{" +
        "position:fixed;bottom:92px;right:24px;z-index:2147483646;" +
        "width:380px;height:600px;max-width:calc(100vw - 48px);max-height:calc(100vh - 112px);" +
        "border-radius:20px;border:1px solid " + BORDER + ";overflow:hidden;" +
        "box-shadow:" + SHADOW + ";background:" + BG + ";" +
        "transform:scale(0.92) translateY(16px);opacity:0;" +
        "transition:transform 200ms ease,opacity 200ms ease;" +
        "pointer-events:none;" +
      "}" +
      "#nexora-widget-panel.nexora-open{" +
        "transform:scale(1) translateY(0);opacity:1;pointer-events:auto;" +
      "}" +
      "#nexora-widget-panel iframe{width:100%;height:100%;border:none;display:block;}";
    document.head.appendChild(style);
  }

  function createButton() {
    button = document.createElement("button");
    button.id = "nexora-widget-btn";
    button.setAttribute("aria-label", "Abrir asistente Nexora");
    button.innerHTML =
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" ' +
        'stroke="' + BG + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
        '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>' +
      "</svg>";
    button.addEventListener("click", toggle);
    document.body.appendChild(button);
  }

  function createPanel() {
    panel = document.createElement("div");
    panel.id = "nexora-widget-panel";
    panel.setAttribute("aria-hidden", "true");

    var iframe = document.createElement("iframe");
    iframe.src = botUrl + "?client=" + encodeURIComponent(clientId);
    iframe.setAttribute("allow", "");
    iframe.setAttribute("title", "Asistente Nexora");
    panel.appendChild(iframe);
    document.body.appendChild(panel);
  }

  function toggle() {
    isOpen = !isOpen;
    if (isOpen) {
      panel.classList.add("nexora-open");
      panel.setAttribute("aria-hidden", "false");
      button.setAttribute("aria-label", "Cerrar asistente Nexora");
      button.innerHTML =
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" ' +
          'stroke="' + BG + '" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">' +
          '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>' +
        "</svg>";
    } else {
      panel.classList.remove("nexora-open");
      panel.setAttribute("aria-hidden", "true");
      button.setAttribute("aria-label", "Abrir asistente Nexora");
      button.innerHTML =
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" ' +
          'stroke="' + BG + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
          '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>' +
        "</svg>";
    }
  }

  function init() {
    if (document.getElementById("nexora-widget-btn")) return;
    injectStyles();
    createPanel();
    createButton();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
