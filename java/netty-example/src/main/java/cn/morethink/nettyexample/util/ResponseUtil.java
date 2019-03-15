package cn.morethink.nettyexample.util;

import io.netty.buffer.Unpooled;
import io.netty.channel.ChannelFutureListener;
import io.netty.channel.ChannelHandlerContext;
import io.netty.handler.codec.http.*;

/**
 * @author 李文浩
 * @date 2018/9/18
 */
public class ResponseUtil {
    private static final String SUCCESS = "SUCCESS";

    private ResponseUtil() {
    }

    private static final GeneralResponse notFoundGeneralResponse = new GeneralResponse(HttpResponseStatus.NOT_FOUND, "404 NOT_FOUND", null);

    private static final GeneralResponse successGeneralResponse = new GeneralResponse(HttpResponseStatus.OK, SUCCESS, null);

    public static void notFound(ChannelHandlerContext ctx, FullHttpRequest request) {
        response(ctx, request, notFoundGeneralResponse);
    }

    public static void success(ChannelHandlerContext ctx, FullHttpRequest request) {
        response(ctx, request, successGeneralResponse);
    }


    /**
     * 响应HTTP的请求
     *
     * @param ctx
     * @param request
     * @param generalResponse
     */
    public static void response(ChannelHandlerContext ctx, HttpRequest request, GeneralResponse generalResponse) {

        boolean keepAlive = HttpUtil.isKeepAlive(request);
        byte[] jsonByteByte = JsonUtil.toJson(generalResponse).getBytes();
        FullHttpResponse response = new DefaultFullHttpResponse(HttpVersion.HTTP_1_1, generalResponse.getStatus(),
                Unpooled.wrappedBuffer(jsonByteByte));
        response.headers().set(HttpHeaderNames.CONTENT_TYPE, HttpHeaderValues.APPLICATION_JSON);
        response.headers().setInt(HttpHeaderNames.CONTENT_LENGTH, response.content().readableBytes());

        if (!keepAlive) {
            ctx.write(response).addListener(ChannelFutureListener.CLOSE);
        } else {
            response.headers().set(HttpHeaderNames.CONNECTION, HttpHeaderValues.KEEP_ALIVE);
            ctx.write(response);
        }
        ctx.flush();
    }
}
