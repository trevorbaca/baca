from abjad.helpers.instances import instances


def apply_molto_pressione(expr, start, stop = None):
   leaves = instances(expr, '_Leaf')
   if stop is None:
      leaves[start].formatter.right.append(
         r'^ \markup { \bold \fontsize #2 "mp" }')
   else:
      leaves[start].formatter.before.extend([
         r"\once \override TextSpanner #'bound-details "
            r"#'left-broken #'X = #8",
         r"\once \override TextSpanner #'dash-fraction = #0.25",
         r"\once \override TextSpanner #'dash-period = #1",
         r"\once \override TextSpanner #'bound-details "
            r"""#'left #'text = \markup { \bold \fontsize #2 "mp " }""",
         r"\once \override TextSpanner #'bound-details "
            r"#'left #'stencil-align-dir-y = #CENTER",
         r"\once \override TextSpanner #'bound-details "
            r"#'right-broken #'text = ##f",
         r"\once \override TextSpanner #'bound-details "
            r"#'right #'text = #(markup #:draw-line '(0 . -1))"
         ])
      leaves[start].formatter.right.append(r'\startTextSpan')
      leaves[stop].formatter.right.append(r'\stopTextSpan')
