
**Package:** scala.collection.mutable._





---

### 🔢 Scala `Int` (Integer) Functions:
---------------------------------------

> `Int` in Scala is a 32-bit signed integer (alias for `java.lang.Integer`).  
> You can also use math and utility methods from `scala.math` and Java classes.

### 💡 Tips

| **Concept**               | **Details**                              |
|--------------------------|-------------------------------------------|
| `Int` is immutable        | Operations return new values              |
| Use `BigInt`              | For very large integers                   |
| Use `math._`              | For math operations                      |
| Watch for integer division | `5 / 2 = 2`, not `2.5` unless cast       |


---

## 🔹 Basics

| **Expression**      | **Description**               | **Example**             |
|---------------------|-------------------------------|--------------------------|
| `val x = 10`        | Declare an integer            | `val a: Int = 10`        |
| `x + y`, `x * y`    | Arithmetic operations         | `10 + 5`, `10 * 2`       |
| `x / y`, `x % y`    | Division, modulo              | `10 / 3 = 3`, `10 % 3 = 1` |
| `x.toFloat`, `.toDouble` | Type conversion         | `10.toFloat = 10.0f`     |
| `x.toString`        | Convert to string             | `100.toString = "100"`   |

---

## 🔍 Comparison & Logical

| **Expression**        | **Description**               | **Example**           |
|------------------------|-------------------------------|------------------------|
| `x == y`, `x != y`     | Equal / Not Equal             | `10 == 10` → `true`    |
| `x > y`, `x <= y`      | Relational operators          | `5 > 3` → `true`       |
| `x && y`, `x || y`     | Logical AND / OR              | `(x > 5) && (x < 10)`  |

---

## 🔁 Loops

| **Syntax**                     | **Description**                  | **Example**                          |
|--------------------------------|----------------------------------|--------------------------------------|
| `for (i <- 1 to 5)`            | Inclusive range                  | `1 to 5` → `1,2,3,4,5`               |
| `for (i <- 1 until 5)`         | Exclusive end                    | `1 until 5` → `1,2,3,4`              |
| `(1 to 5).foreach(println)`    | Print numbers                    | Loops over `1` to `5`                |

---

## 🧠 Math Operations (scala.math._)

```scala
import scala.math._
```

| **Function**            | **Description**                     | **Example**                   |
|-------------------------|-------------------------------------|-------------------------------|
| `abs(x)`                | Absolute value                      | `abs(-5)` → `5`               |
| `max(x, y)`             | Maximum of two values               | `max(3, 5)` → `5`             |
| `min(x, y)`             | Minimum of two values               | `min(3, 5)` → `3`             |
| `pow(x, y)`             | Power                               | `pow(2, 3)` → `8.0`           |
| `sqrt(x)`               | Square root                         | `sqrt(16)` → `4.0`            |
| `round(x)`              | Round float to nearest int          | `round(3.6)` → `4`            |
| `ceil(x)`               | Round up to nearest int             | `ceil(3.2)` → `4.0`           |
| `floor(x)`              | Round down to nearest int           | `floor(3.9)` → `3.0`          |
| `signum(x)`             | Sign: -1, 0, 1                      | `signum(-10)` → `-1`          |
| `random`                | Random double [0, 1)                | `random()`                    |

---

## 🔄 Conversion Functions

| **Function**         | **Description**                      | **Example**                  |
|----------------------|--------------------------------------|------------------------------|
| `x.toByte`, `.toShort`| Convert to smaller types            | `100.toByte` → `100`         |
| `x.toLong`           | Convert to Long                      | `100.toLong`                 |
| `x.toFloat`, `.toDouble` | Convert to decimal               | `100.toDouble = 100.0`       |
| `x.toChar`           | Convert to Char                      | `65.toChar` → `'A'`          |
| `x.toString`         | Convert to String                    | `123.toString = "123"`       |

---

## 🔧 Bitwise Operations

| **Operator**         | **Description**                      | **Example**                   |
|----------------------|--------------------------------------|-------------------------------|
| `x & y`              | Bitwise AND                          | `5 & 3` → `1`                 |
| `x | y`              | Bitwise OR                           | `5 | 3` → `7`                 |
| `x ^ y`              | Bitwise XOR                          | `5 ^ 3` → `6`                 |
| `~x`                 | Bitwise NOT                          | `~5` → `-6`                   |
| `x << n`             | Left shift                           | `2 << 1` → `4`                |
| `x >> n`             | Right shift                          | `8 >> 2` → `2`                |

