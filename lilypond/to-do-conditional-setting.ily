%%%2020-02-20 from Aaron Hill on list

%%%%
\version "2.19.84"

includeMIDI = ##t

\score {
   { b'4 }
   \layout {}
   #(if (and (defined? 'includeMIDI) includeMIDI)
     #{ \midi { \tempo 4 = 150 } #} )
}
%%%%
