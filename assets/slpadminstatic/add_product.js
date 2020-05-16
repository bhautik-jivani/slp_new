function addTechnicalPdfFile(input) {
  if (input.files && input.files[0]) {
        var tech_file_count = $('#technical_uploaded_file_count').val();

        var pdfHtml = "";
        pdfHtml += '<li id="display_tech_file_'+tech_file_count+'">';
            pdfHtml += '<div class="box">';
                pdfHtml += '<a href="javascript:void(0);" class="remove1" onclick="removeTechnicalFile('+tech_file_count+')">';
                    pdfHtml += '<i class="icofont icofont-close"></i>';
                pdfHtml += '</a>';
                pdfHtml += '<div class="icon">';
                    pdfHtml += '<i class="icofont icofont-file-pdf"></i>';
                pdfHtml += '</div>';
                pdfHtml += '<span style="display: inline-block;width: 75px;">'+input.files[0].name+'</span>';
            pdfHtml += '</div>';
        pdfHtml += '</li>';
        $('#js_uploaded_pdf').append(pdfHtml);

        var prev_file_count = tech_file_count;
        $('.technical_file_'+tech_file_count).css('display','none');
        tech_file_count++;
        var tech_input_file = '<input name="technical_datasheet_'+tech_file_count+'" id="technical_file_'+tech_file_count+'" type="file" class="custom-file-input js_technical_file  technical_file_'+tech_file_count+'" onchange="addTechnicalPdfFile(this)" accept=".pdf"/>';
        $('.technical_file_'+prev_file_count).after(tech_input_file);
        $('#technical_uploaded_file_count').val(tech_file_count);
    }
}

function removeTechnicalFile(file_count){
    var tech_file_input = document.getElementById('technical_file_'+file_count);
    tech_file_input.remove();

    var li_display_file = document.getElementById('display_tech_file_'+file_count);
    li_display_file.remove();
}


function addGuidelinesPdfFile(input){
    if (input.files && input.files[0]) {
        var guidelines_file_count = $('#guidelines_uploaded_file_count').val();
        var pdfHtml = "";
        pdfHtml += '<li id="display_guidelines_file_'+guidelines_file_count+'">';
            pdfHtml += '<div class="box">';
                pdfHtml += '<a href="javascript:void(0);" class="remove1" onclick="removeguidelinesFile('+guidelines_file_count+')">';
                    pdfHtml += '<i class="icofont icofont-close"></i>';
                pdfHtml += '</a>';
                pdfHtml += '<div class="icon">';
                    pdfHtml += '<i class="icofont icofont-file-pdf"></i>';
                pdfHtml += '</div>';
                pdfHtml += '<span style="display: inline-block;width: 75px;">'+input.files[0].name+'</span>';
            pdfHtml += '</div>';
        pdfHtml += '</li>';
        $('#guide_file_pdf_show').append(pdfHtml);

        var prev_file_count = guidelines_file_count;
        $('.guidelines_file_'+guidelines_file_count).css('display','none');
        guidelines_file_count++;
        var tech_input_file = '<input name="application_guidelines_'+guidelines_file_count+'" id="guidelines_file_'+guidelines_file_count+'" type="file" class="custom-file-input js_guideline_file  guidelines_file_'+guidelines_file_count+'" onchange="addGuidelinesPdfFile(this)" accept=".pdf"/>';
        $('.guidelines_file_'+prev_file_count).after(tech_input_file);
        $('#guidelines_uploaded_file_count').val(guidelines_file_count);
    }
}

function removeguidelinesFile(file_count){
    var guideline_file_input = document.getElementById('guidelines_file_'+file_count);
    guideline_file_input.remove();

    var li_display_file = document.getElementById('display_guidelines_file_'+file_count);
    li_display_file.remove();
}

function addVideoFile(input){
    if (input.files && input.files[0]) {
        var video_file_count = $('#video_uploaded_file_count').val();
        var pdfHtml = "";
        pdfHtml += '<li id="display_video_file_'+video_file_count+'">';
            pdfHtml += '<div class="box">';
                pdfHtml += '<a href="javascript:void(0);" class="remove1" onclick="removeVideoFile('+video_file_count+')">';
                    pdfHtml += '<i class="icofont icofont-close"></i>';
                pdfHtml += '</a>';
                pdfHtml += '<div class="icon">';
                    pdfHtml += '<i class="icofont icofont-video"></i>';
                pdfHtml += '</div>';
                pdfHtml += '<span style="display: inline-block;width: 75px;">'+input.files[0].name+'</span>';
            pdfHtml += '</div>';
        pdfHtml += '</li>';
        $('#guide_file_pdf_show').append(pdfHtml);        
    }
}
