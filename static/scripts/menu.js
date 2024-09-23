document.addEventListener('DOMContentLoaded', function() {
  const userIcon = document.getElementById('userIcon');
  const menu = document.getElementById('menu');

  userIcon.addEventListener('mouseover', function() {
      menu.style.display = 'block';
      userIcon.style.fontWeight = 600;
  });

  userIcon.addEventListener('mouseout', function() {
      setTimeout(function() {
          if (!menu.matches(':hover')) {
              menu.style.display = 'none';
          }
      }, 300);
  });

  menu.addEventListener('mouseleave', function() {
      menu.style.display = 'none';
      userIcon.style.fontWeight = 300;
  });

  // Add event listener for the toggle button
  document.getElementById('pause').addEventListener('click', toggleVideo);
});