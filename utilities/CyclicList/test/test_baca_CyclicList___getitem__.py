import baca


def test_baca_CyclicList___getitem___01( ):

   cyclic_list = baca.utilities.CyclicList(range(3))
   assert cyclic_list[0] == 0
   assert cyclic_list[1] == 1
   assert cyclic_list[2] == 2
   assert cyclic_list[3] == 0
   assert cyclic_list[4] == 1
   assert cyclic_list[5] == 2


def test_baca_CyclicList___getitem___02( ):

   cyclic_list = baca.utilities.CyclicList(range(3))
   assert cyclic_list[-0] == 0
   assert cyclic_list[-1] == 2
   assert cyclic_list[-2] == 1
   assert cyclic_list[-3] == 0
   assert cyclic_list[-4] == 2
   assert cyclic_list[-5] == 1
