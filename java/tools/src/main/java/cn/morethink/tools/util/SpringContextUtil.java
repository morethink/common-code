package cn.morethink.tools.util;

import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.stereotype.Component;

/**
 * @author 李文浩
 * @date 2018/9/9
 */
@Component
public class SpringContextUtil implements ApplicationContextAware {
    private static ApplicationContext applicationContext = null;

    @Override
    public synchronized void setApplicationContext(ApplicationContext context) {
        if (SpringContextUtil.applicationContext == null) {
            SpringContextUtil.applicationContext = context;
        }
    }

    /**
     * Graceful get Spring ApplicationContext
     * @return
     */
    public static synchronized ApplicationContext getApplicationContext() {
        return applicationContext;
    }

    /**
     * Get bean from name
     * @param name the name of the bean to retrieve
     * @return
     */
    public static Object getBean(String name) {
        return getApplicationContext().getBean(name);
    }

    /**
     * Get bean from class
     * @param clazz the class type
     * @return
     */
    public static <T> T getBean(Class<T> clazz) {
        return getApplicationContext().getBean(clazz);
    }

    /**
     * Get bean from name and class
     * @param name the name of the bean to retrieve
     * @param clazz the class type
     * @return
     */
    public static <T> T getBean(String name, Class<T> clazz) {
        return getApplicationContext().getBean(name, clazz);
    }

}