---

## 🔢 Ranges

| **Expression**         | **Description**                    | **Example**                         |
|------------------------|------------------------------------|-------------------------------------|
| `1 to 5`               | Inclusive range                    | `Range(1, 2, 3, 4, 5)`              |
| `1 until 5`            | Excludes last                      | `Range(1, 2, 3, 4)`                 |
| `(1 to 10 by 2)`       | Step by 2                          | `Range(1, 3, 5, 7, 9)`              |

---



---

### ✨ Scala `String` Functions:
--------------------------------

> Strings in Scala are just Java `String`s, so you get both **Scala** and **Java-style** methods.


### 💡 Tips

| **Concept**                  | **Details**                                        |
|-----------------------------|-----------------------------------------------------|
| Scala Strings = Java Strings | You can use both Scala and Java methods             |
| Strings are immutable        | All operations return new strings                   |
| Use `StringBuilder`          | For efficient mutable string building               |
| Multiline strings            | Use triple quotes `""" ... """`                     |


---

## 🔹 Create & Basic Access

| **Syntax**               | **Description**                      | **Example**                         |
|--------------------------|--------------------------------------|-------------------------------------|
| `"Hello"`                | String literal                       | `val s = "Scala"`                   |
| `s.length`               | Number of characters                 | `"Scala".length` → `5`              |
| `s(i)`                   | Character at index                   | `"Scala"(2)` → `'a'`                |
| `s.charAt(i)`            | Java-style char access               | `s.charAt(1)`                       |

---

## 🔍 Check & Test

| **Function**            | **Description**                            | **Example**                                  |
|-------------------------|--------------------------------------------|----------------------------------------------|
| `s.isEmpty`             | Check if string is empty                   | `"".isEmpty` → `true`                         |
| `s.nonEmpty`            | Not empty                                  | `"abc".nonEmpty` → `true`                    |
| `s.contains("sub")`     | Check substring                            | `"Scala".contains("al")` → `true`            |
| `s.startsWith("prefix")`| Starts with prefix                         | `"Scala".startsWith("Sc")` → `true`          |
| `s.endsWith("suffix")`  | Ends with suffix                           | `"Scala".endsWith("la")` → `true`            |
| `s.equals("other")`     | Equals (case-sensitive)                    | `"abc".equals("abc")` → `true`               |
| `s.equalsIgnoreCase`    | Equals (case-insensitive)                  | `"abc".equalsIgnoreCase("ABC")` → `true`     |

---

## ✏️ Modify & Transform

| **Function**             | **Description**                         | **Example**                                |
|--------------------------|-----------------------------------------|--------------------------------------------|
| `s.toUpperCase`          | Convert to upper case                   | `"scala".toUpperCase` → `"SCALA"`          |
| `s.toLowerCase`          | Convert to lower case                   | `"Scala".toLowerCase` → `"scala"`          |
| `s.capitalize`           | Capitalize first letter                 | `"scala".capitalize` → `"Scala"`           |
| `s.trim`                 | Remove leading/trailing whitespace      | `" abc ".trim` → `"abc"`                   |
| `s.stripMargin`          | Remove margin symbol (e.g. `|`)         | `"""|hi""".stripMargin` → `"hi"`           |
| `s.reverse`              | Reverse string                          | `"abc".reverse` → `"cba"`                  |
| `s.replace("a", "b")`    | Replace character/substring              | `"abc".replace("a", "x")` → `"xbc"`        |
| `s.replaceAll("a", "b")` | Regex replace all                       | `"banana".replaceAll("a", "*")` → `"b*n*n*"`|
| `s.drop(n)`              | Drop first `n` chars                    | `"Scala".drop(2)` → `"ala"`                |
| `s.take(n)`              | Take first `n` chars                    | `"Scala".take(3)` → `"Sca"`                |
| `s.dropRight(n)`         | Drop from end                           | `"Scala".dropRight(2)` → `"Sca"`           |
| `s.takeRight(n)`         | Take from end                           | `"Scala".takeRight(2)` → `"la"`            |

---

## 🔠 Split & Join

| **Function**                   | **Description**                          | **Example**                                     |
|--------------------------------|------------------------------------------|-------------------------------------------------|
| `s.split(" ")`                 | Split into array                         | `"a b".split(" ")` → `Array("a", "b")`          |
| `s.split(",").toList`          | Convert to list                          | `"a,b".split(",").toList` → `List("a", "b")`    |
| `arr.mkString(",")`            | Join array or list into string           | `List("a", "b").mkString(",")` → `"a,b"`        |
| `s.linesIterator`              | Iterate over lines (multiline string)    | `"""a\nb""".linesIterator.toList` → `List("a", "b")` |

