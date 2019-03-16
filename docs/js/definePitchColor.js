var _pitch_dict = {};
_pitch_dict[3-3] = ['crimson','red'];//C
_pitch_dict[4-3] = ['darkred','grey'];//C~D
_pitch_dict[5-3] = ['darkorange','orange'];//D
_pitch_dict[6-3] = ['firebrick','grey'];//D~E
_pitch_dict[7-3] = ['gold','yellow'];//E
_pitch_dict[8-3] = ['darkgreen','green'];//F
_pitch_dict[9-3] = ['darkseagreen','grey'];//F~G
_pitch_dict[10-3] = ['teal','darkturquoise'];//G
_pitch_dict[11-3] = ['thistle','grey'];//G~A
_pitch_dict[12-3] = ['magenta','violet'];//A 
_pitch_dict[13-3] = ['mediumpurple','grey'];//A~B
_pitch_dict[14-3] = ['darkmagenta','mediumpurple'];//B

var pitchOffset =0;

function addfifth(i,j)
{
	return i+7*j
}

var fifthSignature = 0
function pitchColor(pitch)
{
	color = _pitch_dict[addfifth(pitch+pitchOffset,fifthSignature)%12]//in reality this should be a function of the pitch!!!
	return color
}
