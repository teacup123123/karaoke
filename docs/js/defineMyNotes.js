
var myNotes = [];//{timeStart : 0, timeEnd :10, pitch :4 ,lyric: "miao"}]; time in miliseconds

var progBar = document.getElementById('progBar');

function detectPlayable(listOfAudios)//detects that every audio in the list has finished loading
{
	//This function works!
	(function()
	{
		var CancelYourself;
		
		CancelYourself = setInterval(function(){
			var allgood = true;
			for(i=0;i<listOfAudios.length;i++)
			{
				if(listOfAudios[i].readyState!=4)
				{
					allgood=false
				}
			}
			if(allgood)
			{
				document.getElementById("playbutton").disabled=false;
				clearInterval(CancelYourself);
				progBar.setAttribute('max',listOfAudios[0].duration*1000);
			}
		},500)
	})();
}


function loadNotes(online=true)
{
	
	gamePaused = true
	gamePausedAtMs = Date.now()
	gameStartedAtMs = Date.now()
	
	var list = document.getElementById("list");
	var info = document.getElementById("info");
	var songEntry = songList[list.selectedIndex];
	
	var _used_auds =[]
	var tracks=songEntry['tracks']
	for(i = 0;i<tracks.length;i++)
	{
		var aud = audioPlayers[i];
		_used_auds.push(aud);
		aud.src = songEntry.src;
		document.getElementById("playbutton").disabled=true;
		aud.load();
		fifthSignature=0
		
		if(online)
		{
			var xhttp = new XMLHttpRequest();
			xhttp.onreadystatechange = function() {
				if (this.readyState == 4 && this.status == 200) {
					
					var gotmyNotes = JSON.parse(this.responseText);
					
					noteThickness = windowy/gotmyNotes.range;
					
					info.innerHTML="loaded json "+songEntry.title;
					
					resetStaticObjects(gotmyNotes.referencePitch);
					
					myNotes.length = 0;
					for (index = 0; index < gotmyNotes.notes.length; ++index) {
						var note = gotmyNotes.notes[index];
						if(note.pitch == -1)
						{
							var beatlyric='!'
							switch(note.lyric.length)
							{
								case 2:
									
									beatlyric = "轉調 to "+parseInt(note.lyric)
									break
								case 0:
									break
								default:
									beatlyric = note.lyric
							}
							myNotes.push(new myNote(note.start, note.start+10,gotmyNotes.range-2,beatlyric,'black'))
						}
						else
						{
							myNotes.push(new myNote(note.start, note.end,note.pitch-gotmyNotes.referencePitch,note.lyric))					
						}
						rescan = true;
					}
					
					progBar.value = 0;
					//document.getElementById("playbutton").disabled=false;
					
				}
			};
			xhttp.open("GET", songEntry.noteSrc, true);
			xhttp.send();
		}
		else
		{
			var gotmyNotes = JSON.parse(this.responseText);
					
				noteThickness = windowy/gotmyNotes.range;
				
				info.innerHTML="loaded json "+songEntry.title;
				
				resetStaticObjects(gotmyNotes.referencePitch);
				
				myNotes.length = 0;
				for (index = 0; index < gotmyNotes.notes.length; ++index) {
					var note = gotmyNotes.notes[index];
					if(note.pitch == -1)
					{
						var beatlyric='!'
						switch(note.lyric.length)
						{
							case 2:
								
								beatlyric = "轉調 to "+parseInt(note.lyric)
								break
							case 0:
								break
							default:
								beatlyric = note.lyric
						}
						myNotes.push(new myNote(note.start, note.start+10,gotmyNotes.range-2,beatlyric,'black'))
					}
					else
					{
						myNotes.push(new myNote(note.start, note.end,note.pitch-gotmyNotes.referencePitch,note.lyric))					
					}
					rescan = true;
				}
				
				progBar.value = 0;
				//document.getElementById("playbutton").disabled=false;
		}
	}
	updateVoices(songEntry)
	detectPlayable(_used_auds);
}

var songList = []

function refreshList(online=true) {
	if(online)
	{
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
				var list = document.getElementById("list");
			if (this.readyState == 4 && this.status == 200) {
				
				while (list.length > 0) {
					list.remove(0);
				}
				
				songList.length=0
				
				var jsonList = JSON.parse(this.responseText);
				for (index = 0; index < jsonList.length; ++index) {
					var song = jsonList[index];
					var opti = document.createElement('option');
					opti.text = song.title;
					list.add(opti)
					songList.push(song)
				}
			}
		};
		xhttp.open("GET", "json/list.json", true);
		xhttp.send();
	}
	else
	{
		var list = document.getElementById("list");	
		while (list.length > 0) {
			list.remove(0);
		}
		
		songList.length=0
		
		var jsonList = fakeRead
		for (index = 0; index < jsonList.length; ++index) {
			var song = jsonList[index];
			var opti = document.createElement('option');
			opti.text = song.title;
			list.add(opti)
			songList.push(song)
		}
	}
}