---

## 🔄 Convert & Cast

| **Function**           | **Description**                      | **Example**                          |
|------------------------|--------------------------------------|--------------------------------------|
| `s.toInt`, `toDouble`  | Convert to numeric                   | `"42".toInt` → `42`                  |
| `i.toString`           | Int to String                        | `42.toString` → `"42"`               |
| `s.toList`             | String to List[Char]                 | `"abc".toList` → `List('a','b','c')` |
| `s.toArray`            | String to Array[Char]                | `"abc".toArray`                      |

---

## 🔍 Search & Index

| **Function**             | **Description**                    | **Example**                           |
|--------------------------|------------------------------------|---------------------------------------|
| `s.indexOf("a")`         | First occurrence index             | `"banana".indexOf("a")` → `1`         |
| `s.lastIndexOf("a")`     | Last occurrence index              | `"banana".lastIndexOf("a")` → `5`     |
| `s.substring(start, end)`| Get substring                      | `"Scala".substring(1, 4)` → `"cal"`   |

---

## 🔁 Loop & Higher-Order

| **Function**               | **Description**                     | **Example**                          |
|----------------------------|-------------------------------------|--------------------------------------|
| `s.map(_.toUpper)`         | Apply function to each char         | `"abc".map(_.toUpper)` → `"ABC"`     |
| `s.foreach(println)`       | Iterate over characters             | `"hi".foreach(println)`              |
| `s.exists(_ == 'a')`       | Check if any character matches      | `"abc".exists(_ == 'a')` → `true`    |
| `s.forall(_.isDigit)`      | All characters satisfy condition    | `"123".forall(_.isDigit)` → `true`   |
| `s.count(_.isLower)`       | Count matching chars                | `"ScAlA".count(_.isLower)` → `2`     |

---

## 🔧 Misc & Utility

| **Function**             | **Description**                          | **Example**                         |
|--------------------------|------------------------------------------|-------------------------------------|
| `s.hashCode()`           | Hash value                               | `"abc".hashCode()`                  |
| `s.equalsIgnoreCase(s2)` | Case-insensitive comparison              | `"Hi".equalsIgnoreCase("hi")`       |
| `s.distinct`             | Unique characters                        | `"aabbc".distinct` → `"abc"`        |
| `s.groupBy(_.isUpper)`   | Group chars by function                  | `"AbC".groupBy(_.isUpper)`          |

---




---

### 📦 Scala `ListBuffer` Operations:
-------------------------------------

#### 💡 Tips

| **Pattern**                             | **Usage**                            |
|----------------------------------------|--------------------------------------|
| `v.map { case(x) => x * 2 }`           | Destructuring in functional ops      |
| `+=` vs `+=:`                          | Add to end vs beginning              |
| `+` vs `++`                            | Single vs multiple values            |


#### 🔹 Create and Add Elements

| **Syntax**                          | **Description**                          | **Example**                                 |
|------------------------------------|------------------------------------------|---------------------------------------------|
| `ListBuffer[T](vals...)`           | Create a new `ListBuffer`                | `val v = ListBuffer(1, 2, 3)`               |
| `v += value`                       | Add single element at end                | `v += 10`                                   |
| `v +=: value`                      | Add single element at beginning          | `v +=: 0`                                   |
| `v.append(val)`                    | Add at end                               | `v.append(20)`                              |
| `v.appendAll(Seq)`                 | Add multiple at end                      | `v.appendAll(Seq(4,5))`                     |
| `v.prepend(val)`                   | Add at beginning                         | `v.prepend(0)`                              |
| `v.prependAll(Seq)`                | Add multiple at beginning                | `v.prependAll(Seq(-2, -1))`                 |
| `v.insert(index, val)`             | Insert at specific index                 | `v.insert(1, 100)`                          |
| `v.insertAll(index, Seq)`          | Insert multiple at index                 | `v.insertAll(2, Seq(200, 300))`             |
| `v.patch(idx, Seq, len)`           | Replace `len` elements at `idx` with Seq | `v.patch(1, Seq(9,9), 2)`                   |
| `v ++= Seq`                        | Add multiple at end                      | `v ++= Seq(7,8,9)`                          |
| `v --= Seq`                        | Remove matching elements                 | `v --= Seq(2,3)`                            |
| **Note**                           | `+` = single value, `++` = collection    | `v += 1` vs `v ++= Seq(1,2)`                |

