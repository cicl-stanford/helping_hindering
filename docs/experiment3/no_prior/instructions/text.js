var ex_outcome = 'success';
var ex_red_name = 'Parker';
var ex_blue_name = 'Kit';
var height = 443;
var height_short = 352;
// 5em + height of trial images (jspsych font: 1em = 18px)

var starter = '<div style="height:' + height + 'px; text-align: center;">';
var starter_short = '<div style="height:' + height_short + 'px; text-align: center;">'; 
var starter_ex = starter_short + '<h3 style="margin-bottom: -10px;"> Example </h3> <p> Player A: ' + red(ex_red_name) + ', Player B: ' + blue(ex_blue_name) + '</p> <img src="trials/0/';
var end_ex = '.png" style="max-height: 100%; width: auto;"> </img> </div>';

const imagesHTML =
    '<div style="width: 50%; margin: 0 auto;">' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_red.png" style="width: 60px; margin-top: 200px;"></img></div>' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_blue.png" style="width: 60px; margin-top: 200px;"></img></div>' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_salmon.png" style="width: 60px; margin-top: 200px;"></img></div>' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_aqua.png" style="width: 60px; margin-top: 200px;"></img></div>' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_pink.png" style="width: 60px; margin-top: 200px;"></img></div>' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_green.png" style="width: 60px; margin-top: 200px;"></img></div>' +
    '</div> </div> <div style="width: 50%; margin-top: -150px; margin-left: 170px;">' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_teal.png" style="width: 60px;"></img></div>' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_brown.png" style="width: 60px;"></img></div>' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_lime.png" style="width: 60px;"></img></div>' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_magenta.png" style="width: 60px;"></img></div>' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_navy.png" style="width: 60px;"></img></div>' +
    '<div style="width: 15%; float: left;">' +
    '<img src="instructions/agent_orange.png" style="width: 60px;"></img></div>' +
    '</div>' +
    '</div>' +
    '<div style="text-align: center; margin-top: 100px;">' +
    '<p>In this experiment, you will watch a game that involves two players, <b>Player A</b> and <b>Player B</b>, moving around in different grids. The players can be many different colors, as shown above.</p>' +
    '</div>';

var page1 = starter + imagesHTML;

var page2 = starter + 
        '<img src="instructions/instructions1.gif" style="margin-top: 2em;">' +
        ' </img> </div>' +
        '<p> In this example, Player A is ' + red('red') + '. The goal of Player A is to reach the star before time runs' +
        ' out. On each step, Player A can move up, down, left, right,' +
        ' or stay in place. They cannot move through walls. If they reach' +
        ' the star in time, then they succeed! </p>';

var page3 = starter + 
        '<img src="instructions/instructions2.gif" style="margin-top: 2em;">' +
        ' </img> </div>' +
        '<p> In this example, Player B is ' + blue('blue') + '. Player B can move up, down, left, right, or' +
        ' stay in place, and cannot move through walls. Some of the' +
        ' grids contain boxes. Player B can additionally pick these' +
        ' boxes up to push or pull around. </p>';

var page4 = starter_short +
        '<img src="instructions/instructions3.gif" style="height: 240px; margin:' +
        ' auto; margin-top: 4em;"> </div>' +
        '<p> The two players take turns moving. The players are able to pass through each other in the same grid.' + 
        ' However, neither player can move through boxes. </p>' +
        ' <p>' + blue('Player B') + ' is either a <b>helper</b>, or a <b>hinderer</b>.' +
        " If " + blue('Player B') + " is a helper, they will try their best to help " + red('Player A') + " reach" +
        ' the star. If ' + blue('Player B') + ' is a hinderer, they will try their best to hinder ' + red('Player A') + ' from' +
        ' reaching the star. <br> <br> Here is an example in which ' +
        blue('Player B') + ' is a <b>helper</b>. </p>';

var page5 = starter_short +
        '<img src="instructions/instructions4.gif" style="height: 240px; margin:' +
        ' auto; margin-top: 4em;"> </div> <p> Here is an example in which ' +
        blue('Player B') + ' is a <b>hinderer</b>. </p>';

var pageE1 = starter_ex + '00' + end_ex +
        "<p> Let's watch an example scenario. " + red(ex_red_name) + ' was' +
        ' Player A and ' + blue(ex_blue_name) + ' was Player B.' +
        ' The number of timesteps remaining is shown on the right.' +
        ' Player A always goes first. <br> <br>' +
        ' Click the "Next" button to see what happened next. </p>';

var pageE2 = starter_ex + '01' + end_ex +
        '<p>' + red(ex_red_name) + ' went first and took a step right. </p>';

var pageE3 = starter_ex + '02' + end_ex +
        '<p>' + blue(ex_blue_name) + ' took a step right. </p>';

var pageE4 = starter_ex + '03' + end_ex +
        '<p>' + red(ex_red_name) + ' took a step down. </p>';

var pageE5 = starter_ex + '04' + end_ex +
        '<p>' + blue(ex_blue_name) + ' took another step right. </p>';

var pageE6 = starter_ex + '05' + end_ex +
        '<p>' + red(ex_red_name) + ' took a step down. </p>';

var pageE7 = starter_ex + '06' + end_ex +
        '<p>' + blue(ex_blue_name) + ' picked up the box. </p>';

