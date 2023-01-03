document.addEventListener(
  'DOMContentLoaded', function(e){
    console.log("DOM content is loaded.");
  }
);

const input_pass = document.getElementById('password');
const input_c_pass = document.getElementById('password_confirm');
const sbmt = document.getElementById('sbmt');
sbmt.disabled = true;
const alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
const numbers = "1234567890";
const symbols = "/*-+!@#$^&~[]";
var p = false;
var cp = false;


input_pass.addEventListener(
  'input', function(e){
    let passElement = e.target;
    var pass = passElement.value;
    validate();
    if (validate_pass(pass)) {
      passElement.classList.add('input-valid');
      passElement.classList.remove('input-invalid');
      p = true;
    } else {
      passElement.classList.remove('input-valid');
      passElement.classList.add('input-invalid');
      p = false;
    }
  }
);

input_c_pass.addEventListener(
  'input', function(e){
    let cpassElement = e.target;
    let cpass = cpassElement.value;
    var pass = input_pass.value;
    validate();
    if (cpass == pass) {
      cpassElement.classList.add('input-valid');
      cpassElement.classList.remove('input-invalid');
      cp = true;
    } else {
      cpassElement.classList.remove('input-valid');
      cpassElement.classList.add('input-invalid');
      cp = false;
    }
  }
);

function validate() {
  var pass = input_pass.value;
  var cpass = input_c_pass.value;
  if (validate_pass(pass) && pass == cpass) {
    sbmt.disabled = false;
  } else {
    sbmt.disabled = true;
  }
}

function validate_pass(pass) {
  let v1 = false;
  let v2 = false;
  let v3 = false;
  if (pass.length >= 8) {
    for (var i = 0; i < alphabet.length; i++) {
      if (pass.includes(alphabet[i].toUpperCase())) {
        v1 = true;
      }
    }
    for (var i = 0; i < numbers.length; i++) {
      if(pass.includes(numbers[i])) {
        v2 = true;
      }
    }
    for (var i = 0; i < symbols.length; i++) {
      if (pass.includes(symbols[i])) {
        v3 = true;
      }
    }
    if (v1 && v2 && v3) {
      return true;
    }
  }
  return false;
};
