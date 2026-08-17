var height = 443;
var height_short = 352;
// 5em + height of trial images
// jspsych font 1em = 18px

var starter = '<div style="height:' + height + 'px; text-align: center;">';
var starter_short = '<div style="height:' + height_short + 'px; text-align: center;">';
var starter_ex = starter_short + '<h3 style="margin-top: 0em; padding-top: 1em;">' + 
    ' Example </h3> <img src="trials/0/';
var end_ex = '.png" style="max-height: 100%; width: auto; margin: auto;"> </img> </div>';

var page1 = starter +
        '<div style="width: 30%; margin-left: 20%; float:left;">' +
        '<img src="instructions/agent_red.png" style="width: 60px;' +
            'margin-top: 12em;"></img> </div>' +
        '<div style="width: 30%; margin-right: 20%; float:left;">' +
        '<img src="instructions/agent_blue.png" style="width: 60px;' +
            'margin-top: 12em;"></img> </div> </div>' + 
        '<p> In this experiment, you will watch a red player and a blue' +
        ' player moving around in different grids. </p>';

var page2 = starter + 
        '<img src="instructions/instructions1.gif" style="margin-top: 2em;">' +
        ' </img> </div>' +
        '<p> The goal of the red player is to reach the star before time runs' +
        ' out. On each step, the red player can move up, down, left, right,' +
        ' or stay in place. They cannot move through walls. If they reach' +
        ' the star in time, then they succeed! </p>';

var page3 = starter + 
        '<img src="instructions/instructions2.gif" style="margin-top: 2em;">' +
        ' </img> </div>' +
        '<p> The blue player can similarly move up, down, left,' +
        ' right, or stay in place, and cannot move through walls.' +
        ' Some of the grids contain boxes. The blue player can push or' +
        ' pull any of these boxes around. </p>';

var page4 = starter_short +
        '<img src="instructions/instructions3.gif" style="height: 240px; margin:' +
        ' auto; margin-top: 4em;"> </div>' +
        '<p> The two players take turns moving. They can pass each other' +
        ' through the same square, but neither player can move through boxes.' +
        // double quotes
        " Sometimes the blue player's actions help the red player reach" +
        ' the star, and sometimes they hinder the red player from' +
        ' reaching the star. <br> <br> Here is an example of the blue' +
        ' player <b>helping</b> the red player. </p>';

var page5 = starter_short +
        '<img src="instructions/instructions4.gif" style="height: 240px; margin:' +
        ' auto; margin-top: 4em;"> </div> <p> Here is an example of the' +
        ' blue player <b>hindering</b> the red player. </p>';

var page_ex0 = starter_ex + '00' + end_ex + 
        "<p> Let's watch an example scenario. The number of timesteps remaining" +
        ' is shown on the right. The red player always goes first. </p>' +
        '<p> Click the "Next" button to see what happened next. </p>';

var page_ex1 = starter_ex + '01' + end_ex +
        '<p> The red player went first and took a step right. </p>';

var page_ex2 = starter_ex + '02' + end_ex +
        '<p> The blue player took a step right. </p>';

var page_ex3 = starter_ex + '03' + end_ex +
        '<p> The red player took a step down. </p>';

var page_ex4 = starter_ex + '04' + end_ex + 
        '<p> The blue player took another step right. </p>'; 

var page_ex5 = starter_ex + '05' + end_ex + 
        '<p> The red player took another step down. </p>'; 

var page_ex6 = starter_ex + '06' + end_ex + 
        '<p> The blue player picked up the box. </p>';

var page_ex7 = starter_ex + '07' + end_ex + 
        '<p> The red player did nothing on this timestep. </p>';

var page_ex8 = starter_ex + '08' + end_ex + 
        '<p> The blue player pulled the box up. </p>';

var page_ex9 = starter_ex + '09' + end_ex +
        '<p> The red player took a step right. </p>';

var page_ex10 = starter_ex + '10' + end_ex + 
        '<p> The blue player let go of the box. </p>';

var page_ex11 = starter_ex + '11' + end_ex +
        '<p> The red player took another step right. </p>';

var page_ex12 = starter_ex + '12' + end_ex + 
        '<p> The blue player did nothing on this timestep. </p>';

var page_ex13 = starter_ex + '13' + end_ex + 
        '<p> The red player took a step up and reached the star. The red player' +
        ' succeeded this time! And there were 3 timesteps remaining. </p>' +
        '<p> Next, we will ask you some questions about what happened.' +
        ' You will be able to watch a video replay of what happened. </p>';

var outcome_ex = 'success';
var still_ex = ' still';

var instruction_pages = [
    page1,
    page2,
    page3,
    page4,
    page5,
    page_ex0,
    page_ex1,
    page_ex2,
    page_ex3,
    page_ex4,
    page_ex5,
    page_ex6,
    page_ex7,
    page_ex8,
    page_ex9,
    page_ex10,
    page_ex11,
    page_ex12,
    page_ex13
];

for (var i = 0; i < instruction_pages.length; i++) {
    instruction_pages[i] = '<div style="width: 700px; min-width: 300px; margin:' +
        'auto 5em;">' + instruction_pages[i] + '</div>';
}

var instructions_last = '<p> In this experiment, we will show you scenarios' +
        ' like this where the red player either succeeds or fails to reach' +
        ' the star in time. We want to know what you think the blue' +
        " player's intention was in each scenario. </p>";

var comprehension1 = '<p> The goal of both players is to reach the star first.</p>';
var options1 = ['True', 'False']
                    
var comprehension2 = '<p> Which of the following is possible here? </p>' +
        '<img src="instructions/comprehension1.png" style="height: auto;' +
        ' width: 50%;"></img> <br> <ol style="margin-left:15%;">' +
        '<li> The red player can walk around the box. </li>' +
        '<li> The red player can push the box out of the way. </li>' +
        // double quotes
        "<li> The blue player can pull the box out of the red player's way." +
        '</li> </ol>';
var options2 = ['1 only', '2 only', '3 only', 'All of the above'];

var comprehension3 = '<p> The blue player can either help or hinder the red' +
        ' player using the boxes. </p>';
var options3 = ['True', 'False'];
                    
var comprehension4 = '<p> Which of the following can pass through one another in the same grid? </p>' +
        '<ol style="margin-left:30%;"> <li> The red player and a box. </li>' +
        '<li> The red player and the blue player. </li>' +
        '<li> The blue player and a box. </li>' +
        '</li> </ol>';
var options4 = ['1 only', '2 only', '3 only', 'All of the above'];
                    
var start_prompt1 = '<p> Correct! You will now see 24 different scenarios featuring' +
        ' a red player and a blue player in a different grid each time. </p>' +
        '<p> In each scenario, you will first get to walk through a step' +
        '-by-step play of what happened. You can proceed by either clicking' +
        ' the buttons, or pressing the left (&#8592;) and right (&#8594;) arrow keys.' +
        ' backwards to see what happened on each time step. Then, you will see' +
        ' a video replay of what happened while answering the question, just' +
        ' like in the example. </p>';

var start_prompt2 = '<p> Remember, the goal of the red player is to reach the star' +
        ' before time runs out, and the blue player can move boxes around.' +
        ' Neither player can walk through boxes or walls, but they can pass' +
        ' through each other in the same square. </p>' +
        ' <p> Please do not refresh the page. Click the start button whenever' +
        ' you are ready. <p>';

var instruction_images = [
        'instructions/agent_red.png',
        'instructions/agent_blue.png',
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
        'trials/0/full.gif'
];
