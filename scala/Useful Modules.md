

## scala.collection.mutable._

1. ListBuffer()
2. ArrayBuffer()
3. HashMap(key -> value)
4. HashSet()
5. Map(key -> value)
6. MutableList()
7. Queue()
8. Seq()
9. Set()
10. TreeSet()
11. TreeMap()

## scala.io.\_

1. Source

   * fromFile(file\:File)
   * fromInputStream(is\:InputStream)
   * fromString(s\:String)
   * fromURI(uri: URI)
   * fromURL(url: URL)

2. StdIn

   * readBoolean()
   * readByte()
   * readChar()
   * readDouble()
   * readFloat()
   * readInt()
   * readLine()
   * readLong()
   * readShort()

3. Codec(charSet: Charset)

   * decoder
   * encoder
   * name

## scala.math.\_

* E
* Pi
* max(x, y)
* min(x, y)
* ceil(x)
* floor(x)
* round(x)
* exp(x)
* log(x)
* log10(x)
* pow(x, y)
* abs(x)
* sqrt(x)
* cbrt(x)
* random()

## scala.util.\_

* Random

  1. new Random(seed)
  2. nextBoolean()
  3. nextByte()
  4. nextDoble()
  5. nextFloat()
  6. nextInt(n)
  7. nextLong()
  8. nextString(length)

* Breaks

  - breakable
     - break()
     - continue





### 📦 `scala.collection.mutable._`

| Type          | Example Code                               | Description               |
| ------------- | ------------------------------------------ | ------------------------- |
| `ListBuffer`  | `val lb = ListBuffer(1, 2, 3); lb += 4`    | Mutable list              |
| `ArrayBuffer` | `val ab = ArrayBuffer(1, 2); ab.append(3)` | Resizable array           |
| `HashMap`     | `val hm = HashMap("a" -> 1); hm("b") = 2`  | Unordered key-value store |
| `HashSet`     | `val hs = HashSet(1, 2, 3); hs += 4`       | Unordered set             |
| `Map`         | `val m = Map("x" -> 10); m("y") = 20`      | General mutable map       |
| `MutableList` | `val ml = MutableList(1, 2); ml += 3`      | Legacy mutable list       |
| `Queue`       | `val q = Queue(1, 2); q.enqueue(3)`        | FIFO queue                |
| `Seq`         | `val s = Seq(1, 2); s :+= 3`               | Mutable sequence          |
| `Set`         | `val s = Set(1, 2); s += 3`                | Mutable set               |
| `TreeSet`     | `val ts = TreeSet(3, 1, 2)`                | Ordered set               |
| `TreeMap`     | `val tm = TreeMap("a" -> 1, "b" -> 2)`     | Ordered map               |

---

### 🧾 `scala.io._`

| Component           | Example Code                                   | Description        |
| ------------------- | ---------------------------------------------- | ------------------ |
| `Source.fromFile`   | `Source.fromFile("file.txt").getLines()`       | Read from file     |
| `Source.fromURL`    | `Source.fromURL("https://example.com")`        | Read from URL      |
| `Source.fromString` | `Source.fromString("line1\nline2").getLines()` | Read from a string |
| `StdIn.readLine()`  | `val name = StdIn.readLine("Enter: ")`         | Console input      |
| `StdIn.readInt()`   | `val x = StdIn.readInt()`                      | Read integer       |
| `Codec.UTF8.name`   | `val name = Codec.UTF8.name`                   | Character set info |

---

### 🧮 `scala.math._`

| Function              | Example Code            | Description                    |
| --------------------- | ----------------------- | ------------------------------ |
| `E`, `Pi`             | `val r = Pi * 2`        | Constants                      |
| `max`, `min`          | `max(5, 10)`            | Larger or smaller value        |
| `ceil`, `floor`       | `ceil(2.3), floor(2.9)` | Round up/down                  |
| `round`               | `round(2.6)`            | Round to nearest integer       |
| `exp`, `log`          | `exp(1), log(10)`       | Exponential and log            |
| `pow`                 | `pow(2, 3)`             | Power                          |
| `abs`, `sqrt`, `cbrt` | `abs(-5), sqrt(4)`      | Absolute value, root functions |
| `random()`            | `val r = random()`      | Random number \[0.0, 1.0)      |

---

### 🎲 `scala.util._`

| Component       | Example Code                                    | Description                   |
| --------------- | ----------------------------------------------- | ----------------------------- |
| `Random`        | `val r = new Random(); r.nextInt(100)`          | Random number generator       |
| `nextBoolean()` | `r.nextBoolean()`                               | Random boolean                |
| `nextString()`  | `r.nextString(5)`                               | Random string                 |
| `Breaks`        |                                                 | For simulating break in loops |
| `breakable`     | `breakable { for (...) { if (cond) break() } }` | Exits loop early              |
| `break()`       | `break()`                                       | Break out of the loop         |

---


### 📦 `scala.collection.immutable._`