---

#### 🔍 Read Elements

| **Syntax**                | **Description**                     | **Example**                     |
|--------------------------|-------------------------------------|---------------------------------|
| `v(index)`               | Get element at index                | `v(2)`                          |
| `v.slice(start, end)`    | Sublist from `start` to `end - 1`   | `v.slice(1, 3)`                 |
| `v.head`, `v.last`       | First and last elements             | `v.head`, `v.last`              |
| `v.indexOf(val, from)`   | Index of value from `from` index    | `v.indexOf(5, 0)`               |

---

#### ✏️ Update Elements

| **Syntax**              | **Description**                    | **Example**                  |
|------------------------|------------------------------------|------------------------------|
| `v.update(idx, val)`   | Update value at index              | `v.update(1, 99)`            |

---

#### ❌ Delete Elements

| **Syntax**             | **Description**                    | **Example**                   |
|-----------------------|------------------------------------|-------------------------------|
| `v.remove(index)`     | Remove at specific index           | `v.remove(2)`                 |
| `v.clear()`           | Remove all elements                | `v.clear()`                   |
| `v -= val`            | Remove single value (if present)   | `v -= 5`                      |

---

#### 🛠️ Other Useful Operations

| **Function**                      | **Description**                                      | **Example**                               |
|----------------------------------|------------------------------------------------------|-------------------------------------------|
| `v.contains(val)`                | Check if value exists                                | `v.contains(3)`                           |
| `v.containsSlice(Seq)`           | Check for continuous sub-sequence                    | `v.containsSlice(Seq(2, 3))`              |
| `v.combinations(n)`              | All `n`-length combinations                          | `v.combinations(2).toList`                |
| `v.clone()`                      | Deep copy                                            | `val v2 = v.clone()`                      |
| `v.count(_ == val)`              | Count specific values                                | `v.count(_ == 2)`                         |
| `v.diff(Seq)`                    | Elements not in other Seq                            | `v.diff(Seq(1,2))`                        |
| `v.distinct`                     | Remove duplicates                                    | `v.distinct`                              |
| `v.endsWith(Seq)`                | Ends with a sequence                                 | `v.endsWith(Seq(4,5))`                    |
| `v.forall(_ > 18)`               | All elements satisfy condition                       | `v.forall(_ > 0)`                         |
| `v.foreach(println)`             | Iterate and apply function                           | `v.foreach(println)`                      |
| `v.filter(_ % 2 == 0)`           | Filter elements by condition                         | `v.filter(_ % 2 == 0)`                    |
| `v.groupBy(x => x)`              | Group by key                                         | `v.groupBy(x => x).map((k,v) => k -> v.length)` |
| `v.groupMapReduce(k)(v)(_+_)`    | Group and reduce                                     | `v.groupMapReduce(x => x)(_ => 1)(_ + _)` |
| `v.intersect(Seq)`               | Common elements                                      | `v.intersect(Seq(1, 2))`                  |
| `v.isEmpty`, `v.nonEmpty`        | Check emptiness                                      | `v.isEmpty`                               |
| `v.length`, `v.size`             | Number of elements                                   | `v.length`                                |
| `v.map(x => x*2)`                | Transform elements                                   | `v.map(_ * 2)`                            |
| `v.max`, `v.min`                 | Largest, smallest values                             | `v.max`, `v.min`                          |
| `v.mkString(", ")`              | Join to string with separator                        | `v.mkString(", ")`                        |
| `(a, b) = v.partition(cond)`     | Split based on condition                             | `v.partition(_ % 2 == 0)`                 |
| `v.permutations`                 | All permutations                                     | `v.permutations.toList`                   |
| `v.reverse`                      | Reverse order                                        | `v.reverse`                               |
| `v.reduce(_ + _)`                | Reduce to single value                               | `v.reduce(_ + _)`                         |
| `v.sliding(n)`                   | Sliding window views                                 | `v.sliding(2).toList`                     |
| `v.scan(0)(_ + _)`              | Cumulative sum (prefix sum)                          | `v.scan(0)(_ + _)`                        |
| `v.sorted`                       | Sort in ascending order                              | `v.sorted`                                |
| `v.sortBy(_ % 2)`                | Sort using function                                  | `v.sortBy(_ % 2)`                         |
| `(a, b) = v.splitAt(n)`          | Split at index `n`                                   | `v.splitAt(2)`                            |
| `v.sum`                          | Sum of all elements                                  | `v.sum`                                   |
| `v.toList`, `toArray`, etc.      | Convert to other collections                         | `v.toList`, `v.toArray`                   |
| `v.transpose`                    | Swap rows/columns (nested lists only)                | `ListBuffer(List(1,2), List(3,4)).transpose` |
| `v1.zip(v2)`                     | Pair elements from two lists                         | `ListBuffer(1,2).zip(ListBuffer("a","b"))`|
| `v.zipWithIndex`                 | Pair each element with index                         | `v.zipWithIndex`                          |

