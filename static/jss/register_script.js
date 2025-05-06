document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("carbon-form");
    const resultDiv = document.getElementById("result");
    const chatbotButton = document.getElementById("chatbot-button");
    const chatbotBox = document.getElementById("chatbot-box");

    // Form gönderme
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(form);
            const payload = new URLSearchParams();

            for (const pair of formData) {
                payload.append(pair[0], pair[1]);
            }

            const response = await fetch("/gemini-advice", {
                method: "POST",
                body: payload
            });

            const data = await response.json();

            if (data.advice) {
                resultDiv.innerHTML = `
                    <h3>Skor: ${data.score}</h3>
                    <pre>${JSON.stringify(data.advice, null, 2)}</pre>
                `;
            } else {
                resultDiv.innerHTML = "<p>Hata oluştu.</p>";
            }
        });
    }

    // Navbar butonları
    const navButtons = document.querySelectorAll(".nav-btn");
    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.getAttribute("data-target");
            document.querySelectorAll(".section").forEach(sec => sec.style.display = "none");
            document.getElementById(target).style.display = "block";
        });
    });

    // Chatbot göster/gizle
    if (chatbotButton && chatbotBox) {
        chatbotButton.addEventListener("click", () => {
            chatbotBox.classList.toggle("hidden");
        });
    }
});