| Type        | Example Code                                       | Description                |
| ----------- | -------------------------------------------------- | -------------------------- |
| `List`      | `val lst = List(1, 2, 3)`                          | Immutable linked list      |
| `Vector`    | `val vec = Vector(1, 2, 3)`                        | Immutable indexed sequence |
| `Map`       | `val m = Map("a" -> 1, "b" -> 2)`                  | Immutable key-value map    |
| `Set`       | `val s = Set(1, 2, 3)`                             | Immutable set              |
| `SortedMap` | `val sm = SortedMap(3 -> "c", 1 -> "a", 2 -> "b")` | Immutable sorted map       |
| `SortedSet` | `val ss = SortedSet(3, 1, 2)`                      | Immutable sorted set       |

---

### 🔧 `scala.util._`

| Component       | Example Code                                    | Description                   |
| --------------- | ----------------------------------------------- | ----------------------------- |
| `Random`        | `val r = new Random(); r.nextInt(100)`          | Random number generator       |
| `nextBoolean()` | `r.nextBoolean()`                               | Random boolean                |
| `nextString()`  | `r.nextString(5)`                               | Random string                 |
| `Breaks`        |                                                 | For simulating break in loops |
| `breakable`     | `breakable { for (...) { if (cond) break() } }` | Exits loop early              |
| `break()`       | `break()`                                       | Break out of the loop         |

---

### 🧩 `scala.util.matching._`

| Component      | Example Code                       | Description                   |                            |
| -------------- | ---------------------------------- | ----------------------------- | -------------------------- |
| `Regex`        | \`val pattern = "a(b               | c)".r\`                       | Regular expression pattern |
| `findFirstIn`  | `pattern.findFirstIn("abc")`       | Find first match in string    |                            |
| `findAllIn`    | `pattern.findAllIn("abc")`         | Find all matches in string    |                            |
| `replaceAllIn` | `pattern.replaceAllIn("abc", "x")` | Replace all matches in string |                            |
| `split`        | `pattern.split("abc")`             | Split string by pattern       |                            |

---


### 🧩 `scala.concurrent._`

| Component          | Example Code                                                | Description                                                                |
| ------------------ | ----------------------------------------------------------- | -------------------------------------------------------------------------- |
| `Future`           | `val f = Future { /* computation */ }`                      | Represents a computation that may complete in the future                   |
| `Promise`          | `val p = Promise[Int]()`                                    | Represents a writable, single-assignment container for a value of type `T` |
| `ExecutionContext` | `import scala.concurrent.ExecutionContext.Implicits.global` | Provides a global execution context for executing futures                  |

---

### 🧪 `scala.util.parsing._`

| Component      | Example Code                           | Description                       |
| -------------- | -------------------------------------- | --------------------------------- |
| `RegexParsers` | `object MyParser extends RegexParsers` | Base trait for parser combinators |
| `parseAll`     | `parseAll(expr, "1+2")`                | Parse input using the parser      |
| `success`      | `success("Parsed successfully")`       | Successful parse result           |
| `failure`      | `failure("Parse failed")`              | Failed parse result               |

---

---

### ⏳ `java.time` (Java 8+ Time API, used in Scala)

| Component           | Example Code                                          | Description                     |
| ------------------- | ----------------------------------------------------- | ------------------------------- |
| `LocalDate`         | `val date = LocalDate.now()`                          | Current date                    |
| `LocalTime`         | `val time = LocalTime.now()`                          | Current time                    |
| `LocalDateTime`     | `val dt = LocalDateTime.now()`                        | Date and time                   |
| `Duration`          | `val d = Duration.between(t1, t2)`                    | Duration between two times      |
| `Period`            | `val p = Period.ofDays(5)`                            | Represents a period (e.g. days) |
| `DateTimeFormatter` | `val fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd")` | Formatting dates                |

---

### 🧵 `scala.sys.process._`

| Component         | Example Code            | Description                        |                            |
| ----------------- | ----------------------- | ---------------------------------- | -------------------------- |
| Running a command | `"ls -la".!`            | Run shell command and print result |                            |
| Capturing output  | `val out = "whoami".!!` | Capture output of a shell command  |                            |
| Pipelining        | \`"ls" #                | "grep src" !\`                     | Chain commands using pipes |

---

### 🧾 `scala.xml._`

| Component    | Example Code                           | Description             |
| ------------ | -------------------------------------- | ----------------------- |
| XML literals | `val xml = <greeting>Hello</greeting>` | Inline XML structure    |
| Parsing XML  | `XML.loadString("<a><b>1</b></a>")`    | Convert string to XML   |
| Access node  | `xml \ "greeting"`                     | Navigate XML using path |

---

### 🌐 `scala.concurrent.duration._`

| Component        | Example Code                        | Description                      |
| ---------------- | ----------------------------------- | -------------------------------- |
| `Duration`       | `val d = 10.seconds`                | Create a finite duration         |
| `FiniteDuration` | `val fd: FiniteDuration = 1.minute` | Used with Futures and scheduling |
| `fromNow`        | `10.seconds.fromNow`                | Deadline 10 seconds from now     |

---




















