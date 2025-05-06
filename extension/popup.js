const btn = document.getElementById("summarize");
const output = document.getElementById("output");
const closeBtn = document.getElementById("close");

closeBtn.addEventListener("click", function() {
    window.close();
});

function extractVideoId(url) {
    let youtubeDomainPattern = /(?:youtube\.com|youtu\.be)/;
    if (!youtubeDomainPattern.test(url)) {
        return null;
    }

    let match = url.match(/(?:v=|\/embed\/|\/shorts\/|youtu\.be\/)([0-9A-Za-z_-]{11})/);
    return match ? match[1] : null;
}

chrome.tabs.query({ currentWindow: true, active: true }, function(tabs) {
    let currentUrl = tabs[0].url;
    let currentVideoId = extractVideoId(currentUrl);

    chrome.storage.local.get(["summary", "videoId"], (result) => {
        if (result.summary && result.videoId === currentVideoId) {
            output.innerHTML = result.summary;
        } else {
            output.innerHTML = ""; 
        }
    });
});

btn.addEventListener("click", function() {
    btn.disabled = true;
    btn.textContent = "Summarizing...";
    btn.classList.add("summarizing"); 
    chrome.tabs.query({currentWindow: true, active: true}, async function(tabs){
        let url = tabs[0].url;
        console.log("Active Tab URL:", tabs[0].url);

        let apiEndpoint = `https://youtube-summarize-dz8x.onrender.com/summary?url=${encodeURIComponent(url)}`;

        try{
            let response = await fetch(apiEndpoint);
            let data = await response.json();

            if (!response.ok) {
                output.innerHTML = `<p style="color: red;">Error: ${data.error || "Something went wrong. Please try again."}</p>`;
                return;
            }
            
            if (data.summary) {
                output.innerHTML = data.summary;
                chrome.storage.local.set({ summary: data.summary, videoId: data.video_id });
            } else {
                output.innerHTML = `<p style="color: red;">No summary available.</p>`;
            }
        }
        catch(error){
            console.error("Error fetching summary:", error);
            output.innerHTML = `<p style="color: red;">Failed to fetch summary. Please try again.</p>`;
        }
        finally {
            btn.disabled = false;
            btn.textContent = "Summarize";
            btn.classList.remove("summarizing");
        }
    });
});
