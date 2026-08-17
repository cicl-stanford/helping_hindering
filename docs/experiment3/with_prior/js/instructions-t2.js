/* jspsych-instructions.js
 * Josh de Leeuw
 * (with edits by Sarah)
 *
 *
 */

jsPsych.plugins['instructions-t2'] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'instructions-t2',
    description: '',
    parameters: {
      trial: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name: 'Trial',
        default: null,
        description: 'Trial number'
      },
      pages: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name: 'Pages',
        default: undefined,
        array: true,
        description: 'Each element of the array is the content for a single page.'
      },
      header: {
        type: jsPsych.plugins.parameterType.HTMl_STRING,
        pretty_name: 'Header',
        default: '',
        description: 'Content to display above main content at the top of each page.'
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
      judgment_t1: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name: 'Judgment from T1',
        default: null,
        description: 'Previous round response'
      },
      show_clickable_nav: {
        type: jsPsych.plugins.parameterType.BOOL,
        pretty_name: 'Show clickable nav',
        default: false,
        description: 'If true, then a "Previous" and "Next" button will be displayed beneath the instructions.'
      },
      button_label_previous: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Button label previous',
        default: 'Previous',
        description: 'The text that appears on the button to go backwards.'
      },
      button_label_next: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Button label next',
        default: 'Next',
        description: 'The text that appears on the button to go forwards.'
      }
    }
  }

  plugin.trial = function(display_element, trial) {

    var current_page = 0;
    var view_history = [];
    var start_time = performance.now();
    var last_page_update_time = start_time;
    var key_backward = 'leftarrow';
    var key_forward = 'rightarrow';

    function btnListener(evt){
      evt.target.removeEventListener('click', btnListener);
      if(this.id === "jspsych-instructions-back"){
        back();
      }
      else if(this.id === 'jspsych-instructions-next'){
        next();
      }
    }

    function show_current_page() {
      var html = '</h3><p style="margin-bottom: -10px;">' + trial.footer + '</p>';

      // display gif of t1 while clicking through t2
      html += '<div style="display: flex;"><h4 style="flex: 1; opacity: 0.5; margin-right: 200px; margin-top: -3px;">Round 1</h4><h4 style="flex: 1; margin-right: 170px; margin-top: -3px;">Round 2</h4></div>';
      html += '<div style="display: flex; margin-right: 350px"><img src="trials/' + trial.trial + '/t1/full.gif" alt="Left Image" style="flex: 1; width: 50%; height: 50%; opacity: 0.5;">';
      html += trial.pages[current_page] + '</div>';
      
      html += '<div> <p style="flex: 1; margin-top: -230px; max-width: 22%; opacity: 0.6; font-size: 45%"> <i> This is what you responded previously. </i></p>';
      html += '<div> <p style="flex: 1; margin-top: -10px; max-width: 22%; opacity: 0.6; font-size: 48%"> What should <b><span style="color:rgb' + trial.red_display + ';">' + trial.red_name + '</span></b> do in Round 2? </p>';

      var participantResponse = trial.judgment_t1;
      html += '<input style="flex: 1; float: left; margin-left: 2px; width: 200px; height: 10px; opacity: 0.9; -webkit-appearance: none; background: white; border: 1px solid #D3D3D3; border-radius: 0px;" type="range" min="0" max="100" value="' + participantResponse + '" disabled></div>';
      html += '<div style="clear: both; display: flex; margin-left: -22px; margin-bottom: 120px; opacity: 0.6; justify-content: space-between; width: 250px; font-size: 40%"> <span>do the same thing</span> <span>try something different</span> </div>';




      display_element.innerHTML = html;
      
      if (trial.show_clickable_nav) {
        
        var nav_html = "<div class='jspsych-instructions-nav' style='margin-left: 295px; padding: 10px 0px;'>";
        var allowed = (current_page > 0 )? '' : "disabled='disabled'";
        nav_html += "<button id='jspsych-instructions-back' class='jspsych-btn'" +
          "style='margin-right: 5px; margin-top: 30px;' " + allowed + "> &#8592; " +
          trial.button_label_previous + "</button>";

        var slider_exists = ($('.jspsych-html-slider-response-response').length);
        nav_html += "<button id='jspsych-instructions-next' class='jspsych-btn'"+
            "style='margin-left: 5px; margin-top: 30px;' " + (slider_exists ? "disabled" : "") +
            ">" + trial.button_label_next + " &#8594;</button></div>";

        html += nav_html;

        display_element.innerHTML = html;
        if (current_page != 0) {
          display_element.querySelector('#jspsych-instructions-back').addEventListener('click', btnListener);
        }

        display_element.querySelector('#jspsych-instructions-next').addEventListener('click', btnListener);
      } else {
        display_element.innerHTML = html;
      }
      set_slider();
    }

    function next() {

      add_current_page_to_view_history()

      current_page++;

      // if done, finish up...
      if (current_page >= trial.pages.length) {
        endTrial();
      } else {
        show_current_page();
      }

    }

    function back() {

      add_current_page_to_view_history()

      current_page--;

      show_current_page();
    }

    function add_current_page_to_view_history() {

      var current_time = performance.now();

      var page_view_time = current_time - last_page_update_time;

      view_history.push({
        page_index: current_page,
        viewing_time: page_view_time
      });

      last_page_update_time = current_time;
    }

    function endTrial() {

      jsPsych.pluginAPI.cancelKeyboardResponse(keyboard_listener);

      display_element.innerHTML = '';

      var trial_data = {
        "view_history": JSON.stringify(view_history),
        "rt": performance.now() - start_time
      };

      jsPsych.finishTrial(trial_data);
    }

    var after_response = function(info) {

      // have to reinitialize this instead of letting it persist to prevent accidental skips of pages by holding down keys too long
      keyboard_listener = jsPsych.pluginAPI.getKeyboardResponse({
        callback_function: after_response,
        valid_responses: [key_forward, key_backward],
        rt_method: 'performance',
        persist: false,
        allow_held_key: false
      });
      // check if key is forwards or backwards and update page
      if (jsPsych.pluginAPI.compareKeys(info.key, key_backward)) {
        if (current_page !== 0) {
          back();
        }
      }

      if (jsPsych.pluginAPI.compareKeys(info.key, key_forward)) {
        next();
      }

    };

    show_current_page();

    var keyboard_listener = jsPsych.pluginAPI.getKeyboardResponse({
      callback_function: after_response,
      valid_responses: [key_forward, key_backward],
      rt_method: 'performance',
      persist: false
    });
  };

  return plugin;
})();
