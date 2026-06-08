window.addEventListener("scroll", () => {
    document.querySelectorAll(".section").forEach(sec => {
        if (sec.getBoundingClientRect().top < window.innerHeight - 100) {
            sec.classList.add("show");
        }
    });
});
