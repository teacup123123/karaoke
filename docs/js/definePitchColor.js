
var changeFifthAt=[[0,0]]//starting from time 0, fifth is 0
function updateFifth(prog)
{
	for(i=0;i<changeFifthAt.length;i++)
	{
		if(prog>=changeFifthAt[i][0]){fifthSignature = changeFifthAt[i][1]}
		else{break}
	}
}


function rectangle(width, height, color, x, y,label='', isNote = false) {
    this.width = width;
    this.height = height;
    this.x = x;
    this.y = y;
	this.setx0 = function(z){this.x = z};
	this.sety0 = function(z){this.x = z};
	this.setx1 = function(z){this.width = z-this.x};
	this.sety1 = function(z){this.height = z-this.y};
	this.label = label
	this.isInside = function(){//0 for no and 1 for inside
		return (this.x<=windowx)||(this.x+this.width>=0)||(this.y+this.height>=0)||(this.y<=windowy);
	}
	this.isPlaying = function()
	{
		return (this.x<=blacklinerect.x)&&(this.x+this.width>=blacklinerect.x)
	}
	this.textColor = function(){return 'white'}
	
	if(Array.isArray(color))
	{
		this.colorNeutral=function(){return color[0]}
		this.colorActive=function(){return color[1]}
		if(color.length>2){this.textColor=color[2]}
	}
	else if(typeof(color)=='string')
	{
		this.colorNeutral=function(){return color}
		this.colorActive=function(){return color}
	}
	else
	{
		color = color();//call function generator
		//should now be two functions
		this.colorNeutral=color[0]
		this.colorActive=color[1]
		if(color.length>2){this.textColor=color[2]}
	}
	this.isNote = isNote
    this.update = function() {
		if(this.isInside())
		{
			ctx = myGameArea.context;
			if(this.isNote&&this.isPlaying())
			{
				ctx.fillStyle = this.colorActive();
			}
			else
			{
				ctx.fillStyle = this.colorNeutral();
			}
			ctx.fillRect(this.x, this.y, this.width, this.height);
			ctx.fillStyle = this.textColor();
			ctx.font = noteThickness.toString()+"px Arial";
			ctx.fillText(this.label, this.x, this.y+noteThickness);
		}
    }
}

function myNote(startms, endms,pitch,lyric='')
{
	if(lyric.startsWith('轉調 to'))
	{
		var _ = parseInt(lyric.slice(-2));
		
		changeFifthAt.push([startms,_])
		
	}
	this.start= startms;
	this.end= endms;
	this.duration = endms-startms;
	this.pitch = pitch;
	this.lyric = lyric;
	this.rect = (function(){
		var fun0 = function(){return pitchColor(pitch)[0]}
		var fun1 = function(){return pitchColor(pitch)[1]}
		var fun2 = function(){return pitchColor(pitch)[2]}
		return new rectangle((endms-startms)/msPerPx, noteThickness, function(){return [fun0,fun1,fun2]}, windowx, windowy , lyric, true)
	})()
}

var _pitch_dict = {};
_pitch_dict[3-3] = ['crimson','red','white'];//C
_pitch_dict[4-3] = ['darkred','grey','white'];//C~D
_pitch_dict[5-3] = ['darkorange','orange','black'];//D
_pitch_dict[6-3] = ['firebrick','grey','white'];//D~E
_pitch_dict[7-3] = ['gold','yellow','black'];//E
_pitch_dict[8-3] = ['darkgreen','green','white'];//F
_pitch_dict[9-3] = ['darkseagreen','grey','white'];//F~G
_pitch_dict[10-3] = ['teal','darkturquoise','black'];//G
_pitch_dict[11-3] = ['thistle','grey','black'];//G~A
_pitch_dict[12-3] = ['magenta','violet','white'];//A 
_pitch_dict[13-3] = ['mediumpurple','grey','white'];//A~B
_pitch_dict[14-3] = ['darkmagenta','mediumpurple','white'];//B

var pitchOffset =0;

function addfifth(i,j)
{
	return i-7*j
}

var fifthSignature = 0
function pitchColor(pitch)
{
	return _pitch_dict[addfifth(pitch+pitchOffset,fifthSignature)%12]//in reality this should be a function of the pitch!!!
}
