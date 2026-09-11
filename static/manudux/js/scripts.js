const toggleButton = document.getElementById("toggle-btn");
const sidebar = document.getElementById("sidebar");

function toggleSidebar() {
    sidebar.classList.toggle("close");
    toggleButton.classList.toggle("rotate");
    closeAllSubmenus();
}

function toggleSubmenu(button) {
    if (!button.nextElementSibling.classList.contains("show")) {
        closeAllSubmenus();
    }

    button.nextElementSibling.classList.toggle("show");
    button.classList.toggle("rotate");

    if (sidebar.classList.contains("close")) {
        sidebar.classList.toggle("close");
        toggleButton.classList.toggle("rotate");
    }
}

function closeAllSubmenus() {
    Array.from(sidebar.getElementsByClassName("show")).forEach((ul) => {
        ul.classList.remove("show");
        ul.previousElementSibling.classList.remove("rotate");
    });
}

// Mobile bottom-bar "Menu" drawer: a bottom sheet listing everything that
// doesn't fit in the fixed 5-item bar. Handles open/close, Escape, clicking
// outside, and trapping focus inside while it's open so keyboard/screen
// reader users can't tab out into the hidden page behind it.
const mobileMenuBtn = document.getElementById("mobile-menu-btn");
const mobileMenuDrawer = document.getElementById("mobile-menu-drawer");
const mobileMenuOverlay = document.getElementById("mobile-menu-overlay");
const mobileMenuClose = document.getElementById("mobile-menu-close");

function openMobileMenu() {
    mobileMenuDrawer.hidden = false;
    mobileMenuOverlay.hidden = false;
    mobileMenuBtn.setAttribute("aria-expanded", "true");
    document.body.classList.add("mobile-menu-open");
    mobileMenuClose.focus();
    document.addEventListener("keydown", handleMobileMenuKeydown);
}

function closeMobileMenu() {
    mobileMenuDrawer.hidden = true;
    mobileMenuOverlay.hidden = true;
    mobileMenuBtn.setAttribute("aria-expanded", "false");
    document.body.classList.remove("mobile-menu-open");
    document.removeEventListener("keydown", handleMobileMenuKeydown);
    mobileMenuBtn.focus();
}

function handleMobileMenuKeydown(event) {
    if (event.key === "Escape") {
        closeMobileMenu();
        return;
    }

    if (event.key !== "Tab") return;

    const focusable = mobileMenuDrawer.querySelectorAll("a[href], button:not([disabled])");
    if (!focusable.length) return;

    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
    }
}

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener("click", () => {
        if (mobileMenuDrawer.hidden) {
            openMobileMenu();
        } else {
            closeMobileMenu();
        }
    });
    mobileMenuClose.addEventListener("click", closeMobileMenu);
    mobileMenuOverlay.addEventListener("click", closeMobileMenu);
}

// Skeleton loading: every .img-skeleton wrapper starts with a shimmering
// placeholder background and its <img> hidden (see style.scss); reveal the
// image (and drop the shimmer) once it has actually finished loading, so
// slow/large photos don't pop in over broken-image icons or blank space.
document.querySelectorAll(".img-skeleton").forEach((wrapper) => {
    const img = wrapper.querySelector("img");
    if (!img) return;

    const reveal = () => wrapper.classList.add("loaded");

    if (img.complete && img.naturalWidth > 0) {
        reveal();
    } else {
        img.addEventListener("load", reveal, { once: true });
        img.addEventListener("error", reveal, { once: true });
    }
});
