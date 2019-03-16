var _pitch_dict = {};
_pitch_dict[0] = ['magenta','violet'];//A 
_pitch_dict[1] = ['mediumpurple','grey'];//A~B
_pitch_dict[2] = ['darkmagenta','mediumpurple'];//B
_pitch_dict[3] = ['crimson','red'];//C
_pitch_dict[4] = ['darkred','grey'];//C~D
_pitch_dict[5] = ['darkorange','orange'];//D
_pitch_dict[6] = ['firebrick','grey'];//D~E
_pitch_dict[7] = ['gold','yellow'];//E
_pitch_dict[8] = ['darkgreen','green'];//F
_pitch_dict[9] = ['darkseagreen','grey'];//F~G
_pitch_dict[10] = ['teal','darkturquoise'];//G
_pitch_dict[11] = ['thistle','grey'];//G~A

var pitchOffset =0;

function pitchColor(pitch)
{
	color = _pitch_dict[(pitch+pitchOffset)%12]//in reality this should be a function of the pitch!!!
	return color
}
