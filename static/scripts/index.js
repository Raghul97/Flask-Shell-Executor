// when document is ready, hide download option and set event listener for custom argument add button to add new row.
$(document).ready(function(){
    let row = 0;
    $("#download-btn").hide();
    $("#add").click(function(){
        row = row + 1;
        $("tbody").append(`<tr>
            <td><input type="text" key="custom-${row}" class="form-control"></td>
            <td><input type="text" class="form-control"></td>
            <td class='del-button'><button type="button" class="btn btn-outline btn-danger cus-arg-rm">Delete</button></td>
        </tr>`);
    });
});

// set event listener on delete button in custom argument row.
$(document).on('click', '.cus-arg-rm', function () {
    $(this).closest('tr').remove();
});

// set event listener on reset button to reset the form inputs.
$(document).on('click', '#reset-form', function () {
    $("#executor-form")[0].reset();

    // customizing the download and execute buttons when resetting form.
    if ($("#execute").text() != 'Executing' && !$("#execute").hasClass('btn-info')) {
        $("#download-btn").hide();
        $("#execute").text("Execute").removeClass("btn-success btn-danger btn-info disabled").addClass("btn-primary");
        $("#command-generated").text("Run.sh");
    }
});

// event listener on submitting the form to gather all data from input and send ajax post request.
$(document).on('submit', 'form', function (event) {
    event.preventDefault();
    const data = {};

    // collect data from server detail section.
    $('#server-detail').find('input').each(function() {
        if ( $(this).val() ){
            data[$(this).attr('name')] = $(this).val();
        }
    });

    // collect data from argument checkbox section.
    $("input:checkbox:checked").each(function(){
        const elem = $(this).parent().next();
        if (elem.val()) {
            data[elem.attr("name")] = elem.val();
        }
    });

    // collect data from custom argument section.
    $('#custom-argument').find('input').each(function() {
        if ($(this)[0].hasAttribute('key')) {
            if ( $(this).val() && $(this).closest('td').next().find('input').val() ) {
                data[$(this).val()] = $(this).closest('td').next().find('input').val();
            }
         }
    });

    // modify the content of command with the data provided in the form.
    let output = "Run.sh";
    for (const [key, value] of Object.entries(data)) {
        output +=  ` --${key} ${value}`;
    }
    data["command_generated"] = output;
    $("#command-generated").text(output);

    // get status of the task with taskid.
    function update_progress(status_url, taskid) {
        $.getJSON(status_url, function(data) {
            
            // if state of the task is success or failed, modifiy the DOM accordingly.
            if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
                if (data['state'] == 'SUCCESS') {

                    // if success, show option for downloading the file.
                    $("#execute").text("Executed Successfully!").removeClass("btn-info btn-danger disabled").addClass("btn-success");
                    let filename = `output-${taskid}.txt`;
                    $("#download-btn").show();
                    $("#download-btn").empty();
                    $('#download-btn').append(`<a id='download' href="/download/${filename}" style='text-decoration: none; color: black;'>
                        <button type="button" class="btn btn-outline-success btn-actions">Download</button>
                    </a>`)
                }
                else {
                    // if task failed, show the task is failed. 
                    $("#execute").text("Failed").removeClass( "btn-info btn-success" ).addClass( "btn-danger" );
                }
                return
            }
            // else the state is pending or progress, set time interval of 2 seconds and send request again.
            else {
                setTimeout(function() {
                    update_progress(status_url, taskid);
                }, 2000);
            }
        });
    }

    // send ajax post request with the data collected from various sections.
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/form-parse',
        dataType : 'json',
        data : JSON.stringify(data),
        success : function(data, status, request) {
            // if request sent successfully, update the buttons and check the status of the task.
            $("#execute").text("Executing").removeClass( "btn-success btn-danger" ).addClass("btn-info disabled");
            const status_url = request.getResponseHeader('Location');
            const taskid = request.getResponseHeader('taskid');
            $("#download-btn").hide();
            update_progress(status_url, taskid);
        },error : function(result){
            // if request failed, show the request is failed. 
           $("#execute").text("Failed").removeClass("btn-info btn-success").addClass("btn-danger disabled");
        }
    });
})