---


---

### 📦 Scala `Set` Operations:
------------------------------

> `Set` is an **immutable** or **mutable** collection of unique elements.  
> Import `scala.collection.mutable.Set` for mutable behavior.

### 💡 Tips

| **Concept**                     | **Details**                                  |
|--------------------------------|----------------------------------------------|
| **Set is unordered**           | Output order is not guaranteed               |
| **Immutable vs Mutable**       | Use `import scala.collection.mutable.Set`    |
| **No duplicates**              | Duplicate values are ignored                 |
| **Functional style preferred** | Use `map`, `filter`, etc., for transformations |

---

## 🔹 Create & Add Elements

| **Syntax**                          | **Description**                          | **Example**                                      |
|------------------------------------|------------------------------------------|--------------------------------------------------|
| `Set(val1, val2, ...)`             | Create immutable Set                     | `val s = Set(1, 2, 3)`                           |
| `mutable.Set(val...)`             | Create mutable Set                       | `val s = mutable.Set(1, 2)`                      |
| `s += value`                      | Add single element (mutable only)        | `s += 10`                                        |
| `s ++= Set(values)`               | Add multiple elements (mutable only)     | `s ++= Set(4, 5)`                                |
| `s.add(value)`                    | Add single element, returns Boolean      | `s.add(6)`                                       |

---

## 🔍 Read & Check

| **Syntax**             | **Description**                          | **Example**             |
|------------------------|------------------------------------------|--------------------------|
| `s.contains(value)`    | Check if element exists                  | `s.contains(2)`          |
| `s.head`, `s.tail`     | First element, remaining elements        | `s.head`, `s.tail`       |
| `s.isEmpty`            | Check if set is empty                    | `s.isEmpty`              |
| `s.size`, `s.length`   | Number of elements                       | `s.size`                 |
| `s.count(cond)`        | Count elements satisfying condition      | `s.count(_ > 2)`         |
| `s.exists(cond)`       | If any element satisfies condition       | `s.exists(_ % 2 == 0)`   |
| `s.forall(cond)`       | If all elements satisfy condition        | `s.forall(_ < 10)`       |

---

## ✏️ Update (Only in `mutable.Set`)

| **Syntax**            | **Description**                          | **Example**                |
|-----------------------|------------------------------------------|----------------------------|
| `s += value`          | Add an element                           | `s += 10`                  |
| `s -= value`          | Remove an element                        | `s -= 2`                   |
| `s ++= Set(vals)`     | Add multiple elements                    | `s ++= Set(5,6)`           |
| `s --= Set(vals)`     | Remove multiple elements                 | `s --= Set(1,2)`           |
| `s.clear()`           | Remove all elements                      | `s.clear()`                |

---

## ❌ Delete Elements

| **Syntax**         | **Description**               | **Example**             |
|--------------------|-------------------------------|--------------------------|
| `s - val`          | Remove element (immutable)     | `s - 3`                 |
| `s -- Set(...)`    | Remove multiple (immutable)    | `s -- Set(2,3)`         |
| `s.remove(val)`    | Remove and return Bool (mutable)| `s.remove(1)`           |

---

## 🔁 Transformations & Operations

| **Function**                | **Description**                            | **Example**                                |
|----------------------------|--------------------------------------------|--------------------------------------------|
| `s.map(f)`                 | Apply function                             | `s.map(_ * 2)`                             |
| `s.filter(cond)`           | Filter values                              | `s.filter(_ > 2)`                          |
| `s.flatMap(f)`             | Apply function returning sets              | `s.flatMap(x => Set(x, x * 10))`           |
| `s.collect { case ... }`   | Partial function filtering                 | `s.collect { case x if x % 2 == 0 => x }`  |
| `s.mkString(",")`          | Convert to string                          | `s.mkString(",")`                          |
| `s.toList`, `toArray`      | Convert to other collections               | `s.toList`, `s.toArray`                    |

---

## 📚 Set Algebra (Very Useful)

