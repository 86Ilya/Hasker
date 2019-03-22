window.addEventListener("load", submit_form_func);

function submit_form_func(){

  let submit_button = document.getElementById("submit_button");
  submit_button.onclick = submit_data;

}

function submit_data(event){
  let password1 = document.getElementById("id_password").value;
  let password2 = document.getElementById("id_password_again").value;
  let result = document.getElementById("pre_submit");
  let form = document.querySelector('form[enctype="multipart/form-data"]');
  if(password1.length > 0 && password2.length > 0){
    if(password1 === password2){
      result.innerText = "Ok";
      form.submit();
    } else {

      result.innerText = "New passwords mismatch";
      setTimeout(()=>{
        result.innerText = '';
        result.removeAttribute("class");
      }, 3000);
      result.setAttribute("class", "failed_animation");


    }
  }
}
