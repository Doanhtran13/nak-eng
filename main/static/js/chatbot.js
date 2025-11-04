// Robust chatbot toggle: support both id and class markup and avoid throwing
document.addEventListener("DOMContentLoaded", function () {
  const toggle =
    document.getElementById("chatbot-toggle") ||
    document.querySelector(".chatbot-button");
  const container =
    document.getElementById("chatbot-container") ||
    document.querySelector(".chatbot-container");

  if (!toggle || !container) {
    // Nothing to bind on this page
    return;
  }

  toggle.addEventListener("click", function () {
    try {
      // Prefer toggling 'active' class which is used by CSS to show the window
      if (container.classList) {
        container.classList.toggle("active");
      } else {
        // Fallback to inline display toggle
        if (
          container.style.display === "none" ||
          container.style.display === ""
        ) {
          container.style.display = "block";
        } else {
          container.style.display = "none";
        }
      }

      // Optionally load remote chat content once when opened (if endpoint exists)
      if (container.classList && container.classList.contains("active")) {
        // fetch content only if container is empty
        if (!container.innerHTML || container.innerHTML.trim().length === 0) {
          fetch("/chatbot/")
            .then((res) => res.text())
            .then((html) => {
              if (html && html.trim().length > 0) container.innerHTML = html;
            })
            .catch(() => {});
        }
      }
    } catch (err) {
      console.error("chatbot toggle error", err);
    }
  });
});
