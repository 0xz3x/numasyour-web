document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.querySelector(".menu-toggle");
  const navMenu = document.querySelector(".nav-menu");
  const navOverlay = document.querySelector(".nav-overlay");
  const backToTop = document.querySelector(".back-to-top");
  const cookieBanner = document.querySelector(".cookie-banner");
  const acceptCookies = document.getElementById("accept-cookies");
  const refuseCookies = document.getElementById("refuse-cookies");
  const navItems = document.querySelectorAll(".nav-item");

  const toggleMenu = () => {
    navMenu?.classList.toggle("open");
    navOverlay?.classList.toggle("show");
    document.body.style.overflow = navMenu?.classList.contains("open") ? "hidden" : "";
  };

  menuToggle?.addEventListener("click", toggleMenu);
  navOverlay?.addEventListener("click", toggleMenu);

  navItems.forEach((item) => {
    const trigger = item.querySelector(".has-dropdown");
    trigger?.addEventListener("click", (event) => {
      if (window.innerWidth <= 1100) {
        event.preventDefault();
        item.classList.toggle("open");
      }
    });
  });

  const updateBackToTop = () => {
    backToTop?.classList.toggle("show", window.scrollY > 300);
  };

  backToTop?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  window.addEventListener("scroll", updateBackToTop);
  updateBackToTop();

  const revealElements = document.querySelectorAll(".reveal");
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealElements.forEach((element) => revealObserver.observe(element));

  const counters = document.querySelectorAll(".counter");
  const countObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const element = entry.target;
      const target = Number(element.dataset.target || 0);
      const suffix = element.dataset.suffix || "";
      const duration = 900;
      const start = performance.now();

      const tick = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const value = Math.round(target * (1 - Math.pow(1 - progress, 3)));
        element.textContent = `${value}${suffix}`;
        if (progress < 1) {
          requestAnimationFrame(tick);
        }
      };

      requestAnimationFrame(tick);
      countObserver.unobserve(element);
    });
  }, { threshold: 0.45 });
  counters.forEach((element) => countObserver.observe(element));

  const cookieChoice = localStorage.getItem("cookie_consent");
  if (cookieBanner && !cookieChoice) {
    cookieBanner.classList.add("show");
  }

  acceptCookies?.addEventListener("click", () => {
    localStorage.setItem("cookie_consent", "accepted");
    cookieBanner?.classList.remove("show");
  });

  refuseCookies?.addEventListener("click", () => {
    localStorage.setItem("cookie_consent", "refused");
    cookieBanner?.classList.remove("show");
  });
});
