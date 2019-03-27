window.addEventListener("load", search_main_func);

function search_main_func(){
    let form = document.querySelector("#form_search");
    let form_input = document.querySelector("#form_search__input");
    let form_button = document.querySelector("#form_search__button");
    form_input.onkeydown = form_submit_onkeydown;
    form_button.onclick = form_submit;

    function form_submit_onkeydown(event){
        if(event.keyCode == 13 ){
            event.preventDefault();
            form_submit();
        }
    }

    function form_submit(){
            tag_pattern = /tag:(.*)$/;
            let query = form_input.value;
            match = query.match(tag_pattern);
            if(match !== null){
                tag = match[1];
                form.action = `/tag/${tag}/`;
            }
            else{
                form.action += `${query}/`;

            }
            form.submit();
    }

}

