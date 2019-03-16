var progress = 0
var myNotes = [];//{timeStart : 0, timeEnd :10, pitch :4 ,lyric: "miao"}]; time in miliseconds

function loadNotes()
{
	
	gamePaused = true
	gamePausedAtMs = Date.now()
	gameStartedAtMs = Date.now()
	progress = 0;
	myNotes = [];
	
	var list = document.getElementById("list");
	var info = document.getElementById("info");
	var songEntry = songList[list.selectedIndex];
	
	
	//document.body.removeChild(aud)
	if(aud !== null)
	{
		aud.pause()
		//document.body.removeChild(aud)
	}
	aud = document.createElement("AUDIO");
	aud.src = songEntry.src;
	document.getElementById("playbutton").disabled=true;
	aud.onload=function(){
		document.getElementById("playbutton").disabled=false;
	}
	aud.load()
	document.body.appendChild(aud)
	fifthSignature=0
	
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var gotmyNotes = JSON.parse(this.responseText);
			
			noteThickness = windowy/gotmyNotes.range;
			
			info.innerHTML="loaded json"+songEntry.title;
			
			resetStaticObjects(gotmyNotes.referencePitch);
			
			for (index = 0; index < gotmyNotes.notes.length; ++index) {
				var note = gotmyNotes.notes[index];
				if(note.pitch == -1)
				{
					var beatlyric='!'
					switch(note.lyric.length)
					{
						case 2:
							//tone change
							
							function(){
								
								var deadline = note.start;
								var interv;
								interv = setInterval(function(){
									if(progress>deadline)
									{
										fifthSignature=parseInt(note.lyric)
										clearInterval(interv)
									}
								},500)
								
							}()
							
							beatlyric = "轉調 to"+parseInt(note.lyric)
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
			}
			
			setTimeout(function(){
				document.getElementById("playbutton").disabled=false;
			}, 3000)
			//document.getElementById("playbutton").disabled=false;
			
		}
	};
	xhttp.open("GET", songEntry.noteSrc, true);
	xhttp.send();
	
	/*
	myNotes.push(new myNote(0, 1000,1,'1'))
	myNotes.push(new myNote(1000, 2000,2,'2'))
	myNotes.push(new myNote(2000, 2500,3,'3'))
	myNotes.push(new myNote(2500, 3000,4,'4'))
	*/
}

var songList = []

function refreshList() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var list = document.getElementById("list");
			
			while (list.length > 0) {
				list.remove(0);
			}
			
			songList.splice(0,songList.length)
			
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
