import abjad

# all_ais = []
#
# def is_ais(permutation):
#    my_set = set()
#    for i in range(11):
#        next_ = i + 1
#        interval = (permutation[next_] - permutation[i]) % 12
#        my_set.add(interval)
#    return len(my_set) == 11
#
#
# def succession(row):
#    row = abjad.TwelveToneRow(row)
#    succession = []
#    for i in range(11):
#        next_ = i + 1
#        interval = (row[next_].number - row[i].number) % 12
#        succession.append(interval)
#    assert list(sorted(succession)) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
#    return succession
#
#
# start_time = time.time()
# total_ais = 0
# total_permutations = 0
# inner_numbers = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
# for permutation in itertools.permutations(inner_numbers):
#    permutation = (0,) + permutation + (6,)
#    if is_ais(permutation):
#        all_ais.append(permutation)
#        total_ais += 1
#    total_permutations += 1
# print('TOTAL PERMUTATIONS: {}'.format(total_permutations))
# stop_time = time.time()
# total_time = stop_time - start_time
# print('DONE in {} seconds!'.format(int(total_time)))

# all_ais = open('all_ais.py', 'r').read()
# all_ais = eval(all_ais)
# start = time.time()
# unique = set()
# unique_list = []
# for i, ais in enumerate(all_ais):
#    ais = abjad.TwelveToneRow(ais)
#    prime_form_string = str(ais)
#    inversion_string = str(ais.invert())
#    if (prime_form_string not in unique and
#        inversion_string not in unique):
#        unique.add(str(ais))
#        numbers = [_.number for _ in ais]
#        unique_list.append(numbers)
# unique_list.sort()
# stop = time.time()

# all_ieq_ais = open('all_ieq_ais.py', 'r').read()
# all_ieq_ais = eval(all_ieq_ais)


def is_link_chord(ais):
    for sextuple in abjad.sequence(ais).nwise(n=6):
        pc_set = abjad.PitchClassSet(sextuple)
        try:
            set_class = abjad.SetClass.from_pitch_class_set(pc_set)
            if set_class.rank == 17:
                return True
        except KeyError as e:
            print(e)
    return False


# link_chords = []
# for i, ais in enumerate(all_ieq_ais):
#    print(i)
#    if is_link_chord(ais):
#        print('FOUND LINK CHORD ', str(len(link_chords)))
#        link_chords.append(ais)

# link_chords = open('link_chords.py', 'r').read()
# link_chords = eval(link_chords)
# #link_chords = link_chords[:16]
#
# chords = []
# for link_chord in link_chords:
#    segment = abjad.PitchClassSegment(link_chord)
#    segment = segment.voice_vertically()
#    segment = segment.transpose(-24)
#    chord = abjad.Chord(segment, abjad.Duration(1))
#    chords.append(chord)
#
# score, rh_staff, lh_staff = abjad.Score.make_piano_score(chords)
#
# for i in range(len(rh_staff)):
#    written_pitches = []
#    note_heads = []
#    chords = [lh_staff[i], rh_staff[i]]
#    for chord in chords:
#        written_pitches.extend(chord.written_pitches)
#        note_heads.extend(chord.note_heads)
#    segment = abjad.PitchSegment(written_pitches)
#    for sextuple in abjad.sequence(segment).nwise(n=6):
#        try:
#            set_class = abjad.SetClass.from_pitch_class_set(sextuple)
#        except KeyError:
#            pass
#        if set_class.rank == 17:
#            for pitch in sextuple:
#                for note_head in note_heads:
#                    if note_head.written_pitch == pitch:
#                        note_head.tweak.color = 'red'
#            break
#
# abjad.override(score).spacing_spanner.strict_note_spacing = True
# abjad.override(score).bar_line.stencil = False
# abjad.override(score).bar_number.stencil = False
# abjad.override(score).span_bar.stencil = False
# abjad.override(score).time_signature.stencil = False
# abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 2)"
#
# abjad.label(rh_staff).with_indices()
# abjad.override(rh_staff).text_script.staff_padding = 10
#
# lilypond_file = abjad.LilyPondFile.new(
#    score,
#    global_staff_size=12,
#    )
# lilypond_file.layout_block.indent = 0
# lilypond_file.header_block.title = abjad.Markup('Link chords (provisional)')
# abjad.show(lilypond_file)
