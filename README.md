# refdict

![PyPI](https://img.shields.io/pypi/v/refdict.svg)
![GitHub](https://img.shields.io/github/license/DiscreteTom/refdict.svg)

## Usage

- Using string as chain keys to realize chain access(including `dict`/`list`/`tuple`/`str`).
- String can perform as a reference of another item.

![](https://raw.githubusercontent.com/DiscreteTom/refdict/master/img/readme.png)

## Install

`pip install refdict`

## Features

- Using `refdict` just like using `dict`/`list`/`tuple`/`str`.
  - Methods of built-in types: `refdict({}).keys()` or `refdict([]).append(123)`.
  - Iteration and containment check: `for x in refdict([1, 2, 3])`.
  - Slice and slice assignment: `refdict([1, 2, 3])[:] => [1, 2, 3]`.
  - ...
- Chain accessing members using a string.
  - `refdict({'1':{'1':{'1':{'1':'1'}}}})['1.1.1.1'] => 1`.
- Using reference string to reference another item.

## Description

Use **reference prefix** to turn a string into a reference of another item. The default reference prefix is `@`. Reference prefix can be changed by the parameter `refPrefix` of the constructor of refdict.

The `[]` operator can be used for chain access and reference access. The separator of keys is `.` by default, and it can be changed by the parameter `separator` of the constructor.

Here is an example:

```python
data = {
	'player': {
		'name': 'DiscreteTom',
		'items': [
			'@potion.red'
		],
		'weapon': '@sword',
		'attack': '@player.weapon.attack',
		'me': '@player'
	},
	'potion': {
		'red': 'restore your health by 20%',
	},
	'sword': {
		'attack': 123
	},
}
rd = refdict(data)
print(rd['player.items.0']) # => restore your health by 20%
print(rd['player.attack']) # => 123
print(rd['player.items.:']) # => ['@potion.red']
print(rd.text('player.attack')) # => @player.weapon.attack
print('player.weapon' in rd) # => True
```

## Warnings

**Recursive references** like `item: @item` will cause **infinite loop**, including indirect reference.

```python
data = {
	'item': '@item', # => infinite loop!
	'wrapper': {
		'item': '@wrapper.item' # => infinite loop!
	},
	'a': '@b' # => infinite loop!
	'b': '@a' # => infinite loop!
}
```

## FAQ

- Q - Why I can't access the first item of `list`/`tuple`/`str` using `[1]`?
  - A - Of course you should use `[0]` to access the first item, just like using `list`/`tuple`/`str`. It's a little bit counter-intuitive but reasonable.
- Q - Why I got `KeyError` when using `rd['key1.key2']['key3.key4']`?
  - The first `[]` operator will return a non-refdict object, so you can't use chain keys in the following `[]`. To get a sub-refdict, you should use `()` operator, which means you should use `rd('key1.key2')['key3.key4']`.