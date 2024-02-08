$(document).ready(function () {
    $("#searchInput").on("input", function () {
        var searchTerm = $(this).val().toLowerCase();

        $(".order-row").each(function () {
            var date = $(this).find("td:eq(1)").text().toLowerCase();
            var status = $(this).find("td:eq(2)").text().toLowerCase();
            var employee = $(this).find("td:eq(3)").text().toLowerCase();
            var product = $(this).find("td:eq(4)").text().toLowerCase();
            var comment = $(this).find("td:eq(5)").text().toLowerCase();
            var office = $(this).find("td:eq(6)").text().toLowerCase();
            var hidden = $(this).find(".hidden-checkbox").prop("checked");

            if ((date.includes(searchTerm) || status.includes(searchTerm) || employee.includes(searchTerm) || product.includes(searchTerm) || comment.includes(searchTerm) || office.includes(searchTerm)) && (!hidden || (hidden && searchTerm === "false"))) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});
