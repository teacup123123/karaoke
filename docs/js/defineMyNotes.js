var progress = 0
var myNotes = [];//{timeStart : 0, timeEnd :10, pitch :4 ,lyric: "miao"}]; time in miliseconds

function loadNotes()
{
	progress = 0;
	myNotes = [];
	
	var list = document.getElementById("list");
	var info = document.getElementById("info");
	info.innerHTML='loaded!!'
	
	myNotes.push(new myNote(0, 1000,1,lyric='1'))
	myNotes.push(new myNote(1000, 2000,2,lyric='2'))
	myNotes.push(new myNote(2000, 2500,3,lyric='3'))
	myNotes.push(new myNote(2500, 3000,4,lyric='4'))
}

function refreshList() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			var list = document.getElementById("list");
			
			while (list.length > 0) {
				list.remove(0);
			}
			
			var jsonList = JSON.parse(this.responseText);
			for (index = 0; index < jsonList.length; ++index) {
				var song = jsonList[index];
				var opti = document.createElement('option');
				opti.text = song.title;
				list.add(opti)
			}
			
		}
	};
	xhttp.open("GET", "json/list.json", true);
	xhttp.send();
}

refreshList()