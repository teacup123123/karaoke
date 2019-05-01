
var progBar = document.getElementById('progBar');

var audioPlayers = []
for(i=0; i<10;i++)
{
	audioPlayers.push(document.createElement("AUDIO"));
}

var playbackRate = 1;
function playRate(rate)
{
	playbackRate=rate;
	if(rate==0)
	{
		//gameStartedAtMs+=audioPlayers[0].currentTime;
		progBar.value = 0;
		for(i=0; i<mixers.length;i++)
		{
			audioPlayers[i].currentTime=0;
		}
		rescan = true;
	}
	else
	for(i=0; i<mixers.length;i++)
	{
		audioPlayers[i].playbackRate=rate;
	}
}


function playPauseAudio() { 
	if(gamePaused)
	{
		gameStartedAtMs += (Date.now()-gamePausedAtMs);
		for(i = 0; i<mixers.length;i++)
		{	
			audioPlayers[i].play();
		}
		gamePaused=false;
	}
	else
	{	
		gamePaused=true	;
		for(i = 0; i<mixers.length;i++)
		{	
			audioPlayers[i].pause();
		}
		gamePausedAtMs = Date.now();
	}
} 

function changeProgress()
{
	if(gamePaused)
	{
		progBar.value = 1000*Math.round(progBar.value/1000)
		gameStartedAtMs = gamePausedAtMs-progBar.value
		rescan=true;
		
		for(i = 0; i<mixers.length;i++)
		{	
			audioPlayers[i].currentTime=progBar.value*0.001;
		}
	}
}
