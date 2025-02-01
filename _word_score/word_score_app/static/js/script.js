const wordScoreUrl = "/word_score/"; // Ensure this URL is correct
const taskStatusUrl = "/task-status/"; // Base URL (trailing slash)

$("#word-score-form").on("submit", function(event) {
    event.preventDefault();

    $("#result-box").show(); // Show the result box immediately
    $("#status").text("Processing..."); // Initial status message
    $("#total-occurrences").text("");
    $("#all-pages").text("");

    $.ajax({
        url: wordScoreUrl,
        type: "POST",
        data: $(this).serialize(),
        headers: {
            "X-CSRFToken": $("[name='csrfmiddlewaretoken']").val()
        },
        success: function(response) {
            console.log("Word score response:", response); // Debugging line
            if (response && response.task_id) {
                checkTaskStatus(response.task_id);
            } else {
                console.error("Task ID not received:", response);
                $("#status").text("Error: Task ID not received.");
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX error:", status, error, xhr);
            $("#status").text("AJAX Error: " + xhr.responseText);
        }
    });
});

function checkTaskStatus(taskId) {
    const url = taskStatusUrl + taskId + "/"; // Construct the full URL

    const intervalId = setInterval(function() {
        $.ajax({
            url: url,
            success: function(response) {
                console.log("Task status response:", response); // Debugging line
                if (response.status === 'success') {
                    clearInterval(intervalId); // Stop polling

                    $("#status").text("Completed!");
                    $("#total-occurrences").text("Total Occurrences: " + response.total_occurrences);

                    const pagesList = $("<ul></ul>");
                    response.all_pages.forEach(page => {
                        pagesList.append("<li>" + page + "</li>");
                    });
                    $("#all-pages").html("Pages Visited: ").append(pagesList);

                } else if (response.status === 'error') {
                    clearInterval(intervalId);
                    $("#status").text("Error: " + response.message);
                } else if (response.status === 'pending') {
                    $("#status").text("Processing... " + (response.progress ? `(${response.progress}%)` : '')); // Show progress if available
                } else {
                    clearInterval(intervalId);
                    console.error("Unexpected response:", response);
                    $("#status").text("Unexpected response received.");
                }
            },
            error: function(xhr, status, error) {
                clearInterval(intervalId);
                console.error("AJAX error:", status, error, xhr);
            }
        });
    }, 1000); // Poll every 1 second
}