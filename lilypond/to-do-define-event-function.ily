% From Lucas-Fabian Moser:

makeSpace = #(define-event-function (size) (number?)
                #{
                  -\tweak #'stencil #(ly:make-stencil '() '(0 . 0.1) `(0 . ,size) ) _""
                #}
                )

%{ example

upper = \relative c'' {
     c1 \makeSpace 10
}

%}

% The two man points being:
% - use define-event-function instead of define-music-function
% - use a quasiquote ` instead of the quote ' for the pair (0 . [size]), 
% since size must be evaluated, hence unquoted by a comma (,size).
