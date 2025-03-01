\version "2.25.23"

print-grob-properties = #( lambda (grob)
  (ly:message "")
  (ly:message "(grob::name grob): ~s" (grob::name grob))
  (ly:message "(ly:grob? grob): ~s" (ly:grob? grob))
  (ly:message "(ly:grob-array? grob): ~s" (ly:grob-array? grob))
  ; (ly:message "(ly:grob-default-font grob): ~s" (ly:grob-default-font grob))
  ; (ly:message "(ly:grob-interfaces grob): ~s" (ly:grob-interfaces grob))
  (ly:message "(ly:grob-extent grob grob 0): ~s" (ly:grob-extent grob grob 0))
  (ly:message "(ly:grob-property grob 'X-extent): ~s" (ly:grob-property grob 'X-extent))
  (ly:message "(ly:grob-robust-relative-extent grob grob 0): ~s"
    (ly:grob-robust-relative-extent grob grob 0))
  (ly:message "(ly:grob-extent grob grob 1): ~s" (ly:grob-extent grob grob 1))
  (ly:message "(ly:grob-property grob 'Y-extent): ~s" (ly:grob-property grob 'Y-extent))
  (ly:message "(ly:grob-robust-relative-extent grob grob 1): ~s"
    (ly:grob-robust-relative-extent grob grob 1))
  (ly:message "(ly:grob-get-vertical-axis-group-index grob): ~s"
    (ly:grob-get-vertical-axis-group-index grob))
  (ly:message "(ly:grob-layout grob): ~s" (ly:grob-layout grob))
  (ly:message "(ly:grob-original grob): ~s" (ly:grob-original grob))
  (ly:message "(ly:grob-parent grob 0): ~s" (ly:grob-parent grob 0))
  (ly:message "(ly:grob-parent grob 1): ~s" (ly:grob-parent grob 1))
  (ly:message "(ly:grob-property grob 'break-align-anchor): ~s"
    (ly:grob-property grob 'break-align-anchor))
  (ly:message "(ly:grob-property grob 'break-align-anchor-alignment): ~s"
    (ly:grob-property grob 'break-align-anchor-alignment))
  (ly:message "(ly:grob-property grob 'break-align-symbol): ~s"
    (ly:grob-property grob 'break-align-symbol))
  (ly:message "(ly:grob-property grob 'break-align-symbols): ~s"
    (ly:grob-property grob 'break-align-symbols))
  (ly:message "(ly:grob-property grob 'break-visibility): ~s"
    (ly:grob-property grob 'break-visibility))
  (ly:message "(ly:grob-property grob 'font-size): ~s"
    (ly:grob-property grob 'font-size))
  (ly:message "(ly:grob-property grob 'non-musical): ~s"
    (ly:grob-property grob 'non-musical))
  (ly:message "(ly:grob-property grob 'outside-staff-priority): ~s"
    (ly:grob-property grob 'outside-staff-priority))
  (ly:message "(ly:grob-property grob 'stencil): ~s"
    (ly:grob-property grob 'stencil))
  (ly:message "(ly:grob-relative-coordinate grob grob 0): ~s"
    (ly:grob-relative-coordinate grob grob 0))
  (ly:message "(ly:grob-relative-coordinate grob grob 1): ~s"
    (ly:grob-relative-coordinate grob grob 1))
  (ly:message "(ly:grob-spanned-column-rank-interval grob): ~s"
    (ly:grob-spanned-column-rank-interval grob))
  (ly:message "(ly:grob-staff-position grob): ~s" (ly:grob-staff-position grob))
  (ly:message "(ly:grob-system grob): ~s" (ly:grob-system grob))
  (ly:message "(grob::rhythmic-location grob): ~s" (grob::rhythmic-location grob))
  (ly:message "(grob::when grob): ~s" (grob::when grob))
  ; (ly:message "(grob::display-objects grob): ~s" (grob::display-objects grob))
  )

%{
  \once \override Staff.Clef.after-line-breaking = #print-grob-properties
  c'4
%}

print-spanner-properties = #(lambda (grob)
    (ly:message "")
    (ly:message "(grob::name grob): ~s" (grob::name grob))
    (ly:message "(ly:grob? grob): ~s" (ly:grob? grob))
    (ly:message "(ly:spanner? grob): ~s" (ly:spanner? grob))
    (ly:message "(ly:item? grob): ~s" (ly:item? grob))
    (ly:message "")
    (ly:message "(ly:grob-property grob 'bound-details): ~s"
      (ly:grob-property grob 'bound-details))
    (ly:message "")
    (ly:message "(assoc-get 'left (ly:grob-property grob 'bound-details)):")
    (ly:message "~s" (assoc-get 'left (ly:grob-property grob 'bound-details)))
    (ly:message "")
    (ly:message "(assoc-get 'right (ly:grob-property grob 'bound-details)):")
    (ly:message "~s" (assoc-get 'right (ly:grob-property grob 'bound-details)))
    (ly:message "")
    (ly:message "(ly:grob-property grob 'left-bound-info): ~s"
      (ly:grob-property grob 'left-bound-info))
    (ly:message "")
    (ly:message "(ly:grob-property grob 'right-bound-info): ~s"
      (ly:grob-property grob 'right-bound-info))
    (ly:message "")
    (ly:message "(ly:spanner-bound grob -1): ~s" (ly:spanner-bound grob -1))
    (ly:message "(ly:spanner-bound grob 1): ~s" (ly:spanner-bound grob 1))
    (ly:message "(ly:spanner-broken-neighbor grob -1): ~s"
      (ly:spanner-broken-neighbor grob -1))
    (ly:message "(ly:spanner-broken-neighbor grob 1): ~s"
      (ly:spanner-broken-neighbor grob 1))
    (ly:message "(first-broken-spanner? grob): ~s" (first-broken-spanner? grob))
    (ly:message "(middle-broken-spanner? grob): ~s" (middle-broken-spanner? grob))
    (ly:message "(end-broken-spanner? grob): ~s" (end-broken-spanner? grob))
    (ly:message "(not-first-broken-spanner? grob): ~s" (not-first-broken-spanner? grob))
    (ly:message "(not-last-broken-spanner? grob): ~s" (not-last-broken-spanner? grob))
    (ly:message "(unbroken-or-first-broken-spanner? grob): ~s"
      (unbroken-or-first-broken-spanner? grob))
    (ly:message "(unbroken-or-last-broken-spanner? grob): ~s"
      (unbroken-or-last-broken-spanner? grob))
    (ly:message "(unbroken-spanner? grob): ~s" (unbroken-spanner? grob))
    (ly:message "")
    )

%{
  {
    \override TupletBracket.after-line-breaking = #print-spanner-properties
    \times 8/10 { c'4 d' e' f' g' \break a' b' c'' d'' e'' }
  }
%}
