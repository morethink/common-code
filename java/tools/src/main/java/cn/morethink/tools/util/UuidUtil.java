package cn.morethink.tools.util;

import java.util.UUID;
import java.util.stream.IntStream;

/**
 * @author 李文浩
 * @date 2018/9/9
 */
public class UuidUtil {
    private UuidUtil() {
    }

    private static final String[] CHARS = new String[]{
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C",
            "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
            "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"};

    /**
     * like 550E8400-E29B-11D4-A716-446655440000
     *
     * @return
     */
    public static String genTypicalUuid() {
        return UUID.randomUUID().toString();
    }

    private static String genUuid(int length, int radix) {
        StringBuilder buffer = new StringBuilder();
        String uuid = UUID.randomUUID().toString().replace("-", "");
        IntStream.range(0, length).forEach(i -> {
            String str = uuid.substring(i * 4, i * 4 + 4);
            int x = Integer.parseInt(str, radix);
            buffer.append(CHARS[x % 0x3E]);
        });
        return buffer.toString();
    }

    /**
     * like 5Ts8MFp3
     *
     * @return
     */
    public static String genShortUuid() {
        return genUuid(8, 16);
    }
}
