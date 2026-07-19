// =======================================================
// VoiceB2B Portal
// =======================================================

const phoneInput = document.getElementById("phone");
const callButton = document.getElementById("callBtn");

const statusLabel = document.getElementById("status");
const callSidLabel = document.getElementById("callSid");

const chatWindow = document.getElementById("chatWindow");

let lastMessageCount = 0;
let chatInterval = null;


// =======================================================
// Start Call
// =======================================================

callButton.addEventListener("click", async () => {

    const phone = phoneInput.value.trim();

    if (!phone) {

        alert("Enter customer mobile number.");

        return;
    }

    statusLabel.innerHTML = "Calling...";

    try {

        const response = await fetch("/api/call", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            // Change this key if your backend expects "phone"
            body: JSON.stringify({
                to_number: phone
            })

        });

        const result = await response.json();

        console.log(result);

        if (result.success) {

            statusLabel.innerHTML = "Calling";

            callSidLabel.innerHTML = result.call_sid;

            // Clear previous chat
            chatWindow.innerHTML = "";
            lastMessageCount = 0;

            // Load immediately
            loadConversation();

            // Prevent multiple timers
            if (chatInterval !== null) {
                clearInterval(chatInterval);
            }

            // Start polling
            chatInterval = setInterval(loadConversation, 2000);

        } else {

            statusLabel.innerHTML = "Failed";

            alert(result.error);
        }

    } catch (e) {

        console.error(e);

        statusLabel.innerHTML = "Error";

    }

});


// =======================================================
// Load Conversation
// =======================================================

async function loadConversation() {

    try {

        const response = await fetch("/api/chat");

        const messages = await response.json();

        if (!Array.isArray(messages))
            return;

        if (messages.length === lastMessageCount)
            return;

        lastMessageCount = messages.length;

        chatWindow.innerHTML = "";

        messages.forEach(msg => {

            const wrapper = document.createElement("div");

            wrapper.className =
                msg.role === "customer"
                    ? "message customer"
                    : "message ai";

            const bubble = document.createElement("div");

            bubble.className = "bubble";

            bubble.innerText = msg.message;

            wrapper.appendChild(bubble);

            chatWindow.appendChild(wrapper);

        });

        chatWindow.scrollTop = chatWindow.scrollHeight;

    } catch (e) {

        console.error(e);

    }

}