package cn.morethink.tools.util;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Map;

/**
 * @author 李文浩
 * @version 2017/4/6.
 */
@Slf4j
public class JsonUtil {

    private JsonUtil() {

    }

    private static final ObjectMapper OBJECT_MAPPER;

    /**
     * 是否打印美观格式
     */
    private static boolean isPretty = true;

    static {
        //SerializerProvider sp = new StdSerializerProvider();
        //sp.setNullValueSerializer(new NullSerializer());
        OBJECT_MAPPER = new ObjectMapper();
        OBJECT_MAPPER.setDateFormat(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"));
    }

    public static ObjectMapper getObjectMapper() {
        return OBJECT_MAPPER;
    }

    /**
     * Java对象转Json字符串
     *
     * @param object Java对象，可以是对象，数组，List,Map等
     * @return json 字符串
     */
    public static String toJson(Object object) {
        String json = null;
        try {
            if (isPretty) {
                json = OBJECT_MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(object);
            } else {
                json = OBJECT_MAPPER.writeValueAsString(object);
            }
        } catch (Exception e) {
            log.warn("json error:{}", e.getMessage());
        }
        return json;
    }


    /**
     * Json字符串转Java对象
     *
     * @param json
     * @param c
     * @return
     */
    public static <T> T toPOJO(String json, Class<?> c) {
        T t = null;
        try {
            t = (T) OBJECT_MAPPER.readValue(json, c);
        } catch (IOException e) {
            log.info("context", e);
        }
        return t;
    }

    public static <T> T toPOJO(Map map, Class<T> clazz) {
        return OBJECT_MAPPER.convertValue(map, clazz);
    }

    /**
     * JSON串转换为Java泛型对象，可以是各种类型，此方法最为强大。用法看测试用例。
     *
     * @param <T>
     * @param jsonString JSON字符串
     * @param tr         TypeReference,例如: new TypeReference< List<FamousUser> >(){}
     * @return List对象列表
     */
    public static <T> T toList(String jsonString, TypeReference<T> tr) {

        if (jsonString == null || "".equals(jsonString)) {
            return null;
        } else {
            try {
                return OBJECT_MAPPER.readValue(jsonString, tr);
            } catch (Exception e) {
                log.warn("json error:" + e.getMessage());
            }
        }
        return null;
    }

    public static void prettyPrint(Object object) {
        try {
            log.info(OBJECT_MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(object));
        } catch (IOException e) {
            log.info("", e);
        }
    }

    public static void prettyPrint(String json) {

        try {
            Object object = OBJECT_MAPPER.readValue(json, Object.class);
            log.info(OBJECT_MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(object));
        } catch (IOException e) {
            log.info("字符串无内容");
        }
    }
}
