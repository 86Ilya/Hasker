window.addEventListener("load", ask_question_main_func);

function ask_question_main_func(){
    // let tags_from_server = {1: 'python', 2: 'c++', 3: 'scala', 4: 'java'};
    // console.log(document.querySelector("#tags_from_server").textContent);
//    let tags_from_server = JSON.parse(document.querySelector("#tags_from_server").textContent);
    let tags_added_elem = document.querySelector("#tags_field__added");
    let tags_input_elem = document.querySelector("#tags_field__input");
    let tags_dropdown_content = document.querySelector(".dropdown-content");
    let ask_button = document.querySelector("#ask_button");
    let form = document.querySelector("#ask_form");
    let tags_field = document.querySelector(".tags_field");
    let tags_nonvisible_options = document.querySelectorAll("#id_tags option");
    let tags_added_list = [];
    let tags_from_server = {};

    for(tag_option of tags_nonvisible_options){
        console.log(tag_option);
        tags_from_server[tag_option.textContent] = tag_option.value;

    }
    console.log(tags_from_server)
    tags_input_elem.oninput = oninput_tags_input_elem;
    tags_input_elem.onkeydown = remove_last_tag; 
    ask_button.onclick = submit_form;

    tags_field.onclick = () => {
        tags_input_elem.focus();
        };

    function oninput_tags_input_elem(event){

        while (tags_dropdown_content.hasChildNodes()) {
            tags_dropdown_content.removeChild(tags_dropdown_content.lastChild);
        }
        let input_text = event.target.textContent;
        // after editing this field it can be empty
        if(input_text.length == 0){
            return;
        }
        console.log("\""+input_text+"\"");
        for (const tag_name in tags_from_server) {
            // tag_name = tags_from_server[key];
            if(tags_added_list.indexOf(tag_name) == -1 && tag_name.startsWith(input_text)){
                // add tag to dropdown list
                tag_div = document.createElement('div');
                tag_div.onclick = onclick_tag_div;
                tag_div.innerText = tag_name;
                tags_dropdown_content.appendChild(tag_div);
           }
        }
        tags_dropdown_content.style.display = 'block';
    }

    function onclick_tag_div(event){
        tag_name = event.target.innerText;

        tags_dropdown_content.style.display = 'none';
        // create tag element with attributes
        tag = document.createElement("div");
        tag.className += "d-inline badge badge-info m-2";
        tag.innerText = tag_name;
        // add element to non editable list
        tags_added_elem.appendChild(tag);
        // remove element from editable field
        tags_input_elem.innerText = "";
        // add element to user tag list
        tags_added_list.push(tag_name);
        // focus on editable field
        tags_input_elem.focus();

    }

    function remove_last_tag(event){
        key = event.keyCode;
        if(key == 8){
            if(tags_input_elem.textContent.length == 0){
                let last_user_tag_name = document.querySelector("#tags_added_elem").lastChild.innerText;
                let index_tag_element = tags_added_list.indexOf(last_user_tag_name);
                tags_added_list.splice(index_tag_element, 1);
                tags_added_elem.removeChild(tags_added_elem.lastChild);
            }
        }
    }
    
    function submit_form(){
            tags_added_list.forEach(function(value){
            let option = document.querySelector(`#id_tags option[value="${tags_from_server[value]}`)
            option.selected = true;
        });
        form.submit();
    }

}

