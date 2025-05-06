
Resource
---------
  - Git : https://github.com/rockthejvm
  - Youtube : https://www.youtube.com/@rockthejvm


Scala Pattern Matching:
-----------------------

**Switch on steriods**

```
object test 
{
    var n = 2
    var find = n match {
            case 1 => "first"
            case 2 => "second"
            case _ => "nothing"
        }
}
```

**Type Matching**
```
def func():Any = 45

val findType = func() match {
            case _:String => "this is string"
            case _:Int => "THis is Int"
            case _ => "something else"
        }

**Name Binding**

case class Person(name:String, age:Int)
val obj = Person("thamu", 23)

val a = obj match{
            case p @ Person(n, a) => f"${n} and ${a}"  // `p` referencing `Person(n, a)`
        }
```

**Conditional Guards**
```
val n = 1
val a = n match{
            case 1 => "first"
            case n if n % 10 == 1 => n + "st"
        }

<!-- list position -->
val l = List(1, 2, 3, 4, 5)
val m = l match{
            case List(1, _, 3, _*) => "Found expected" // _* : Remaining all element.
            case _ => "Unexpected"
        }
```

**Contravriance:**

<img width="789" alt="Screenshot 2025-05-05 at 10 23 42 PM" src="https://github.com/user-attachments/assets/64aef45b-269f-411e-bf7e-e8df80564fd2" />

<img width="785" alt="image" src="https://github.com/user-attachments/assets/b8776e02-50c9-4129-9fa2-a2c6cbf13c46" />

**Sending HTTP requests**
-------------------------
  - passing a payload String
  - Receive a response at some point - Future[String]
  - `AKKA` HTTP client API.


**Higher Order Functions:**

  <img width="790" alt="image" src="https://github.com/user-attachments/assets/ef11dd7f-e51b-4cb9-9cdd-5051a19ef2ad" />


**Looping**

  <img width="622" alt="image" src="https://github.com/user-attachments/assets/fc5322ef-37cc-4d49-9c9a-240466fc1d50" />

  <img width="759" alt="image" src="https://github.com/user-attachments/assets/cc7fc5ca-9343-45b2-bcdc-fbb023f7764b" />

  Rule of Thumb:
  --------------
    - Learning Scala, Ignore Loops
    - Teaching Scala, Stop teaching Loops!.

Nothing Data Type:
-------------------

  <img width="782" alt="image" src="https://github.com/user-attachments/assets/8027fe5c-9553-412a-982c-159eed76a811" />

  <img width="792" alt="image" src="https://github.com/user-attachments/assets/6f3d0ca7-4267-4641-9c93-af98881c54f7" />

Call By Name:
-------------

  <img width="788" alt="image" src="https://github.com/user-attachments/assets/39a1f522-bf1a-4137-9676-8b7077ad3b99" />

  <img width="747" alt="image" src="https://github.com/user-attachments/assets/12c0f012-e437-473a-a993-243c03571a9b" />

Read Files:
-----------





 



























