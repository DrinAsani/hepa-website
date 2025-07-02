// static/js/contact.js

(function() {
  // Wait for the DOM to be ready
  document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('mainContactForm');
    if (!form) return;

    form.onsubmit = function(e) {
      e.preventDefault();

      // Grab the form values
      const name    = form.querySelector('[name="name"]').value;
      const email   = form.querySelector('[name="email"]').value;
      const message = form.querySelector('[name="message"]').value;

      // Send them to the backend
      fetch('/submit_contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, message })
      })
      .then(res => res.json())
      .then(data => {
        const msgEl = document.getElementById('formSuccessMsg');
        if (data.success) {
          // Show success message
          msgEl.textContent = data.message;
          msgEl.style.display = 'block';

          // Hide again after a few seconds
          setTimeout(() => {
            msgEl.style.display = 'none';
            form.reset();
          }, 3500);
        } else {
          alert('Something went wrong. Try again later.');
        }
      })
      .catch(err => {
        alert('Error submitting form!');
        console.error('Contact form error:', err);
      });
    };
  });
})();
