/**
 * a jspsych plugin for slider question judging what red should do in the next trial
 *
 */


jsPsych.plugins['judge-next'] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'judge-next',
    description: '',
    parameters: {
      trial: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name: 'Trial',
        default: null,
        description: 'Trial number'
      },
      title: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Title',
        default: ' ',
        description: '',
      },
      footer: {
        type: jsPsych.plugins.parameterType.HTMl_STRING,
        pretty_name: 'Footer',
        default: '',
        description: 'Content to display below main content, before nav buttons.'
      },
      red_name: {
          type: jsPsych.plugins.parameterType.STRING,
          pretty_name: 'Red Name',
          default: ' ',
          description: 'Name of red player',
      },
      blue_name: {
          type: jsPsych.plugins.parameterType.STRING,
          pretty_name: 'Blue Name',
          default: ' ',
          description: 'Name of blue player',
      },
      red_display: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Red Display',
        default: ' ',
        description: '',
      },
      blue_display: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Blue Display',
        default: ' ',
        description: '',
      },
    }
  }

  plugin.trial = function(display_element, trial) {

      var slider_width = 500;
      var slider_labels = ['do the same thing',
                           'try something different'];
      var button_label = 'Continue';

      var html = '<div id="jspsych-html-slider-response-wrapper">';
      html += '<div id="jspsych-html-slider-response-stimulus">';

      // display t1 gif while answering the question
      html += '</h3><p style="margin-bottom: -10px;">' + trial.footer + '</p>';
      html += '<h4> Round 1 </h4>';
      html += '<img src="trials/' + trial.trial + '/t1/full.gif"></img>';

      // add question about round 2
      html += '<p> Now that you have seen this trial, what do you think <b><span style="color:rgb' + trial.red_display + ';">' + trial.red_name + '</span></b> should do in Round 2?</p></div>';

      // add slider response
      html += '<div class="jspsych-html-slider-response-container"' +
          'style="position:relative; margin: 0 auto 3em auto; width:' + 
          slider_width + 'px;">';
      html += '<div style="width: 100%;" class="jspsych-html-slider-' +
          'response-response slider-two"></div>';
      html += '<div>';

      for(var j=0; j < slider_labels.length; j++){
        var width = 100/(slider_labels.length-1);
        var left_offset = (j * (100 /(slider_labels.length - 1))) - (width/2);
        html += '<div style="display: inline-block; position: absolute; left:' + 
          left_offset + '%; text-align: center; width: ' + width + '%;' +
          'margin-top: 0.4em; line-height: 1em;"> <span style="text-align:' +
          'center; font-size: 80%;">' + slider_labels[j] + '</span> </div>';
      }
      html += '</div>';
      html += '</div>'; // for response container
      html += '</div>'; // for response wrapper

      html += '<p style="margin-top: 70px; margin-bottom: -10px;"> Click Continue to see what happens in Round 2. </p> </div>';

      // add submit button
      html += '<button id="jspsych-html-slider-response-next" style="margin:' +
        '2em 1em 3em 1em;" class="jspsych-btn" disabled>' + button_label +
        '</button>';

      display_element.innerHTML = html;

      var response = {};

      set_slider();

      display_element.querySelector('#jspsych-html-slider-response-next').addEventListener('click', function() {
        response.slider = $('.jspsych-html-slider-response-response').slider('option', 'value');
        end_trial();
      });


      function end_trial(){

        jsPsych.pluginAPI.clearAllTimeouts();

        // save data
        var trialdata = {
          "trial": trial.trial,
          "judge_t1": response.slider
        };

        display_element.innerHTML = '';

        // next trial
        jsPsych.finishTrial(trialdata);
      }

    };

    return plugin;
})();
