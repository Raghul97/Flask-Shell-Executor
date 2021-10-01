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

$(document).on('click', '.cus-arg-rm', function () {
    $(this).closest('tr').remove();
});

$(document).on('click', '#reset-form', function () {
    $("#executor-form")[0].reset();
    if ($("#execute").text() != 'Executing' && !$("#execute").hasClass('btn-info')) {
        $("#download-btn").hide();
        $("#execute").text("Execute").removeClass("btn-success btn-danger btn-info disabled").addClass("btn-primary");
        $("#command-generated").text("Run.sh");
    }
    
});

$(document).on('submit', 'form', function (event) {
    event.preventDefault();
    const data = {};
    $('#server-detail').find('input').each(function() {
        if ( $(this).val() ){
            data[$(this).attr('name')] = $(this).val();
        }
    });
    $('#custom-argument').find('input').each(function() {
        if ($(this)[0].hasAttribute('key')) {
            if ( $(this).val() && $(this).closest('td').next().find('input').val() ) {
                data[$(this).val()] = $(this).closest('td').next().find('input').val();
            }
         }
    });
    $("input:checkbox:checked").each(function(){
        const elem = $(this).parent().next();
        if (elem.val()) {
            data[elem.attr("name")] = elem.val();
        }
    });
    let output = "Run.sh";
    for (const [key, value] of Object.entries(data)) {
        output +=  ` --${key} ${value}`;
    }
    data["command_generated"] = output;

    $("#command-generated").text(output);

    function update_progress(status_url, taskid) {
        $.getJSON(status_url, function(data) {
            if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
                if (data['state'] == 'SUCCESS') {
                    $("#execute").text("Executed Successfully!").removeClass("btn-info btn-danger disabled").addClass("btn-success");
                    let filename = `output-${taskid}.txt`;
                    $("#download-btn").show();
                    $("#download-btn").empty();
                    $('#download-btn').append(`<a id='download' href="/download/${filename}" style='text-decoration: none; color: black;'>
                        <button type="button" class="btn btn-outline-success btn-actions">Download</button>
                    </a>`)
                }
                else {
                    $("#execute").text("Failed").removeClass( "btn-info btn-success" ).addClass( "btn-danger" );
                }
                return
            }
            else {
                setTimeout(function() {
                    update_progress(status_url, taskid);
                }, 2000);
            }
        });
    }

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: '/form-parse',
        dataType : 'json',
        data : JSON.stringify(data),
        success : function(data, status, request) {
            $("#execute").text("Executing").removeClass( "btn-success btn-danger" ).addClass("btn-info disabled");
            const status_url = request.getResponseHeader('Location');
            const taskid = request.getResponseHeader('taskid');
            $("#download-btn").hide();
            update_progress(status_url, taskid);
        },error : function(result){
           $("#execute").text("Failed").removeClass("btn-info btn-success").addClass("btn-danger disabled");
        }
    });
})
