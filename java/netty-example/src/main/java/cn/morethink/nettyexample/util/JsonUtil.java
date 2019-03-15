package cn.morethink.nettyexample.util;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import io.netty.buffer.ByteBuf;
import io.netty.handler.codec.http.FullHttpRequest;
import io.netty.util.CharsetUtil;

import java.lang.reflect.Type;

/**
 * @author 李文浩
 * @date 2018/9/5
 */
public class JsonUtil {

    private JsonUtil() {

    }

    private static final GsonBuilder gsonBuilder = new GsonBuilder();

    private static final Gson gson = gsonBuilder.disableHtmlEscaping().setDateFormat("yyyy-MM-dd HH:mm:ss").create();

    public static String toJson(Object o) {
        return gson.toJson(o);
    }

    public static <T> T fromJson(FullHttpRequest request, Class<T> c) {
        ByteBuf jsonBuf = request.content();
        String jsonStr = jsonBuf.toString(CharsetUtil.UTF_8);
        return gson.fromJson(jsonStr, c);
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
     * @param request
     * @param type    new TypeToken<List<yourbean>>(){}.getType()
     * @return
     */
    public static <T> T fromJson(FullHttpRequest request, Type type) {
        ByteBuf jsonBuf = request.content();
        String json = jsonBuf.toString(CharsetUtil.UTF_8);
        return gson.fromJson(json, type);
    }
}
