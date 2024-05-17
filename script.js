document.addEventListener("DOMContentLoaded", function() {
    const messages = ["Join the Discord", "Follow my TikTok", "Follow my Twitch"]; // Array of messages
    const bubble = document.querySelector('.bubble'); // Select the bubble element
    const circle = bubble.querySelector('.circle'); // Select the circle element inside the bubble
    const messageContainer = circle.querySelector('.message'); // Select the message container inside the circle
  
    function getRandomMessage() {
      return messages[Math.floor(Math.random() * messages.length)]; // Get random message from the array
    }
  
    function updateMessage() {
      circle.classList.add('oval');
      circle.style.transform = 'translateX(-50%)'; // Slide out to the left
      setTimeout(() => {
        messageContainer.textContent = getRandomMessage(); // Update bubble text content with random message
        circle.classList.remove('oval');
        circle.style.transform = 'translateX(0)'; // Slide back to original position
      }, 5000);
    }
  
    // Initial message update
    updateMessage();
  
    // Update message every 7 seconds
    setInterval(updateMessage, 7000);
  });



  //-----------------------------------------------------------