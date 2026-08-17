function red(text) {
    var red = '<b><span style="color:rgb(255,60,60);">' + text + '</span></b>';
    return red
}


function blue(text) {
    var blue = '<b><span style="color:rgb(0,170,255);">' + text + '</span></b>';
    return blue
}


function set_slider() {
    $('.jspsych-html-slider-response-response').slider();
    $('.ui-slider-handle').hide();

    $('.jspsych-html-slider-response-response').slider({ min: 0, max: 100 })
    $('.slider-three').slider('pips', { first: 'pip', last: 'pip', step: 50 });
    $('.slider-two').slider('pips', { first: 'pip', last: 'pip', step: 100 });

    $('.jspsych-html-slider-response-response').slider().on('slidestart', function( event, ui ) {
        $(this).find('.ui-slider-handle').show();
        if ($('.ui-slider-handle:hidden').length == 0) {
            $('#jspsych-html-slider-response-next').prop('disabled', false);
            $('#jspsych-instructions-next').prop('disabled', false);
        }
    });
}

function set_slider_resp(participantResponse) {
    $('.jspsych-html-slider-response-response').slider('value', participantResponse);
    $('.jspsych-html-slider-response-response').attr('disabled', true);
}

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  while (0 !== currentIndex) {
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

function range(start, end) {
  // includes start, excludes end
  return new Array(end - start).fill().map((d, i) => i + start);
}

function generate_trial_order(num_trials) {
    return shuffle(range(0, num_trials))
}
