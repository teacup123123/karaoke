var progress = 0
var myNotes = [];//{timeStart : 0, timeEnd :10, pitch :4 ,lyric: "miao"}]; time in miliseconds

function loadNotes(src)
{
	progress = 0;
	myNotes = [];
	
	myNotes.push(new myNote(0, 1000,1,lyric='1'))
	myNotes.push(new myNote(1000, 2000,2,lyric='2'))
	myNotes.push(new myNote(2000, 2500,3,lyric='3'))
	myNotes.push(new myNote(2500, 3000,4,lyric='4'))
}

function refreshList() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			document.getElementById("list").innerHTML = this.responseText;
		}
	};
	xhttp.open("GET", "json/list.json", true);
	xhttp.send();
}

refreshList()