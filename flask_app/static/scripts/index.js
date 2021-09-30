$(document).ready(function(){
    let row = 0;
    $("#add").click(function(){
        row = row + 1;
        $("tbody").append(`<tr>
            <td><input type="text" key="custom-${row}" class="form-control"></td>
            <td><input type="text" class="form-control"></td>
            <td class='del-button'><button type="button" class="btn btn-outline btn-danger del">Delete</button></td>
        </tr>`);
    });
});

$(document).on('click', '.del', function () {
    $(this).closest('tr').remove();
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
        const elem = $(this).next().find('input');
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
                    $("#execute").text("Executed Successfully!").removeClass( "btn-info btn-danger" ).addClass( "btn-success disabled" );
                    const filename = `output-${taskid}.txt`;
                    $('#download-btn').append(`<a id='download' href="/download/${filename}" style='text-decoration: none; color: black;'>
                        <button type="button" class="btn btn-outline-success btn-execute">Download</button>
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
            $("#execute").text("Executing").removeClass( "btn-success btn-danger" ).addClass( "btn-info" );
            const status_url = request.getResponseHeader('Location');
            const taskid = request.getResponseHeader('taskid');
            update_progress(status_url, taskid);
            $("#executor-form")[0].reset();
        },error : function(result){
           $("#execute").text("Failed").removeClass( "btn-info btn-success" ).addClass( "btn-danger" );
        }
    });
})
