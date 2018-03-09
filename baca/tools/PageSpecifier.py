import abjad
import typing


class PageSpecifier(abjad.AbjadObject):
    r'''Page specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_systems',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        systems: typing.List[list] = None,
        ) -> None:
        if systems is not None:
            y_offsets: list = []
            for system in systems:
                y_offset = system[1]
                if y_offset in y_offsets:
                    message = f'systems overlap at Y-offset {y_offset}.'
                    raise Exception(message)
                else:
                    y_offsets.append(y_offset)
        self._systems = systems

    ### PUBLIC PROPERTIES ###

    @property
    def systems(self) -> typing.List[list]:
        r'''Gets systems.
        '''
        return self._systems
