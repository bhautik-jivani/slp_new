$('.custom-control-input').on("change",function(){
    var $checkbox = $(this).find(':checkbox');
    var status = $(this).attr('data-merchant-status')
    var statusURL = $(this).attr('data-status-url')
    var csrf = $( "input[name$='csrfmiddlewaretoken']" ).val();
    var merchant_id = $(this).attr('data-merchant-id')

    if (status == 'Unblock'){
        $.ajax({
                url: statusURL,
                type:'post',
                data: {
                    'status': status,
                    'id':merchant_id,
                    'csrfmiddlewaretoken':csrf,
                },
                success: function (data) {
                    $(this).attr('data-merchant-status',data)
                }
            });
    }else{
        $.ajax({
                url: statusURL,
                type:'post',
                data: {
                    'status': status,
                    'id':merchant_id,
                    'csrfmiddlewaretoken':csrf,
                },
                success: function (data) {
                    $(this).attr('data-merchant-status',data)
                }
            });
    }

});