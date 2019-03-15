package cn.morethink.tools.util;


import org.springframework.beans.BeanUtils;
import org.springframework.beans.BeansException;
import org.springframework.beans.FatalBeanException;

import java.beans.PropertyDescriptor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;

/**
 * @author 李文浩
 * @date 2018/9/9
 */

public class SpecificBeanUtils extends BeanUtils {

    private SpecificBeanUtils(){}

    /**
     * Override copyProperties method
     * in order not to copy the field when its value is null
     *
     * @param source
     * @param target
     * @throws BeansException
     */
    public static void copyProperties(Object source, Object target) {
        Class<?> actualEditable = target.getClass();
        PropertyDescriptor[] targetPds = getPropertyDescriptors(actualEditable);
        for (PropertyDescriptor targetPd : targetPds) {
            if (targetPd.getWriteMethod() != null) {
                PropertyDescriptor sourcePd = getPropertyDescriptor(
                        source.getClass(), targetPd.getName());
                if (sourcePd != null && sourcePd.getReadMethod() != null) {
                    try {
                        doCopy(source, target, sourcePd, targetPd);
                    } catch (Exception ex) {
                        throw new FatalBeanException(
                                "Could not copy properties from source to target", ex);
                    }
                }
            }
        }
    }

    private static void doCopy(Object source, Object target, PropertyDescriptor sourcePd, PropertyDescriptor targetPd) throws IllegalAccessException, InvocationTargetException {
        Method readMethod = sourcePd.getReadMethod();
        if (!Modifier.isPublic(readMethod.getDeclaringClass().getModifiers())) {
            readMethod.setAccessible(true);
        }
        Object value = readMethod.invoke(source);

        if (value != null) {
            Method writeMethod = targetPd.getWriteMethod();
            if (!Modifier.isPublic(writeMethod.getDeclaringClass().getModifiers())) {
                writeMethod.setAccessible(true);
            }
            writeMethod.invoke(target, value);
        }
    }
}