| **Function**             | **Description**                            | **Example**                             |
|--------------------------|--------------------------------------------|-----------------------------------------|
| `s1 ++ s2`               | Union of two sets                         | `Set(1,2) ++ Set(2,3)` = `Set(1,2,3)`   |
| `s1 & s2` or `intersect` | Intersection (common elements)            | `Set(1,2) & Set(2,3)` = `Set(2)`        |
| `s1 -- s2` or `diff`     | Elements in `s1` but not `s2`             | `Set(1,2,3) -- Set(2)` = `Set(1,3)`     |
| `s1.union(s2)`           | Same as `++`                              | `s1.union(s2)`                          |
| `s1.intersect(s2)`       | Same as `&`                               | `s1.intersect(s2)`                      |
| `s1.diff(s2)`            | Same as `--`                              | `s1.diff(s2)`                           |
| `s1.subsetOf(s2)`        | Check if `s1` is subset of `s2`           | `Set(1,2).subsetOf(Set(1,2,3))`         |
| `s1 == s2`               | Check if sets are equal                   | `Set(1,2) == Set(2,1)` → `true`         |

---

## 🔄 Iteration & Functional Ops

| **Function**               | **Description**                    | **Example**                          |
|----------------------------|------------------------------------|--------------------------------------|
| `s.foreach(println)`       | Loop through set                   | `s.foreach(println)`                |
| `s.reduce(_ + _)`          | Reduce to single value             | `s.reduce(_ + _)`                   |
| `s.fold(z)(op)`            | Fold with initial value            | `s.fold(0)(_ + _)`                  |
| `s.find(cond)`             | Find first matching element        | `s.find(_ > 2)`                     |
| `s.take(n)`                | First `n` elements                 | `s.take(2)`                         |
| `s.drop(n)`                | Skip first `n` elements            | `s.drop(2)`                         |
| `s.zipWithIndex`           | Pair with index                    | `s.zipWithIndex`                    |

---

## 🔧 Utility

| **Function**        | **Description**                   | **Example**           |
|---------------------|-----------------------------------|-----------------------|
| `s.clone()`         | Copy of set (mutable)             | `val s2 = s.clone()`  |
| `s.equals(other)`   | Check equality                    | `s.equals(Set(1,2))`  |
| `s.toSeq`, `toSet`  | Convert to sequence or set        | `s.toSeq`             |
| `s.hashCode()`      | Get hash code                     | `s.hashCode()`        |

---


---


### 🗺️ Scala `mutable.Map` Operations:
--------------------------------------

> Import mutable map:
```scala
import scala.collection.mutable.Map
```

### 💡 Tips

| **Concept**                   | **Details**                                             |
|------------------------------|----------------------------------------------------------|
| `Map` keys are unique        | Adding a key again will overwrite its value              |
| Mutable vs Immutable         | Use `mutable.Map` for in-place updates                   |
| Pattern matching on `(k, v)` | Useful in `map`, `filter`, `collect`, etc.               |
| `getOrElseUpdate`            | Add key with default if not exists                       |
| `clone`                      | For copying current map                                  |


---

## 🔹 Create & Add Elements

| **Syntax**                         | **Description**                          | **Example**                                        |
|-----------------------------------|------------------------------------------|----------------------------------------------------|
| `Map(key -> val, ...)`            | Create mutable map                       | `val m = Map("a" -> 1, "b" -> 2)`                  |
| `Map.empty[Key, Value]`           | Create empty map                         | `val m = Map.empty[String, Int]`                  |
| `m += (key -> val)`               | Add single key-value                     | `m += ("c" -> 3)`                                  |
| `m ++= Map(...)`                  | Add multiple pairs                       | `m ++= Map("d" -> 4, "e" -> 5)`                    |
| `m.put(k, v)`                     | Add/update and return old value (Option)| `m.put("f", 6)`                                    |
| `m.getOrElseUpdate(k, v)`         | Add only if key not present              | `m.getOrElseUpdate("g", 7)`                        |

---

## 🔍 Read & Access Elements

| **Syntax**               | **Description**                         | **Example**                        |
|--------------------------|-----------------------------------------|------------------------------------|
| `m(key)`                 | Get value for key (throws if not found) | `m("a")`                           |
| `m.get(key)`             | Option type get                         | `m.get("b")`                       |
| `m.contains(key)`        | Check if key exists                     | `m.contains("a")`                  |
| `m.keys`, `m.values`     | Get all keys or values                  | `m.keys`, `m.values`               |
| `m.isEmpty`, `m.nonEmpty`| Check if map is empty/non-empty         | `m.isEmpty`                        |
| `m.size`                 | Number of key-value pairs               | `m.size`                           |
| `m.keySet`               | All keys as Set                         | `m.keySet`                         |

