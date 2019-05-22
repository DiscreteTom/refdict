# refdict

在Python使用refdict更好地组织数据

使用`data['key.key.key.1.2.3']`

实现`data['key']['key']['key'][1][2][3]`的效果

兼容dict/list/tuple/string！

- [refdict](#refdict)
	- [Usage](#usage)
	- [Features](#features)
	- [Warnings](#warnings)
	- [Change Log](#change-log)
		- [v2.0.0](#v200)
		- [v1.0.0](#v100)

## Usage

在字符串值前面加上**引用前缀**使其变成**另一个对象的引用**。默认的引用前缀是`@`。可以在构造函数中传入参数`refPrefix`来改变引用前缀

在`[]`运算符中使用一个字符串实现refdict内容的链式访问。使用`.`作为多个key的连接符。可以在构造函数传入参数`divider`来改变分隔符

```python
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
rd = refdict(data)
print(rd['player.items.1']) # => restore your health by 20%
print(rd['player.attack']) # => 123
rd['player.items.1'] = 'empty'
print(rd['player.items.1']) # => empty
print(rd['player.items.:.1']) # => empty
rd['player.items.:'] = []
print(rd['player.items']) # => []
print(rd.text('player.me.attack')) # => @player.weapon.attack
```

## Features

- 能够解析`dict`/`list`/`tuple`/`str`和其他支持`[]`运算符的数据类型
  - 如果使用默认的分隔符`.`，那么`dict`的key中不能出现`.`
  - `list`/`tuple`/`str`之外的类型在解析key的时候作为`str`解析
- 可以在value中使用`.`连接属性
  - 如`rd['player.items.1'] = '@potion.red' = 'restore your health by 20%'`
- 链式解析
  - 因为`rd['player.weapon'] = '@sword'`，所以`rd['player.attack'] = '@player.weapon.attack' = '@sword.attack' = 123`
- 赋值操作。如果被赋值的对象是引用字符串，则仅解引用，不删除引用目标
  - 如`rd['player.items.1'] = 'empty'`解除了原本其指向`apple`的引用并赋值为`empty`，但是并没有删除`apple`
- 切片取值与赋值。对于`list`/`tuple`/`str`可以使用`[:]`进行切片
  - 如`rd['player.items.:.1'] = ['@apple', 'empty'][:][1] = ['@apple', 'empty'][1] = 'empty'`
- 使用`text`函数取字面值。text函数正常计算前n-1个key，然后直接返回最后一个key对应的字面值
  - 如`rd.text('player.me.attack')`计算`rd['player.me']`得到`player`对象，`attack`作为最后一个key直接返回字面值`@player.weapon.attack`

## Warnings

使用形如`item: @item`的递归引用会导致**死循环**，包括间接递归引用

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

## Change Log

### v2.0.0

改名。还是小写看起来舒服。但是不向前兼容了所以就用2.0.0的版本号好了

### v1.0.0

- 实现`[]`取值与赋值
- 实现`text`函数以获得字面值