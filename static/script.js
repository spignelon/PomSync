async function updateStatus() {
    try {
        let response = await fetch('/status');
        let data = await response.json();

        if (!data.active) {
            document.getElementById("status").innerText = "No active session.";
            document.getElementById("timer").innerText = "00:00";
        } else {
            document.getElementById("status").innerText = `Current Phase: ${data.phase.toUpperCase()}`;
            let minutes = Math.floor(data.remaining_time / 60);
            let seconds = data.remaining_time % 60;
            document.getElementById("timer").innerText = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        }
    } catch (error) {
        console.error("Error fetching status:", error);
    }
}

async function startSession(mode) {
    try {
        let response = await fetch('/start', {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mode: mode })
        });

        let result = await response.json();
        console.log(result);
    } catch (error) {
        console.error("Error starting session:", error);
    }
}

async function resetSession() {
    await fetch('/reset', { method: "POST" });
}

setInterval(updateStatus, 1000);
