document.addEventListener('DOMContentLoaded', function () {
  // Find all internal navigation links
  const links = document.querySelectorAll('a:not([target="_blank"]):not([href^="http"]):not([href^="#"])');
  const page = document.getElementById('page-transition');

  links.forEach(link => {
    link.addEventListener('click', function (e) {
      // Only animate if it's not a download or anchor
      if (
        this.hostname === window.location.hostname &&
        !this.hasAttribute('download') &&
        !this.href.includes('#')
      ) {
        e.preventDefault();
        page.classList.add('fade-out');
        setTimeout(() => {
          window.location = this.href;
        }, 500); // match CSS transition duration
      }
    });
  });

  // Fade in on page load
  page.classList.remove('fade-out');
});


