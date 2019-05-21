from refdict import RefDict

if __name__ == '__main__':
	data = {
		'player': {
			'name': 'DiscreteTom',
			'items': [
				'@apple',
				'@potion.red'
			],
			'weapon': '@sword',
			'attack': '@player.weapon.attack',
			'me': '@player'
		},
		'apple': 'restore your health by 10%',
		'potion': {
			'red': 'restore your health by 20%',
		},
		'sword': {
			'attack': 123,
			'value': 50
		},
	}
	rd = RefDict(data)
	print(rd['player.items.1']) # => restore your health by 20%
	print(rd['player.attack']) # => 123
	rd['player.items.1'] = 'empty'
	print(rd['player.items.1']) # => empty
	print(rd['player.items.:.1']) # => empty
	rd['player.items.:'] = []
	print(rd['player.items']) # => []
	print(rd.text('player.me.attack')) # => @player.weapon.attack