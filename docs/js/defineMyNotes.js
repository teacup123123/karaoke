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
	var music = document.getElementById("karaokeSrc");
	var songEntry = songList[list.selectedIndex];
	music.src = songEntry.src;
	document.getElementById("playbutton").disabled=true;
	music.onload=function(){
		document.getElementById("playbutton").disabled=false;
	}
	
	
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var gotmyNotes = JSON.parse(this.responseText);
			
			noteThickness = windowy/gotmyNotes.range;
			
			info.innerHTML="loaded json"+songEntry.title;
			
			resetStaticObjects();
			
			for (index = 0; index < gotmyNotes.notes.length; ++index) {
				var note = gotmyNotes.notes[index];
				myNotes.push(new myNote(note.start, note.end,note.pitch-gotmyNotes.referencePitch,note.lyric))
			}
			
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
