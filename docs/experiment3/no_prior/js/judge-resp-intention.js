/**
 * a jspsych plugin for responsibility + intention judgments
 *
 */


jsPsych.plugins['judge-resp-intention'] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'judge-resp-intention',
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
      outcome: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Outcome',
        default: ' ',
        description: '',
      }
    }
  }

  plugin.trial = function(display_element, trial) {

    var html = '<div id="jspsych-html-slider-response-wrapper">';
    html += '<div id="jspsych-html-slider-response-stimulus">';

    // display gif of t1 while answering questions about t2
    if (trial.trial == 0) {
      html += '<h3 style="margin-bottom: -10px;"> Example </h3> <p> Player A: ' + red(ex_red_name) + ', Player B: ' + blue(ex_blue_name) + '</p>';
      html += '<img src="trials/' + trial.trial + '/full.gif"></img>';
    } else {
      html += '<h3 style="margin-bottom: -10px;">' + trial.title + '</h3><p style="margin-bottom: -10px;">' + trial.footer + '</p>';
      html += '<div style="display: flex; justify-content: center;"><img src="trials/' 
            + trial.trial + '/t2/full.gif" style="flex: 1; max-width: 58%; height: auto;"></div>';
    }
  
    // intention inference slider
    var slider_width = 500;
    var slider_labels = ['definitely a hinderer',
                         'unsure',
                         'definitely a helper']
    var button_label = 'Continue';

    if (trial.trial == 0) {
      html += '<div style="margin-top: 1.5em; margin-bottom: 0.6em; font-size: 90%"><p>Now that you have seen this trial, do you think ' + blue(trial.blue_name) + ' is a hinderer or a helper?</p></div>';
    }
    else {
      html += '<div style="margin-top: 1.5em; margin-bottom: 0.6em; font-size: 90%"><p>Now that you have seen this trial, do you think <b><span style="color:rgb' + trial.blue_display + ';">' + trial.blue_name + '</span></b> is a hinderer or a helper?</p></div>';
    }

    // add slider response
    html += '<div class="jspsych-html-slider-response-container"' +
        'style="position:relative; margin: 0 auto 3em auto; width:' + 
        slider_width + 'px;">';
    html += '<div style="width: 100%;" class="jspsych-html-slider-' +
        'response-response slider-three"';
    html += 'id = "jspsych-html-slider-response-response-0"></div>';
    html += '<div>';
    for(var j=0; j < slider_labels.length; j++){
      var width = 100/(slider_labels.length-1);
      var left_offset = (j * (100 /(slider_labels.length - 1))) - (width/2);
      html += '<div style="display: inline-block; position: absolute; left:' + 
        left_offset + '%; text-align: center; width: ' + width + '%;' +
        'margin-top: 0.6em; line-height: 1em;"> <span style="text-align:' +
        'center; font-size: 70%; margin-bottom: 2em">' + slider_labels[j] + '</span> </div>';
    }

    html += '</div>'; 
    html += '</div>';
    html += '</div>';
    html += '<div style="margin-bottom: 2em;"></div>';

    // responsibility judgment slider
    var slider_width = 500;
    var slider_labels = ['not at all', 'very much'];
    var button_label = 'Continue';

    if (trial.trial == 0) {
      var names = [red(trial.red_name), blue(trial.blue_name)]
    } else {
      var names = ['<b><span style="color:rgb' + trial.red_display + ';">' + trial.red_name + '</span></b>',
                '<b><span style="color:rgb' + trial.blue_display + ';">' + trial.blue_name + '</span></b>'];
    }
    

    for(var i = 0; i < names.length; i++) {
      html += '<div style="margin-top: 3em; margin-bottom: 0.6em; font-size: 90%"><p>How responsible was ' + names[i] + ' for the ' + trial.outcome + '?</p></div>';
      html += '<div class="jspsych-html-slider-response-container"' +
        'style="position:relative; margin: 0 auto 3em auto; width:' + 
        slider_width + 'px;">';
      html += '<div style="width: 100%;" class="jspsych-html-slider' +
        '-response-response slider-two"';
      html += 'id = "jspsych-html-slider-response-response-' + (i + 1) + '"></div>';

      html += '<div>';
      for(var j = 0; j < slider_labels.length; j++){
        var width = 100/(slider_labels.length-1);
        var left_offset = (j * (100 /(slider_labels.length - 1))) - (width/2);
        html += '<div style="display: inline-block; position: absolute; left:'+left_offset+'%; text-align: center; width: '+width+'%; margin-top: 0.6em;">';
        html += '<span style="text-align: center; font-size: 70%; margin-bottom: 1.5em">'+slider_labels[j]+'</span>';
        html += '</div>';
      }

      html += '</div>';
      html += '</div>';
    }

    // html += '<div style="margin-bottom: 1em;"></div>';

    // add submit button
    html += '<button id="jspsych-html-slider-response-next" style="margin: 0 1em 1em 1em;" class="jspsych-btn" disabled>'+button_label+'</button>';

    display_element.innerHTML = html;

    var response = {};
    
    set_slider();

    display_element.querySelector('#jspsych-html-slider-response-next').addEventListener('click', function() {
      for(var i = 0; i < names.length + 1; i++) {
        response[i] = $('#jspsych-html-slider-response-response-'+i).slider('option', 'value');
      }
      end_trial();
    });

    function end_trial(){

      jsPsych.pluginAPI.clearAllTimeouts();

      // save data
      var trialdata = {
        "trial": trial.trial,
        "int_t2": response[0],
        "resp_red": response[1],
        "resp_blue": response[2]
      };

      display_element.innerHTML = '';

      // next trial
      jsPsych.finishTrial(trialdata);
    }

  };

  return plugin;
})();
