window.addEventListener("load", vote_main_func);

function vote_main_func(){
    let question_rating_div = document.querySelector("#question_rating_div");
    let thumbs = document.querySelectorAll(".fa-angle-up,.fa-angle-down");
    thumbs.forEach(function(elem){
        elem.onclick = vote;
    });

    function vote(event){
        let rating_elem = event.target.parentNode.getElementsByTagName("div")[0];
        let vote_action = event.target.getAttribute("data-action-vote");
        let csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value

        let options = {
            method: 'POST',
            headers: {
                "X-CSRFToken": csrftoken,
                'Accept': 'text/plain',
                "Content-Type": "Application/json",
            },
            credentials: "same-origin"
//            credentials: "include"
        }
        fetch(vote_action, options).then(function(response){
            response.json().then(function(response_parsed){
//                console.log(response_parsed);
                if(response_parsed.result){
                    rating_elem.textContent = response_parsed.rating;
                }
            });

        });
    }
}