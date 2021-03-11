/* Javascript for AkidzonXBlock. */
function AkidzonXBlock(runtime, element) {

    function imgCounting() {
        var src = $(this).attr("src");
        // Check the beginning of the src attribute
        // Modify the src attribute based upon the state var we just set
        if (src.indexOf("_bw.png") == -1) {
            src = src.replace('.png', '_bw.png');
            // $(this).css('background-color', 'gray');
            count_index = count_index + parseInt($("#skipcounting").val());
            tag_img = '<img src = "{% static "/akidzon_icons/counting_index/countingindex_count_index.png" %}" style = "position: relative; top: -70px; left: 20px; z-index: 2;" >'.replace('count_index', count_index);
            $(this).parents('td').append(tag_img)
        }
        $(this).attr("src", src);
    }

    var handlerSubmitUrl = runtime.handlerUrl(element, 'submit_user_answer');
    var handlerSelectQuestionUrl = runtime.handlerUrl(element, 'select_question_link');
    var handlerSelectCategoryUrl = runtime.handlerUrl(element, 'select_category_link');

    function success_load(data) {
        debugger
        $("#questions_answered").html(data.questions_answered);
        $("#scores").html(data.scores);
        $("#questionbody").html(data.questionbody);
        $("#question_id").html(data.question_id);
        $("#question_list_html").html(data.question_list_html);
        $("#answer").val('');
    }
    function save_and_load_question(e, url_handler){
        debugger;
        e.preventDefault();
        count_index = 0;
        let standard_answers = {};
        let user_answers = {};
        let items = $(".form_to_be_checked");
        let correct_points = 0;
        let total_points = items.length;
        for (item of items) {
            let item_id = item.attributes['id'].value;
            standard_answers[item_id] = item.attributes['value_to_check'].value;
            if(item.hasAttribute('eval_method') & item.attributes.getNamedItem('eval_method') !=null){
                 tmp_answer = eval(item.attributes['eval_method'].value.trim());
                 user_answers[item_id] = tmp_answer.trim();
            }
            else if (item.type == 'checkbox') {
                user_answers[item_id] = item.checked.toString();
            } else if (item.type == 'number') {
                user_answers[item_id] = item.value.trim();
            } else if (item.type == 'text') {
                let entered_value = item.value.trim().replace(/\s/g, '');
                user_answers[item_id] = entered_value;
            } else if (item.tagName == 'LI') {
                let nodes = Array.from(item.closest('ul').children)
                user_answers[item_id] = nodes.indexOf(item);
            } else if (item.tagName == 'TD') {
                user_answers[item_id] = item.textContent.trim().replace(/\s/g, '');
                if (item.hasAttribute('cell_checked')) {
                    user_answers[item_id] = item.attributes['cell_checked'].value.trim();
                }else{
                    user_answers[item_id] = item.textContent.trim();
                }
            }
        }
        // Check whether answe to the question is corrected
        $.ajax({
            url: url_handler,
            type: 'POST',
            data: JSON.stringify({
                "scores": $('#scores').text(),
                'questions_answered': $('#questions_answered').text(),
                'category_id': $('#category_id').text(),
                'standard_answers': standard_answers,
                'user_answers': user_answers,
                'show_answers': e.target.dataset['show_answers'],
                "question_id": e.target.dataset['question_id'],
                "new_category_id": e.target.dataset['category_id']
            }),
            success: success_load
        })
    }

    $(function ($) {
        $('img.counting_picture').bind("click", imgCounting);
        $('#question_list_html').on('click', '.XAkidzonQuestionLink', function (e) {
            save_and_load_question(e, handlerSelectQuestionUrl);
        });

        $('#category_list_html').on('click', '.XAkidzonCategoryLink', function (e) {
            save_and_load_question(e, handlerSelectCategoryUrl);
        });

        $("#submit_answer_btn,#show_answer_btn").click(function(e){
            save_and_load_question(e, handlerSubmitUrl);
        });
    });
}
