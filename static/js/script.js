
// This function will add new input fields depending on the amount of ingredients the user picks. If a user changes their mind, it will remove previous input fields.
$("#number_of_ingredients").change(function() {
    $(".ingredients_remove").remove();
    $(".label_remove").remove();
    
    var ingredients_selector = document.getElementById("number_of_ingredients");
    var ingredients_selector_value = ingredients_selector.value;

    for (var i = 0; i < ingredients_selector_value; i++) {
        $("#ingredients_fields").append("<input type='text' class='ingredients_remove' name='ingredients[" + i + "]' id='ingredients[" + i + "]'/>");
        $("#ingredients_fields").append("<label for='ingredients[" + i + "]' class='label_remove' >Ingredient " + (i + 1) + "</label>");
    }
});

// This function works the same as above, but for instructions.
$("#number_of_instructions").change(function() {
    $(".instructions_remove").remove();
    $(".instructions_label_remove").remove();
    
    var instructions_selector = document.getElementById("number_of_instructions");
    var instructions_selector_value = instructions_selector.value;

    for (var i = 0; i < instructions_selector_value; i++) {
        $("#instructions_fields").append("<input type='text' class='instructions_remove' name='instructions[" + i + "]'/ required>");
        $("#instructions_fields").append("<label for='instructions[" + i + "]' class='instructions_label_remove' required>Instructions " + (i + 1) + "</label>");
    }
});

// FOR MATERIALIZE

// Modal
$(document).ready(function(){
    $('.modal').modal();
});
  
// Select
$(document).ready(function(){
    $('select').formSelect();
});

$('.dropdown-trigger').dropdown();

// Carousel
$(document).ready(function(){
    $('.carousel').carousel();
  });
 
 //Sidenav
 $(document).ready(function(){
    $('.sidenav').sidenav();
  });
  
  //Collapsible for Mobile
  $(document).ready(function(){
    $('.collapsible').collapsible();
  });