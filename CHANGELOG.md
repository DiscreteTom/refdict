# CHANGELOG

## [Unreleased]

## [3.3.0] - 2019-07-27

>Using a string as the keys of the partial result instead of storing the partial result in a variable. In this way the representation of refdict is correct.

### Fixed

- Representation of partial refdict.

## [3.2.1]

### Fixed

Optimize documents.

## [3.2.0]

### Added

- Chain creation, just like creating new items in `dict`
  - `rd = refdict({}); rd['a.b'] = 1` will cause `rd = refdict({'a': {'b': 1}})`

## [3.1.0]

### Added

- Method `refdict.get(keys, default = None)`, just like `dict.get` but can be used with chain keys.

### Fixed

- The `str()` function.
- The `repr()` function.

## [3.0.0]

### Added

- Class method `findItem` to make non-refdict object has chain access and reference access effect.
  - `refdict.findItem(data, 'key1.key2')`.
- Solution to use chain access and reference access many times with operator `()`.
  - Operator `[]` will return a non-refdict object, so we can **NOT** use chain access or reference access after the first `[]`.
  - But operator `()` will return a **sub-refdict**, which contains all data of the original refdict, but stand for a part of the original refdict.
  - Finally, after querying sub-refdict using `()`, we need to use `[]` to get a non-refdict value.
  - So we can use chain access and reference access many times like `rd('key1.key2')('key3.key4')['key5.key6']`.

### Changed

- To realize sub-refdict, the member variable `refdict.data` become private. You have to use `refdict.load` to change the inner data of a refdict.

## [2.2.0]

### Added

- Support for chain containment check.
  - `'key1.key2' in refdict({'key1':{'key2':123}}) => True`.

## [2.1.0]

### Added

- Support for methods of built-in types.
  - `refdict({}).keys` is `dict.keys`.
  - `refdict([]).append` is `list.append`.
- Keys of operator `[]` & `[]=` can be `int` and `slice`.
- Support for simple containment check.
- Support for `str()`.
- Support for item's chain deletion.
  - `rd=refdict({'a':{'b':123}});del rd[a.b] => rd=refdict({'a':{}})`.

## [2.0.0]

### Changed

Rename `RefDict` to `refdict`.

## [1.0.0]

### Added

- Complete support for operator `[]` & `[]=`.
- Function `text` to get literal result with reference prefix.