var pageE8 = starter_ex + '07' + end_ex +
        '<p>' + red(ex_red_name) + ' did nothing on this timestep. </p>';

var pageE9 = starter_ex + '08' + end_ex +
        '<p>' + blue(ex_blue_name) + ' pulled the box up. </p>';

var pageE10 = starter_ex + '09' + end_ex +
        '<p>' + red(ex_red_name) + ' took a step right. </p>';

var pageE11 = starter_ex + '10' + end_ex +
        '<p>' + blue(ex_blue_name) + ' let go of the box. </p>';

var pageE12 = starter_ex + '11' + end_ex +
        '<p>' + red(ex_red_name) + ' took another step right. </p>';

var pageE13 = starter_ex + '12' + end_ex +
        '<p>' + blue(ex_blue_name) + ' did nothing on this timestep. </p>';

var pageE14 = starter_ex + '13' + end_ex +
        '<p>' + red(ex_red_name) + ' took a step up and reached the star. </p>';

var pageE15 = starter_ex + '14' + end_ex +
        '<p>' + red(ex_red_name) + ' succeeded! And there were 3 timesteps remaining.' +
        ' </p> <p> Next, we will ask you some questions about what happened.' +
        ' You will be able to watch a video replay of what happened. </p>';


var instruction_pages = [
    page1,
    page2,
    page3,
    page4,
    page5,
    pageE1,
    pageE2,
    pageE3,
    pageE4,
    pageE5,
    pageE6,
    pageE7,
    pageE8,
    pageE9,
    pageE10,
    pageE11,
    pageE12,
    pageE13,
    pageE14,
    pageE15
];

for (var i = 0; i < instruction_pages.length; i++) {
    instruction_pages[i] = '<div style="width: 700px; min-width: 300px; margin:' +
        'auto 5em;">' + instruction_pages[i] + '</div>';
}

var instructions_last = '<p> In this experiment, we will show you several scenarios' +
        ' like this where Player A either succeeds or fails to reach' +
        ' the star in time. We want to know whether you think Player B is a helper' +
        ' or a hinderer, and how responsible you think each player was for the success or failure. </p>';

var comprehension1 = '<p> The goal of both players is to reach the star first.</p>';
var options1 = ['True', 'False']
                    
var comprehension2 = '<p> Player A is ' + red('red') + ' and Player B is ' + blue('blue') + '. Which of the following is possible here? </p>' +
        '<img src="instructions/comprehension1.png" style="height: auto;' +
        ' width: 50%;"></img> <br> <ol>' +
        '<li> Player A can walk around the box. </li>' +
        '<li> Player A can push the box out of the way. </li>' +
        "<li> Player B can pull the box out of Player A's way." +
        '</li> </ol>';
var options2 = ['1 only', '2 only', '3 only', 'All of the above'];

var comprehension3 = '<p> Player B can either be a helper or a hinderer towards Player A. </p>';
var options3 = ['True', 'False'];

var comprehension4 = '<p> Which of the following can pass through one another in the same grid? </p>' +
        '<ol> <li> Player A and a box. </li>' +
        '<li> Player A and Player B. </li>' +
        '<li> Player B and a box. </li>' +
        '</li> </ol>';
var options4 = ['1 only', '2 only', '3 only', 'All of the above'];
                    
var start_prompt1 = '<p> Correct! You will now see several trials featuring' +
        ' a different Player A and Player B in a different grid each time.' +
        ' The two players will be different colors each time. </p>' +
        '<p> In each trial, you will first get to walk through a step' +
        '-by-step play of what happened on each timestep. You can proceed by either' +
        ' clicking the buttons, or pressing left (&#8592;) and right (&#8594;) arrow keys.' +
        ' Then, you will see a video replay of what happened' +
        ' while answering the questions, just like in the example. </p>';

var start_prompt2 = '<p> Remember, the goal of <b>Player A</b> is to' +
        ' reach the star before time runs out. <b>Player B</b>' +
        ' can move boxes around, and is either a helper or a hinderer.' +
        ' Neither player can walk through boxes or walls.' +
        '</p> <p> Please do not refresh the page. Click the Start button whenever' +
        " you're ready. <p>";

var instruction_images = [
        'instructions/agent_red.png',
        'instructions/agent_blue.png',
        'instructions/agent_salmon.png',
        'instructions/agent_aqua.png',
        'instructions/agent_pink.png',
        'instructions/agent_green.png',
        'instructions/agent_teal.png',
        'instructions/agent_brown.png',
        'instructions/agent_lime.png',
        'instructions/agent_magenta.png',
        'instructions/agent_navy.png',
        'instructions/agent_orange.png',
        'instructions/instructions1.gif',
        'instructions/instructions2.gif',
        'instructions/instructions3.gif',
        'instructions/instructions4.gif',
        'instructions/comprehension1.png',
        'trials/0/00.png',
        'trials/0/01.png',
        'trials/0/02.png',
        'trials/0/03.png',
        'trials/0/04.png',
        'trials/0/05.png',
        'trials/0/06.png',
        'trials/0/07.png',
        'trials/0/08.png',
        'trials/0/09.png',
        'trials/0/10.png',
        'trials/0/11.png',
        'trials/0/12.png',
        'trials/0/13.png',
        'trials/0/14.png',
        'trials/0/full.gif'
];
