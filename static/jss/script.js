document.addEventListener('DOMContentLoaded', function () {
  const toggleButton = document.querySelector('.chatbot-toggle');
  const chatbotWindow = document.querySelector('.chatbot-window');

  toggleButton.addEventListener('click', function () {
    chatbotWindow.classList.toggle('active');
  });
});