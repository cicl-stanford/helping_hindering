var judgeCounterfactual = (function (jsPsych) {
    'use strict';

    const info = {
        name: 'judge-counterfactual',
        parameters: {
            trial: {
              type: jsPsych.ParameterType.HTML_STRING,
              pretty_name: 'Trial',
              default: null,
            },
            title: {
              type: jsPsych.ParameterType.STRING,
              pretty_name: 'Title',
              default: ' ',
            },
            still: {
              type: jsPsych.ParameterType.STRING,
              pretty_name: 'Still',
              default: '',
            },
        },
    };
  
    class JudgeCounterfactualPlugin {
        constructor(jsPsych) {
            this.jsPsych = jsPsych;
        }
        trial(display_element, trial) {
            var slider_width = 500;
            var slider_labels = ['definitely no',
                                 'unsure',
                                 'definitely yes'];
            var button_label = 'Continue';
  
            var html = '<div id="jspsych-html-slider-response-wrapper">';
            html += '<div id="jspsych-html-slider-response-stimulus" style="padding-bottom: 1em;">';
            html += '<h3>' + trial.title + '</h3>';
            html += '<img src="trials/' + trial.trial + '/full.gif"></img></div>';
            html += '<p>Would the red player' + trial.still + " have succeeded if the blue player hadn't been there?</p>";
            html += '<div class="jspsych-html-slider-response-container" style="position:relative; margin: 0 auto 3em auto; width:' + slider_width + 'px;">';
  
            html += '<div style="width: 100%;" class="jspsych-html-slider-response-response slider-three"></div>';
            html += '<div>'
            for(var j=0; j < slider_labels.length; j++){
                var width = 100/(slider_labels.length-1);
                var left_offset = (j * (100 /(slider_labels.length - 1))) - (width/2);
                html += '<div style="display: inline-block; position: absolute; left:'+left_offset+'%; text-align: center; width: '+width+'%; margin-top: 0.4em;">';
                html += '<span style="text-align: center; font-size: 80%;">'+slider_labels[j]+'</span>';
                html += '</div>'
            }
            html += '</div>'; // for response container
            html += '</div>'; // for response wrapper
            html += '</div>';
  
            html += '<button id="jspsych-html-slider-response-next" style="margin: 0 1em 3em 1em;" class="jspsych-btn" disabled>'+button_label+'</button>';
  
            display_element.innerHTML = html;
  
            var response = {};
  
            set_slider();
  
            display_element.querySelector('#jspsych-html-slider-response-next').addEventListener('click', function() {
                response.slider = $('.jspsych-html-slider-response-response').slider('option', 'value');
                end_trial();
            });
  
            const end_trial = () => {
                this.jsPsych.pluginAPI.clearAllTimeouts();
                var trialdata = {
                  "trial": trial.trial,
                  "response": response.slider
                };
                display_element.innerHTML = '';
                this.jsPsych.finishTrial(trialdata);
            };
        }
    };
    JudgeCounterfactualPlugin.info = info;

    return JudgeCounterfactualPlugin;

})(jsPsychModule);
