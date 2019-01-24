// This function will add new input fields depending on the amount of ingredients the user picks. If a user changes their mind, it will remove previous input fields.
$("#number_of_ingredients").change(function() {
    $(".ingredients_remove").remove();
    var ingredients_selector = document.getElementById("number_of_ingredients");
    var ingredients_selector_value = ingredients_selector.value;

    for (var i = 0; i < ingredients_selector_value; i++) {
        $("#ingredients_fields").append("<input type='text' class='ingredients_remove' name='ingredients[" + i + "]'/>");
    }
});
// This function works the same as above, but for instructions.
$("#number_of_instructions").change(function() {
    $(".instructions_remove").remove();
    var instructions_selector = document.getElementById("number_of_instructions");
    var instructions_selector_value = instructions_selector.value;

    for (var i = 0; i < instructions_selector_value; i++) {
        $("#instructions_fields").append("<input type='text' class='instructions_remove' name='instructions[" + i + "]'/>");
    }
});