---

## ✏️ Update Elements

| **Syntax**                   | **Description**                        | **Example**                          |
|------------------------------|----------------------------------------|--------------------------------------|
| `m(key) = newVal`            | Update value for a key                | `m("a") = 100`                        |
| `m.update(k, v)`             | Same as above                        | `m.update("b", 200)`                 |
| `m.put(k, v)`                | Add or update                        | `m.put("c", 300)`                    |

---

## ❌ Delete Elements

| **Syntax**                 | **Description**                    | **Example**                      |
|----------------------------|------------------------------------|----------------------------------|
| `m -= key`                 | Remove by key                     | `m -= "a"`                       |
| `m --= List(k1, k2)`       | Remove multiple keys              | `m --= List("b", "c")`           |
| `m.remove(key)`            | Remove and return old value (Option)| `m.remove("d")`                 |
| `m.clear()`                | Remove all entries                | `m.clear()`                      |

---

## 🔁 Transformations & Functional Ops

| **Function**                         | **Description**                          | **Example**                                       |
|-------------------------------------|------------------------------------------|---------------------------------------------------|
| `m.map { case (k, v) => ... }`      | Transform map                            | `m.map { case (k, v) => k -> (v * 10) }`          |
| `m.filter { case (k, v) => ... }`   | Filter by key/value                      | `m.filter { case (k, v) => v > 1 }`               |
| `m.flatMap { case (k, v) => ... }`  | Flatten to new key-value pairs           | `m.flatMap { case (k, v) => Map(k -> v, k -> v+1)}`|
| `m.collect { case ... }`            | Partial map transformation               | `m.collect { case (k, v) if v > 2 => k -> v*2 }`  |
| `m.foreach { case (k, v) => ... }`  | Loop through key-value pairs             | `m.foreach { case (k, v) => println(s"$k=$v") }`  |

---

## 🔧 Utility Functions

| **Function**                   | **Description**                         | **Example**                                |
|--------------------------------|-----------------------------------------|--------------------------------------------|
| `m.getOrElse(k, default)`      | Get value or default                    | `m.getOrElse("z", 0)`                      |
| `m.toList`, `toSeq`, `toMap`  | Convert to other collection types       | `m.toList`, `m.toSeq`                      |
| `m.clone()`                   | Copy of map                             | `val m2 = m.clone()`                       |
| `m.equals(m2)`                | Compare maps                            | `m.equals(m2)`                             |
| `m.mkString(", ")`           | Join to string                          | `m.mkString(", ")`                         |
| `m.zipWithIndex`              | Zip with index (as Iterable)            | `m.zipWithIndex`                           |
| `m.count { case (k, v) => ...}`| Count matching pairs                   | `m.count { case (k, v) => v > 2 }`         |
| `m.keysIterator`, `valuesIterator` | Iterate over keys or values         | `m.keysIterator.foreach(println)`          |

---

## 📚 Set-Like Operations (on keys)

| **Function**                        | **Description**                              | **Example**                                  |
|------------------------------------|----------------------------------------------|----------------------------------------------|
| `m.keySet.intersect(other.keySet)` | Common keys                                  | `m.keySet & m2.keySet`                        |
| `m.keySet.diff(...)`               | Key difference                               | `m.keySet -- m2.keySet`                       |
| `m ++ m2`                          | Merge two maps (later overwrites earlier)    | `m ++ m2`                                     |
| `m ++= m2`                         | In-place merge (mutable)                     | `m ++= m2`                                    |
| `m.updated(k, v)`                  | Return new map with updated value            | `m.updated("x", 42)`                          |

---



---

## 🔄 `scala.collection.mutable.Queue`
-------------------------------------

> FIFO (First In, First Out) – Elements are added at the end and removed from the front.


### 💡 Tips

| **Concept**               | **Details**                                          |
|--------------------------|-------------------------------------------------------|
| Queue = FIFO              | First in, first out – used for scheduling             |
| Stack = LIFO              | Last in, first out – used for undo/history            |
| Both are mutable          | Use when needing in-place modification                |
| `.toList`, `.toArray`     | Convert to immutable collections                      |


### ✅ Create & Modify Queue

