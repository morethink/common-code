package cn.morethink.tools.util;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.typeadapters.RuntimeTypeAdapterFactory;

import java.lang.reflect.Type;

/**
 * @author 李文浩
 * @date 2018/11/1
 */
public class GsonUtil {

    private GsonUtil() {

    }

    private static final GsonBuilder gsonBuilder = new GsonBuilder();

    private static final RuntimeTypeAdapterFactory<AssertBase> runtimeTypeAdapterFactory = RuntimeTypeAdapterFactory
            .of(AssertBase.class, "type")
            .registerSubtype(Assert.class, Assert.class.getName());

    private static final Gson gson = gsonBuilder
            .disableHtmlEscaping()
            .setDateFormat("yyyy-MM-dd HH:mm:ss")
            .registerTypeAdapterFactory(runtimeTypeAdapterFactory)
            .create();

    public static String toJson(Object o) {
        return gson.toJson(o);
    }



    public static <T> T fromJson(String json, Class<T> c) {
        return gson.fromJson(json, c);
    }

    /**
     * 把json字符串解析成List：
     * params: new TypeToken<List<yourbean>>(){}.getType()
     * 把json字符串解析成map：
     * new TypeToken<HashMap<String,Object>>() {}.getType()
     *
     * @param json
     * @param type    new TypeToken<List<yourbean>>(){}.getType()
     * @return
     */
    public static <T> T fromJson(String json, Type type) {
        return gson.fromJson(json, type);
    }
}