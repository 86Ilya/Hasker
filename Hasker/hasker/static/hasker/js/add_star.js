window.addEventListener("load", add_star_main_func);

function add_star_main_func(){

    let stars = document.querySelectorAll(".fa-star");
    stars.forEach(function(elem){
        elem.onclick = set_correct_answer;
    });

    function set_correct_answer(event){
        let star_action = event.target.getAttribute("data-action-star");
        let csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value
        let options = {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrftoken,
                'Accept': 'text/plain',
                "Content-Type": "Application/json",
            },
            credentials: "same-origin"
        }
        fetch(star_action, options).then(function(response){
            response.json().then(function(response_parsed){
                if(response_parsed.result){
                    if(response_parsed.correct == true){
                        // find old correct answer and set it to false
                        let correct_answer_star_elem = document.querySelector(".fas.fa-star");
                        if(correct_answer_star_elem){
                            correct_answer_star_elem.setAttribute("class", "far fa-star");
                            //change action
                            let action = correct_answer_star_elem.getAttribute("data-action-star").replace("remove_star", "add_star");
                            correct_answer_star_elem.setAttribute("data-action-star", action);
                        }
                        event.target.setAttribute("class", "fas fa-star");

                        //change action
                        let action = event.target.getAttribute("data-action-star").replace("add_star", "remove_star");
                        event.target.setAttribute("data-action-star", action);
                    }
                    else if(response_parsed.correct == false){
                        event.target.setAttribute("class", "far fa-star");
                        //change action
                        let action = event.target.getAttribute("data-action-star").replace("remove_star", "add_star");
                        event.target.setAttribute("data-action-star", action);
                    }
                }
            });

        });
    }
}
