$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#supplier_id").val(res._id);
        $("#supplier_name").val(res.name);
        $("#supplier_category").val(res.category);
        if (res.available == true) {
            $("#supplier_available").val("true");
        } else {
            $("#supplier_available").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#supplier_name").val("");
        $("#supplier_category").val("");
        $("#supplier_available").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a supplier
    // ****************************************

    $("#create-btn").click(function () {

        let name = $("#supplier_name").val();
        let category = $("#supplier_category").val();
        let available = $("#supplier_available").val() == "true";

        let data = {
            "name": name,
            "category": category,
            "available": available
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/suppliers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a supplier
    // ****************************************

    $("#update-btn").click(function () {

        let supplier_id = $("#supplier_id").val();
        let name = $("#supplier_name").val();
        let category = $("#supplier_category").val();
        let available = $("#supplier_available").val() == "true";

        let data = {
            "name": name,
            "category": category,
            "available": available
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/suppliers/${supplier_id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a supplier
    // ****************************************

    $("#retrieve-btn").click(function () {

        let supplier_id = $("#supplier_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/suppliers/${supplier_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a supplier
    // ****************************************

    $("#delete-btn").click(function () {

        let supplier_id = $("#supplier_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/suppliers/${supplier_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("supplier has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#supplier_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a supplier
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#supplier_name").val();
        let category = $("#supplier_category").val();
        let available = $("#supplier_available").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/suppliers?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '</tr></thead><tbody>'
            let firstsupplier = "";
            for(let i = 0; i < res.length; i++) {
                let supplier = res[i];
                table +=  `<tr id="row_${i}"><td>${supplier._id}</td><td>${supplier.name}</td><td>${supplier.category}</td><td>${supplier.available}</td>`;
                if (i == 0) {
                    firstsupplier = supplier;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstsupplier != "") {
                update_form_data(firstsupplier)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})