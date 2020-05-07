% Aaron Hill, 2020-02-25:

% This is usually where \alterBroken comes into play.  It works with
% anything that is a Spanner, allowing you to specify the desired value
% for each segment.

%%%%
{
   \set Staff.pedalSustainStyle = #'mixed
   \alterBroken Y-offset #'(0 -16) Staff.SustainPedalLineSpanner
   c'2\sustainOn c'
   c'1 \break
   c'2 c'\sustainOff
   c'1
}
%%%%
