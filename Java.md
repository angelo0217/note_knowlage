# Function 寫法
```javascript
public class TestFunction {

    interface IsSameData{
        boolean isSame(String a, String b);
    }

    @Test
    public void test() {
        Function strLen = t -> {
            System.out.println(t);
            return t;
        };

        Consumer cc = c -> {
            System.out.println("consumer: " + c);
        };

        Predicate isDoubleMax = o -> {
            if (o.equals("Test")) {
                return true;
            }
            return false;
        };

        strLen.apply("aaaaa");
        cc.accept("bbbbb");
        System.out.println(isDoubleMax.test("Test"));

        IsSameData isSameData = (a, b) -> {
            return a.equals(b);
        };

        System.out.println(isSameData.isSame("A", "A"));
    }

}
```
# java 17 switch
```javascript
    @Test
    public void switchDemo(){
        Map<String, Object> data = new HashMap<>();
        data.put("key1", "aaa");
        data.put("key2", 111);
        if (data.get("key1") instanceof String s) {
            log.info(s);
        }

        switch (data.get("key1")) {
            case String s  -> log.info(s);
            case Double d  -> log.info(d.toString());
            case Integer i -> log.info(i.toString());
            default        -> log.info("");
        }

        var word = switch (data.get("key1")) {
            case String s  -> s;
            case Double d  -> d.toString();
            case Integer i -> i.toString();
            default             -> {
                System.out.println("The color could not be found.");
                yield "Unknown Color";
            }
        };
        System.out.println(word);
    }
```