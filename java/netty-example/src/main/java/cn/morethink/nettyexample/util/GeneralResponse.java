package cn.morethink.nettyexample.util;

import io.netty.handler.codec.http.HttpResponseStatus;
import lombok.Data;

/**
 * @author 李文浩
 * @date 2018/9/5
 */
@Data
public class GeneralResponse {
        private transient HttpResponseStatus status = HttpResponseStatus.OK;
        private String message = "SUCCESS";
        private Object data;

        public GeneralResponse(Object data) {
                this.data = data;
        }

        public GeneralResponse(HttpResponseStatus status, String message, Object data) {
                this.status = status;
                this.message = message;
                this.data = data;
        }
}
