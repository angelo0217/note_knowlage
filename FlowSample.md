# Flow
參考 https://ithelp.ithome.com.tw/articles/10234553
```mermaid
pie
title code language
"Jave" : 50
"Python" : 40
"C#" : 10
```
```mermaid
graph TB
    Start --> Open
    Open --> Put
    Put --> IsFit{"has name?"}
    IsFit -->|Y| Named
    Named --> End
    IsFit -->|N| GetName
    GetName --> Adam
    Adam --> register
```
```mermaid
sequenceDiagram
  Alice->>John: Hello John, how are you?
  loop Healthcheck
      John->>John: Fight against hypochondria
  end
  Note right of John: Rational thoughts!
  John-->>Alice: Great!
  John->>Bob: How about you?
  Bob-->>John: Jolly good!
```
```mermaid
classDiagram
  Class01 <|-- AveryLongClass : Cool
  <<interface>> Class01
  Class09 --> C2 : Where am i?
  Class09 --* C3
  Class09 --|> Class07
  Class07 : equals()
  Class07 : Object[] elementData
  Class01 : size()
  Class01 : int chimp
  Class01 : int gorilla
  class Class10 {
    <<service>>
    int id
    size()
  }
```