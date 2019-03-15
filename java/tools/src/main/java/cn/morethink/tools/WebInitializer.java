package cn.morethink.tools;

import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.support.SpringBootServletInitializer;

/**
 * 当将SpringBoot应用打成war部署到Tomcat时需要建立此类，使用SpringBoot内嵌的Tomcat则不需要
 *
 * @author 李文浩
 * @date 2018/9/9
 */
public class WebInitializer extends SpringBootServletInitializer {

    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(Application.class);
    }

}