| **Syntax**                           | **Description**                         | **Example**                                  |
|-------------------------------------|-----------------------------------------|----------------------------------------------|
| `val q = Queue(1, 2, 3)`            | Create a queue                          | `import scala.collection.mutable.Queue`      |
| `Queue.empty[Int]`                  | Empty queue                             | `val q = Queue.empty[Int]`                   |
| `q.enqueue(4)`                      | Add element to end                      | `q.enqueue(4)` → `Queue(1, 2, 3, 4)`          |
| `q.enqueueAll(Seq(5, 6))`           | Add multiple elements                   | `q.enqueueAll(List(5, 6))`                    |
| `q += 7`                            | Enqueue using `+=`                      | `q += 7`                                      |
| `q ++= Seq(8, 9)`                   | Enqueue multiple using `++=`            | `q ++= Seq(8, 9)`                             |
| `q.dequeue()`                       | Remove first element                    | `q.dequeue()` → removes `1`                   |
| `q.dequeueFirst(_ % 2 == 0)`        | Remove first matching element           | Removes first even number                     |
| `q.dequeueAll(_ > 3)`               | Remove all matching elements            | Removes all > 3                               |

### 🔍 Read / Utility

| **Function**             | **Description**                          | **Example**                        |
|--------------------------|------------------------------------------|------------------------------------|
| `q.front`, `q.head`      | First element                            | `q.front`                          |
| `q.last`                 | Last element                             | `q.last`                           |
| `q.isEmpty`, `q.nonEmpty`| Check emptiness                          | `q.isEmpty`                        |
| `q.size`                 | Queue size                               | `q.size`                           |
| `q.contains(4)`          | Check if element exists                  | `q.contains(4)`                    |
| `q.clear()`              | Remove all elements                      | `q.clear()`                        |
| `q.clone()`              | Copy of queue                            | `val q2 = q.clone()`               |

---

## 📚 `scala.collection.mutable.Stack`
---------------------------------------

> LIFO (Last In, First Out) – Last added is the first to be removed.

### ✅ Create & Modify Stack

| **Syntax**                            | **Description**                        | **Example**                                    |
|--------------------------------------|----------------------------------------|------------------------------------------------|
| `val s = Stack(1, 2, 3)`             | Create stack                          | `import scala.collection.mutable.Stack`        |
| `Stack.empty[Int]`                   | Empty stack                           | `val s = Stack.empty[Int]`                     |
| `s.push(4)`                          | Add element on top                    | `s.push(4)` → `Stack(4, 1, 2, 3)`               |
| `s.pushAll(List(5, 6))`              | Push multiple values                  | `s.pushAll(Seq(5, 6))`                          |
| `s += 7`                             | Push using shorthand                  | `s += 7`                                        |
| `s ++= List(8, 9)`                   | Push multiple                         | `s ++= List(8, 9)`                              |
| `s.pop()`                            | Remove and return top                 | `s.pop()` → removes last added                 |
| `s.pop2`                             | Remove and return top 2 elements      | `s.pop2` → `(top1, top2)`                      |

### 🔍 Read / Utility

| **Function**             | **Description**                          | **Example**                          |
|--------------------------|------------------------------------------|--------------------------------------|
| `s.top`, `s.head`        | Top element (peek)                      | `s.top`                              |
| `s.isEmpty`, `s.nonEmpty`| Check if stack is empty                 | `s.isEmpty`                          |
| `s.size`                 | Size of stack                           | `s.size`                             |
| `s.contains(2)`          | Check for value                         | `s.contains(2)`                      |
| `s.clear()`              | Remove all elements                     | `s.clear()`                          |
| `s.clone()`              | Clone/copy                              | `val s2 = s.clone()`                 |

---

## 🔁 Common Functional Ops (Work on Both)

| **Function**                        | **Description**                        | **Example**                                |
|------------------------------------|----------------------------------------|--------------------------------------------|
| `q.map(_ * 2)`                     | Transform each element                 | `q.map(_ * 2)`                             |
| `q.filter(_ % 2 == 0)`             | Filter elements                        | `q.filter(_ % 2 == 0)`                     |
| `q.foreach(println)`               | Print each element                     | `q.foreach(println)`                       |
| `q.exists(_ == 3)`                 | Check existence                        | `q.exists(_ == 3)`                         |
| `q.forall(_ > 0)`                  | All match condition                    | `q.forall(_ > 0)`                          |
| `q.sum`, `q.max`, `q.min`          | Aggregate values                       | `q.sum` → sum of elements                  |

---


 
    
    


