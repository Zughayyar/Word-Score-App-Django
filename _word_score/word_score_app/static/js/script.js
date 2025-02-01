function checkWordScore() {
    let url = document.getElementById("urlInput").value;
    let word = document.getElementById("wordInput").value;
    let resultBox = document.getElementById("resultBox");
    
    if (!url || !word) {
        resultBox.style.display = "block";
        resultBox.style.background = "#f8d7da";
        resultBox.style.color = "#721c24";
        resultBox.textContent = "Please enter both URL and word!";
        return;
    }
}

$("#word-score-form").on("submit", function(event) {
    event.preventDefault();
    $("#result-box").show();
    $("#status").text("Processing...");
    $("#total-occurrences").text("");
    $("#all-pages").text("");

    $.ajax({
        url: "{% url 'word_score' %}",
        type: "POST",
        data: $(this).serialize(),
        success: function(response) {
            checkTaskStatus(response.task_id);
        }
    });
});

function checkTaskStatus(taskId) {
    $.ajax({
        url: "/task-status/" + taskId + "/",
        success: function(response) {
            if (response.status === "pending") {
                setTimeout(function() {
                    checkTaskStatus(taskId);
                }, 2000);
            } else if (response.status === "success") {
                $("#status").text("Completed!");
                $("#total-occurrences").html("<strong>Total Occurrences:</strong> " + response.total_occurrences);
                $("#all-pages").html("<strong>Pages Visited:</strong> " + response.all_pages.join(", "));
            } else {
                $("#status").text("Error: " + response.message);
            }
        }
    });
}