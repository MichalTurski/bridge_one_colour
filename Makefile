demo:
	python3.9 run.py \
	--table_state='[[13, 11, 10, 9, 8, 7, 6], [], [5, 4, 2, 1], []]' \
	--nb_unknown_cards_op0=13 \
	--nb_unknown_cards_op1=13 \
	--unassigned_cards='[12, 3]'

demo_wo_full_visibility:
	python3.9 first_trick.py \
	--table_state='[[13, 11, 10, 9, 8, 7, 6], [], [5, 4, 2, 1], []]' \
	--nb_unknown_cards_op0=13 \
	--nb_unknown_cards_op1=13 \
	--unassigned_cards='[12, 3]'

demo_current_player_2:
	python3.9 first_trick.py \
	--table_state='[[9,8], [], [13,11,7,6], []]' \
	--nb_unknown_cards_op0=12 \
	--nb_unknown_cards_op1=5 \
	--unassigned_cards='[4]' \
	--current_trick=[10,12] \
	--current_player=2